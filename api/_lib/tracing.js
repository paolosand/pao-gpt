// Langfuse tracing bootstrap. Import this FIRST — before any other import — in any
// entry point that calls generate()/embed(), so the OTel SDK registers before the
// first span is created. No-ops entirely when Langfuse keys aren't configured
// (local dev, CI): the OTel API is safe to call with no SDK registered, and this
// mirrors guard.js's own rule that an unset secret disables a feature, never throws.
import { NodeTracerProvider } from '@opentelemetry/sdk-trace-node';
import { LangfuseSpanProcessor } from '@langfuse/otel';
import { containsConfidentialTerm, filterResponse } from './guard.js';

const enabled = Boolean(process.env.LANGFUSE_PUBLIC_KEY && process.env.LANGFUSE_SECRET_KEY);

let _spanProcessor = null;

if (enabled) {
  _spanProcessor = new LangfuseSpanProcessor({
    environment: process.env.VERCEL_ENV ?? 'development',
    // Export-time backstop applied to every observation's input/output/metadata.
    // A confidential-term hit blanks the WHOLE value rather than redacting in place —
    // same "uniform, not surgical" rule as guard.js's scrubConfidential(), for the same
    // reason: a redaction marker that appears on some traces and not others is itself
    // an identification oracle. This runs regardless of which call site produced the
    // observation, so it still holds even if a future call site forgets to sanitize.
    mask: ({ data }) =>
      containsConfidentialTerm(data) ? '[REDACTED — confidential term matched]' : filterResponse(data),
  });

  // NodeTracerProvider, not the full NodeSDK: NodeSDK's auto-registered context
  // manager doesn't reliably propagate the active span across awaits inside Vercel's
  // bundled function runtime (silently drops nested observations — "No active OTEL
  // span in context"). This is Langfuse's own documented workaround.
  new NodeTracerProvider({ spanProcessors: [_spanProcessor] }).register();
}

// Vercel Functions may freeze the process the instant the response ends, so every
// request must explicitly flush — there's no guarantee a later invocation's cold
// start will do it for you.
export async function flushTracing() {
  if (_spanProcessor) await _spanProcessor.forceFlush();
}
