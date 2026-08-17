import './_lib/tracing.js'; // must be first: registers the OTel SDK before any span is created
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { startActiveObservation, updateActiveObservation, propagateAttributes } from '@langfuse/tracing';
import { flushTracing } from './_lib/tracing.js';
import { check, filterResponse, scrubConfidential } from './_lib/guard.js';
import { generate } from './_lib/rag.js';
import { isGreetingSentinel, GREETING_BLOCKS } from './_lib/personality.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

function getProjectIds() {
  try {
    const raw = readFileSync(join(__dirname, '..', 'src', 'data', 'portfolio.json'), 'utf8');
    const json = JSON.parse(raw);
    // Only projects have stable .id fields. Work IDs are hardcoded in buildSystemPrompt defaults.
    return (json.projects ?? []).map(p => p.id);
  } catch {
    return [];
  }
}

const projectIds = getProjectIds();
const workIds = []; // use buildSystemPrompt defaults

function setSseHeaders(res) {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');
}

function sendEvent(res, payload) {
  res.write(`data: ${JSON.stringify(payload)}\n\n`);
  res.flush?.();
}

function streamText(res, text) {
  const tokens = text.match(/\S+\s*/g) ?? [];
  for (const token of tokens) {
    sendEvent(res, { type: 'token', text: token });
  }
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const { query, history = [] } = req.body ?? {};

  if (!query || typeof query !== 'string' || query.trim().length === 0) {
    res.status(400).json({ error: 'query is required and must be a non-empty string' });
    return;
  }
  if (query.length > 2000) {
    res.status(400).json({ error: 'query must be 2000 characters or fewer' });
    return;
  }
  if (!Array.isArray(history)) {
    res.status(400).json({ error: 'history must be an array' });
    return;
  }

  setSseHeaders(res);

  try {
    // tags is a trace-level attribute: it must go through propagateAttributes (context
    // propagation to every observation in this callback), not updateActiveObservation
    // (which only ever touches the single currently-active observation) — the latter
    // silently drops unrecognized fields rather than erroring, so this is easy to get
    // wrong quietly. Confirmed by direct trace inspection during instrumentation.
    await propagateAttributes({ tags: ['pao-gpt'] }, async () => {
      await startActiveObservation('chat-response', async () => {
        updateActiveObservation({
          input: query,
          metadata: { historyLength: history.length },
        });

        try {
          // Greeting sentinel: return hardcoded blocks, skip RAG and guard
          if (isGreetingSentinel(query)) {
            const textBlock = GREETING_BLOCKS.find(b => b.type === 'text');
            const embedBlocks = GREETING_BLOCKS.filter(b => b.type !== 'text');
            if (textBlock) streamText(res, textBlock.content);
            if (embedBlocks.length > 0) sendEvent(res, { type: 'embeds', blocks: embedBlocks });
            updateActiveObservation({ output: textBlock?.content ?? '', metadata: { outcome: 'greeting' } });
            res.write('data: [DONE]\n\n');
            res.end();
            return;
          }

          const guardResult = check(query);
          if (guardResult.isMalicious) {
            streamText(res, guardResult.response);
            updateActiveObservation({
              output: guardResult.response,
              metadata: { outcome: 'blocked', reason: guardResult.reason },
            });
            res.write('data: [DONE]\n\n');
            res.end();
            return;
          }

          const blocks = await generate(query, history, { projectIds, workIds });
          // Order matters: scrub client names across the WHOLE response first (a hit
          // replaces everything with a uniform refusal, so no per-term signal escapes),
          // then apply the per-block PII redaction to whatever survives.
          const safeBlocks = scrubConfidential(blocks);
          const filteredBlocks = safeBlocks.map(block =>
            block.type === 'text'
              ? { ...block, content: filterResponse(block.content) }
              : block
          );

          const textContent = filteredBlocks
            .filter(b => b.type === 'text')
            .map(b => b.content)
            .join('\n\n');

          const embedBlocks = filteredBlocks.filter(b => b.type !== 'text');

          updateActiveObservation({
            output: textContent,
            metadata: { outcome: 'generated', embedCount: embedBlocks.length },
          });

          streamText(res, textContent);
          if (embedBlocks.length > 0) sendEvent(res, { type: 'embeds', blocks: embedBlocks });

          res.write('data: [DONE]\n\n');
          res.end();
        } catch (err) {
          updateActiveObservation({ level: 'ERROR', statusMessage: err.message });
          throw err;
        }
      });
    });
  } catch (err) {
    console.error('Chat handler error:', err);
    if (!res.headersSent) {
      res.status(500).json({ error: 'Internal server error' });
    } else {
      sendEvent(res, { type: 'error', message: 'Something went wrong — try again in a moment' });
      res.end();
    }
  } finally {
    // Awaited, not waitUntil(): the SSE response is already fully sent by this point
    // (res.end() above), so this can't add latency for the client — it only keeps the
    // function invocation itself open until the trace is actually delivered, which the
    // platform guarantees regardless of whether request-context/waitUntil is wired up.
    await flushTracing();
  }
}
