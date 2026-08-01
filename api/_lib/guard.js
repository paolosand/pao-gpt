// api/lib/guard.js
//
// SCOPE NOTE: `check()` is a cheap first-pass regex filter for obvious jailbreak
// phrasing. It is NOT the confidentiality boundary and must never be mistaken for
// one — it matches literal wording only, so paraphrases pass through, and it sees
// one message at a time, so incremental multi-turn extraction never trips it.
// Confidentiality is enforced by the CLIENT CONFIDENTIALITY rules in personality.js
// (model-side) plus `filterResponse()` below (output-side backstop).
import { WITTY_REJECTIONS } from './personality.js';

// Real client / collaborator names must NEVER be committed to this repo — it is
// public. The denylist is supplied at runtime via the CONFIDENTIAL_TERMS env var
// (comma-separated) and is only ever read server-side inside a Vercel function.
// Empty/unset simply disables the backstop; it never throws.
function confidentialTerms() {
  return (process.env.CONFIDENTIAL_TERMS ?? '')
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean);
}

function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Word-bounded so a short term cannot match inside a longer, unrelated word (e.g.
// a term that is also an English word stem must not fire on its inflected forms).
// Anchors are only added where the term's own edge is a word character, so
// multi-word terms containing punctuation still behave.
function termPattern(term) {
  const body = escapeRegex(term);
  const lead = /^\w/.test(term) ? '\\b' : '';
  const tail = /\w$/.test(term) ? '\\b' : '';
  return new RegExp(`${lead}${body}${tail}`, 'i');
}

// CRITICAL — why this replaces the WHOLE response instead of redacting in place:
// a surgical redaction marker is an identification oracle. If the model can be made
// to echo an attacker-supplied list of companies, per-term redaction returns
// "[redacted], Google X, Acme, [redacted]" and names two clients in a single turn.
// Any filter keyed on a secret list leaks that list the moment its output is
// distinguishable. So a hit discards the entire response and returns a fixed reply
// that is byte-identical regardless of which term fired — and is deliberately worded
// to match the ordinary "I won't confirm or deny a guess" answer the model already
// gives for EVERY company guess, including companies Paolo never worked with. A
// prober therefore sees the same response for a real client and for a wrong guess.
const UNIFORM_REFUSAL =
  "Not something I can get into — Paolo's client work is confidential, and that covers who the clients were, so I won't confirm or rule out any guess. Happy to go deep on what he actually built though, or you can email him directly.";

export function containsConfidentialTerm(text) {
  return confidentialTerms().some((t) => termPattern(t).test(text));
}

// Applies to the full block array, post-generation. Returns the blocks untouched,
// or a single uniform refusal block if anything tripped the denylist.
export function scrubConfidential(blocks) {
  const terms = confidentialTerms();
  if (terms.length === 0) return blocks;

  const hit = blocks.some(
    (b) => typeof b.content === 'string' && containsConfidentialTerm(b.content),
  );
  if (!hit) return blocks;

  return [{ type: 'text', content: UNIFORM_REFUSAL }];
}

const PROMPT_INJECTION_PATTERNS = [
  /ignore\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?|context)/i,
  /disregard\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?|context)/i,
  /forget\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?|context)/i,
  /you\s+are\s+now\s+a?\s*(different|new|another)?\s*(ai|assistant|bot|model)/i,
  /pretend\s+(you\s+)?(have\s+no\s+restrictions|you\s+are|to\s+be)/i,
  /act\s+as\s+(if\s+you\s+(are|were)\s+)?(a\s+)?(different|unrestricted|evil|dan)/i,
  /jailbreak/i,
  /prompt\s+injection/i,
  /system\s+prompt/i,
  /reveal\s+(your\s+)?(instructions?|prompts?|system|context|training)/i,
  /bypass\s+(your\s+)?(restrictions?|filters?|guidelines?|safety)/i,
  /override\s+(your\s+)?(restrictions?|instructions?|programming)/i,
  /do\s+anything\s+now/i,
  /\bdan\b.*mode/i,
  /developer\s+mode/i,
  /sudo\s+(mode|access)/i,
];

const SENSITIVE_INFO_PATTERNS = [
  { pattern: /\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b/g, label: 'SSN' },
  { pattern: /\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b/g, label: 'phone' },
];
// Note: /g flag is required for String.replace() to replace all occurrences

function randomRejection() {
  return WITTY_REJECTIONS[Math.floor(Math.random() * WITTY_REJECTIONS.length)];
}

export function check(message) {
  for (const pattern of PROMPT_INJECTION_PATTERNS) {
    if (pattern.test(message)) {
      return {
        isMalicious: true,
        reason: `Matched pattern: ${pattern}`,
        response: randomRejection(),
      };
    }
  }
  return { isMalicious: false, reason: null, response: null };
}

export function filterResponse(text) {
  let out = text;
  for (const { pattern } of SENSITIVE_INFO_PATTERNS) {
    out = out.replace(pattern, '[REDACTED]');
  }
  // NOTE: client-name scrubbing deliberately does NOT happen here. Per-block
  // redaction would leak which term matched — see scrubConfidential() above.
  return out;
}
