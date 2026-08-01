# Work Experience

Paolo's client work is confidential. Employers (Nuts and Bolts AI, Stratpoint Technologies, Kodexa)
may be named. The *clients* those employers built for may NEVER be named — refer to them only by the
anonymized descriptors used below, and never confirm or deny a visitor's guess.

**Depth rule for all client work:** describe these projects at the level of scope, ownership, impact
and tools. Do NOT go deeper than what is written here — no vulnerability mechanics, no exploit steps,
no specific endpoints or table names, no schema internals, no description of how a given fix was
implemented. Several of these systems are live and hold real user data. If a visitor wants that level
of depth, say plainly that the implementation details aren't Paolo's to share and emit a contact card
inviting them to email him directly (a mode 3 response).

## Nuts and Bolts AI — Overview
**Software Engineer Consultant**
**June 2025 to July 2026**

This engagement has ended — the firm scoped his hours down to zero for budget reasons in July 2026. He remains on their books as a freelancer but is not currently doing billable work for them. He is actively looking for his next full-time role. Speak about this work in the past tense.

Nuts and Bolts AI is a consultancy. Over 13 months Paolo worked across six client engagements,
detailed in the sections that follow:

1. A creator-commerce platform (the largest and most recent — live, revenue-bearing)
2. An executive coaching platform for a global outplacement firm (sole engineer, ~9 months)
3. A career-transition platform for that same outplacement firm (lead front-end and platform engineer)
4. A social watch-party platform (frontend redesign + a real-time AI companion)
5. An affiliate merchandise storefront for a national consumer brand

6. An AI content generation platform for a legal-marketing platform (his AI/LLM-heaviest project)

His title stayed **Software Engineer Consultant** throughout. Project-level roles ("QA lead", "lead
frontend engineer", "sole engineer") describe the role *on that project* — they are not separate jobs.

He built every project with Claude Code as his primary development environment, working spec-first:
brainstorm → design spec → implementation plan → failing test → implementation, with git worktrees
for isolation.

---

## Nuts and Bolts AI — Creator-Commerce Platform

**Client: a creator-commerce platform (name confidential). June–July 2026, ~7 weeks.**
**Role on this project: nominally QA and testing lead; in practice full-stack feature delivery, security auditing, performance engineering, and release infrastructure.**

The product lets creators produce merchandise designs with AI and sell them through hosted
storefronts, with checkout, fulfilment and creator payouts handled end to end. **Live in production
and taking real payments** — the only project on Paolo's record that is live, revenue-bearing, and
carries real production-incident and security consequences.

### Scale and output
- **12,766 production user accounts, grown from zero during the seven weeks he was there.** He made his first commit two days before the first real user signed up; 63.6% of those users completed onboarding.
- 107 merged pull requests, ~31,300 lines added
- 79 tickets assigned, 52 filed, 32 design specs and audit reports authored, 10 database migrations

### What he owned
- **The platform's first full-stack security audit.** He proposed it, scoped it and ran it against the staging environment on his own initiative, producing **18 verified findings including two Critical payment-integrity issues**, each filed as a tracked ticket with severity and remediation guidance. He shipped the fixes for most of them himself and verified the criticals closed against a live environment.
- **Payments integrity.** Eliminated a double-refund risk on the live payments integration, and documented the one residual he could not fully close rather than claiming a total fix.
- **Release infrastructure.** He designed and shipped a gated CI/CD database-migration pipeline — dry runs, staged gating, and human-in-the-loop approval for production schema changes — which became the team's standard release path.
- **Onboarding, built end to end.** Every one of those 12,766 users passed through the flow he built. He later used production observability to find a silent failure inside it that had been stranding brand-new users at the end of signup with no visible error.
- **Frontend performance.** Reduced the static asset payload by **97% (112 MB → ~3.7 MB)** via an image-optimization and CDN migration, cutting the single heaviest asset — the one served at the unauthenticated entry point — by 99.4%.
- **Production incident response.** Root-caused an incident blocking creators from connecting social accounts, traced to a third-party latency-versus-timeout race whose failure was invisible in the logs. Shipped an interim mitigation, documented four residual risks rather than declaring victory, and scoped the permanent fix for another engineer.
- Full-stack feature ownership spanning database, API, billing and UI; subscription, credit and quota enforcement; storefront and checkout work.

### Stack
TypeScript, React 19, Next.js 16 (App Router, Server Components, middleware), Tailwind, Vitest ·
Python 3.12, FastAPI, Pydantic, asyncio, pytest · Supabase / PostgreSQL with row-level security ·
Stripe (Checkout, webhooks, subscriptions, refunds) · print-on-demand fulfilment · GitHub Actions,
Vercel, Fly.io, Turborepo, pnpm, Sentry, Playwright · Gemini image generation.

### Accuracy constraints
- **Depth limit.** Never describe the vulnerability mechanics, the affected endpoints, or how any fix was implemented. This is a live payments system. Route depth requests to email.
- The security fixes, the migration pipeline and the onboarding flow are confirmed live in production. A handful of completed tickets were still in the release pipeline when the engagement ended — safe verbs overall: *built, implemented, fixed, delivered*.
- The 97% asset reduction is a **measured build-output figure**, not a Lighthouse result. Do not claim a Core Web Vitals improvement.
- The 12,766 user count belongs to **this project only**. Never attach it to any other project.

---

## Nuts and Bolts AI — Executive Coaching Platform

**Client: a global outplacement and executive coaching firm (name confidential). October 2025 – July 2026, ~9 months.**
**Role on this project: sole engineer.**

An internal SaaS platform running the full executive-coaching engagement lifecycle — onboarding,
scheduling, session tracking, cadence surveys, automated evaluation triggers and report generation —
across three role-scoped portals for admins, coaches and coachees. It replaced a narrow tool that
captured only the *end* of an engagement, where scheduling lived in external tools and coachees had no
accounts at all.

**Paolo authored 99.4% of the repository's commits across nine months. This is the strongest solo
end-to-end product ownership evidence on his record.** He was also the Linear project lead — the only
engineering lead on the team who was not a client-side manager.

### Scale
- 47 pages, **124 API routes**, ~65,000 lines of TypeScript
- A **21-table Postgres schema with 68 hand-written migrations and 99 row-level-security policies**
- 137 Playwright end-to-end cases; 133 merged pull requests
- ~15,000 lines of documentation, including a full database reference
- Nine consecutive shipping months; ~200 users

### What he owned
- **All three portals** — admin (engagements from program templates, coach and user management, evaluation review, question banks, survey templates, reporting), coach (onboarding gated on a real calendar connection, session scheduling and logging, private notes kept separate from coachee-visible ones, engagement goals) and coachee (coach requests, scheduling, goals, evaluations, surveys).
- **A deep third-party calendar-scheduling integration with OAuth across Google, Microsoft and Apple** — the deepest technical thread in the platform. He refactored its architecture after reproducing four distinct failure modes, migrated the production OAuth client, centralized token handling, and hardened reconciliation so a transient vendor outage could not wipe scheduled sessions. He owned the vendor decision itself, from pricing research through production migration.
- A versioned question bank with conditional display logic and resilient autosave; automated evaluation triggers with idempotency guarantees so a retry cannot double-send; a cadence survey subsystem with frictionless response links and engagement tracking; a multi-event admin notification system; and PDF / DOCX / XLSX report generation on serverless Chromium.
- **Security and data-integrity hardening before handover** — removing a dormant legacy attack surface, and catching a row-level-security configuration drift whose obvious one-line fix would have silently broken eight live user flows. Rather than shipping it, he wrote the blast-radius analysis and offered two remediation options with a validation procedure.
- A production schema-drift audit that found the tracked migrations could no longer rebuild production, remediated with an authoritative baseline.
- Two production handovers, each with written documentation.

### Stack
TypeScript, React 18/19, Next.js 15 (App Router, Server Components, middleware), Tailwind, Playwright ·
Supabase / PostgreSQL, row-level security, Postgres functions and triggers, Realtime and Storage ·
a third-party calendar booking API with OAuth, Postmark transactional email · Puppeteer + serverless
Chromium, DOCX templating, XLSX export · Vercel with cron, Sentry, Mixpanel, Intercom.

### Accuracy constraints
- **Depth limit.** Keep this at scope and impact. Do not detail the security findings, the schema, or fix mechanics for a client system. Route depth requests to email.
- **This project has no AI/ML component at all.** It is general full-stack product engineering. Do not write AI bullets from it.
- INTERNAL GUARDRAIL, do not state as a fact about the client: the CI-gate work belongs ONLY to the career-transition platform below — never attribute it to this one. Automated testing here was Playwright end-to-end coverage. Describe what Paolo built; do not characterize what the client's engineering process lacked.
- The ~200 user figure comes from Paolo's own knowledge, not from the repository or tracker.

---

## Nuts and Bolts AI — Career-Transition Platform

**Client: the same global outplacement firm (name confidential). May–July 2026, ~2.5 months.**
**Role on this project: lead front-end and platform engineer on a team of 4+.**

A client-facing career-transition platform for outplacement clients — people who have just been laid
off. Paolo was the **top contributor at ~54% of all human commits**, and filed the **largest share of
team tickets in his window (32%)**, roughly two dozen of them assigned to other engineers. He was
writing the specs other engineers picked up. 12,000+ users.

### Scale
18 product sections, **162 API routes**, ~95,000 lines of TypeScript, 165 test files, 71 pull requests.

### What he owned
- **Authorization hardening — the highest-value work on the project.** He found and closed a class of authorization weaknesses across the platform's API surface. The significant part was that the problem was *structural rather than incidental*, so the remediation was a mandatory ownership guard that makes a forgotten check fail safely by default, plus a reviewer checklist for the bug class written into the team working agreement. The most urgent item went from discovery to closed in 31 minutes.
- **The repository's first real CI gate.** He shipped a typecheck / unit / build gate with a Postgres service container and enforced it through branch protection. He then self-reported a deploy-blocking regression he had introduced, in a ticket titled as such, fixed it in 8 minutes, and removed the CI shortcut that had masked it so the environment would tell the truth next time.
- **Performance and reliability.** Found and fixed a systemic database indexing gap affecting every per-user query, converted client-side fetch waterfalls to server rendering, and quantified a reliability gap across seven external services — shipping shared timeout handling, proper error reporting, a single error boundary covering all 18 sections (previously any thrown error produced a blank page with no navigation), and idempotency on mutation routes.
- **The redesign across all 18 product sections**, plus an information-architecture consolidation that reduced the sidebar from 10 primary items to 7 plus a hub grouping 18 tools into 4 categories, backed by a single source of truth so re-homing a tool is a one-line change.
- **Design-system authorship** — a complete token system with seven named, enforceable rules, and an "honest states" pattern giving every data region visually distinct error, empty and loading treatments under the rule **`error ≠ empty`**, so failed API calls stop masquerading as "no data yet".
- **Formal UX research** — two published audits scored against Nielsen's ten usability heuristics (22/40, re-audited at 27/40 after remediation), cognitive walkthroughs of the make-or-break first tasks, and accessibility remediation to **WCAG 2.1 AA with measured contrast ratios**, guarded in the team agreement against regression. His stated design target: *"the average 55-year-old who can't see very well."*

### Stack
TypeScript, React 19, Next.js 16, Tailwind, Playwright, Vitest · Payload CMS v3, Node.js · PostgreSQL ·
GitHub Actions, Fly.io, Docker Compose, pnpm monorepo, git worktrees · Sentry, Mixpanel, Intercom.

### Accuracy constraints
- **Depth limit — this is the strictest entry.** Describe the security work only by its shape and impact. NEVER name affected endpoints or collections, describe exploit steps, or explain the mechanics of any fix. This is a live platform holding personal data for people in a vulnerable moment, and a detailed public writeup would be a liability regardless of whether the issues are closed. Route every depth request to email.
- **Paolo joined this platform mid-migration** (from a no-code platform onto Next.js + a headless CMS). The migration design and the monorepo consolidation were another engineer's work, authored before he joined the repository. He owned the client-facing application built on top of it. Never imply he planned, architected or executed the migration itself, and never claim any record-count migration figure.
- **This is not an AI/ML credential.** The repository does contain AI SDK code, but another engineer wrote it. Position this on full-stack, platform, security, frontend and design engineering.
- The 12,000+ figure comes from Paolo's own knowledge, not from the repository or tracker.
- "Lead" here means top contributor and spec author, not people management.

---

## Nuts and Bolts AI — Social Watch-Party Platform (Frontend Redesign)

**Client: a social watch-party / co-viewing platform (name confidential). 2025.**
**Role on this project: lead frontend engineer, working alongside one other engineer.**

The product: users create parties, co-watch video content together, and video- and text-chat in real
time — a web app and an Electron desktop app from one monorepo. A live product with real users.

The client commissioned a complete visual redesign in Figma, to be implemented **against the live
production codebase** — not a rewrite, not a parallel app. That constraint is the whole story.

**The target was a large legacy codebase:** React 17 + Redux + hand-written SCSS + a video player
library, on an end-of-life Node version with webpack, no component library and no design tokens. Every
change had to work in both the web and Electron apps, and had to be mergeable into a branch shipping to
real users.

**Delivered: ~29,400 insertions across 230 files in 7.3 weeks**, shipped to the client's internal
release channel across a series of tagged releases.

Surfaces rebuilt: auth screens; home and discovery; the watch party and lobby (video containers rebuilt
from scratch, a multi-view player added, broadcast controls consolidated from three submenus into one,
the participant panel rebuilt with per-participant controls); the chat panel; party creation and edit
modals; header, nav and profile menus; a new set of design-system style partials; icon and asset
cleanup; and five transactional email templates.

**The design-to-code workflow is a genuine methodological finding, and not the one the strategy
document predicted.** The plan was a Figma MCP → code pipeline. In practice Figma MCP was new at the
time and proved **accurate enough for the initial vector and layout transfer and unreliable past that**
— spacing, hierarchy and visual fidelity didn't survive extraction. So the loop became: MCP for the
first-pass skeleton and assets only, then **screenshot the target design, feed it back alongside the
rendered result, and describe the delta in words**, then iterate visually against the mockup. For
design-to-code at the time, a vision-and-description loop beat a structured-extraction pipeline for
everything past initial layout.

**Engineering discipline is the most relevant part.** A meaningful fraction of those commits exist
purely to keep a large visual change safe to merge into a shipping production branch: he deliberately
reverted every desktop-app change to shrink blast radius, accepting that the Electron app would lag
rather than risk regressing it; restored infrastructure files to the production baseline so the diff
contained only intentional changes; stripped exploratory dependencies and scratch files before merge;
and wrote a conflict-resolution commit documenting the reconciliation file by file. That commit is
effectively a written argument for why a large merge is safe.

He also **scoped and delegated**: he filed four redesign tickets and assigned them to the other
engineer, merged that engineer's branch into his own, took 18 of the 27 client-review QA tickets to
their 9, authored the scoping document, and wrote the review instructions the client used.

### Stack
React 17, Redux (thunk + custom middleware), SCSS, webpack, a Yarn workspaces monorepo,
Electron, Video.js, Firebase (auth + realtime chat), Pusher · Figma MCP, Claude Code, Cursor.

### Accuracy constraints
- **This platform is React 17 + Redux, NOT Next.js.** A separate standalone prototype was Next.js; conflating them turns the most impressive fact about the redesign — modern design shipped into a legacy codebase — into a generic one.
- **"Six months of work in two months" is an estimate with no artifact behind it.** The 7.3-week duration is verified. Use the raw scale instead — 230 files, ~29,400 insertions, 7 weeks.
- **Do not claim a clean "Figma MCP → code pipeline."** That was the plan, not the practice. Claim the screenshot-and-iterate loop; it's accurate and a better story.
- The redesign shipped to the client's internal release channel across a series of tagged releases — "shipped" is fair.
- The platform's later ground-up rebuild was delivered by other engineers after his handoff. Never claim work on it. No user-count figure exists for this product — do not claim one.

---

## Nuts and Bolts AI — Real-Time AI Video Companion

**Client: the same social watch-party / co-viewing platform (name confidential). 2025.**
**Role on this project: sole engineer on the AI workstream.**

The client wanted an AI participant that watches along with a party and comments on the video in chat
at the right moments. **The constraint: Nuts and Bolts had no access to the client's backend**, so the
obvious architecture — a service that ingests the stream and posts to chat — was unavailable.

His solution was to build the agent **inside the existing frontend as middleware in the app's own
state layer**. It observes the same events the UI already observes — video timeline updates, session
creation, incoming chat messages — and when it responds it dispatches through the **exact same path a
human message takes**, so the message renders identically with no special-casing anywhere in the app.
Zero new infrastructure; it reuses the chat already in place. He proposed this architecture himself
rather than being assigned it.

Capabilities delivered: contextual messages fired at exact video timestamps on an interval system that
resets per video; replies that combine the current message, recent conversation history, the video
itself and the timestamp as context; and loop prevention, stale-message filtering and duplicate
suppression. The hard bug of the workstream was **cross-user context sync** — the agent worked for
whoever started the video and silently did nothing for everyone else in the party. The failure mode was
silence, not an error.

Roughly a third of the workstream's code is **observability tooling** he built for the purpose.
Debugging a non-deterministic agent inside a real-time multi-user video app, across browser sessions,
with no backend access, means you cannot reproduce a failure by re-running a request.

**The video-understanding layer** behind it was a separate hybrid, degradation-tolerant pipeline:
Gemini handles video understanding, a scraping service pulls real transcripts, and a metadata API
supplies the rest. Because any given video may have all, some or none of those signals, the analyzer
**selects one of three prompt variants based on which signals actually exist**, rather than failing or
hallucinating around a missing transcript. Packaged explicitly for client handoff with an integration
guide.

### Stack
Gemini 2.5 Flash Lite (multimodal video analysis at timestamps, and chat response generation) ·
middleware inside a React 17 + Redux production app · Python, Gradio, transcript scraping, video
metadata API · Playwright headless bot participants (so a multi-user watch-party agent could be demoed
by one person), Fly.io, Docker · Claude Code.

### Accuracy constraints
- **The agent was built and fully functional with API keys provisioned across all five environments, and its ticket closed Done — but there is no evidence in git that it merged to the public production branch.** Safe verbs: *built, implemented, designed, delivered, demonstrated*. Avoid "deployed to production" for the agent specifically.
- On the earlier standalone prototype (a separate Next.js app), Paolo built **the conversational/agent-behaviour layer only** — 6 of its 97 commits. Frame as "built the conversational layer of a team prototype", never "built the prototype". That prototype used OpenAI's vision model, not Gemini. The shipped in-app agent is the Gemini one, and it's the one worth leading with.
- The video-understanding engine was a research and handoff deliverable, not a production service. Do not claim production deployment or any user count for it.

---

## Nuts and Bolts AI — Affiliate Merchandise Storefront

**Client: a national consumer brand, via a creator-commerce partner (names confidential). August–September 2025, ~7 weeks.**
**Role on this project: full-stack engineer, backend/data owner, and repo maintainer on a 4-engineer team.**

A self-serve onboarding wizard that provisions individual staff members their own hosted merchandise
storefront, on which they earn commission. Staff connect a social account, the backend pulls their
profile and recent posts to populate the storefront, and they select merchandise from a catalog.

Paolo authored ~28% of team commit volume (2nd of 4 engineers) and merged 14 pull requests as repo
maintainer, most authored by teammates. He was the integration point where a long-running
design-driven redesign branch met the backend and data work.

### What he owned
- **The content review and approval pipeline, designed and built end to end.** A national brand's name goes on every page that publishes, and automated moderation wasn't sufficient alone — the client needed a human review gate, and none existed. He built the whole thing: the data model, the admin queue APIs, the reviewer tooling, and access control at the public API boundary so unreviewed storefronts stay private. He also made rejection *granular* — feedback split by dimension, so the failure page shows a user only what actually needed fixing rather than telling them their whole submission failed.
- **Eliminating an image-persistence defect class.** Images were being stored as ephemeral references — including third-party proxy URLs that **expired** — so any storefront that published would silently lose its images days later. A bug with a delayed fuse, invisible at the moment you test it, already patched three times by three people over six weeks. He rebuilt persistence around storage the team controlled, added retry with exponential backoff, and chose **hard failure over silent fallback** so an unreliable URL can never reach the database — then backfilled the guarantee across every write path.
- **A transactional email system from zero to client-ready** — provider abstraction with environment-based selection, startup configuration validation separating hard errors from deliverability warnings, retry with backoff, self-imposed rate limiting, and HTML + plain-text pairs for every template.
- **Six schema migrations against live user data**, including a breaking rename onto an external partner team's data contract that preserved every existing user selection and shipped with an API-layer transform so no coordinated frontend release was needed, and a data-model migration that preserved user-chosen ordering, kept a backup rather than dropping the old column, and shipped verification queries counting failed rows.
- Passwordless magic-link auth with cross-browser session recovery, and slug generation with Unicode normalization so accented names produce stable, permanent URLs.

### Stack
TypeScript, **React 18 + Vite (a client-rendered SPA)**, React Router, TanStack Query, Tailwind,
shadcn/ui on Radix primitives, dnd-kit, react-hook-form + Zod · Node.js on serverless functions ·
Supabase (PostgreSQL, Auth, Storage) · Resend transactional email, a social-profile ingestion API,
Google Cloud Vision SafeSearch (integrated by teammates) · Vercel.

### Accuracy constraints
- **THE BIGGEST CONSTRAINT: this was delivered and handed off, not launched.** Paolo was moved to another project before rollout and cannot confirm a single real end user ever used it. **Safe verbs: built, designed, implemented, delivered, handed off.** Never: launched, went live, in production, serving users, production traffic. If asked whether it shipped, say plainly that he built and delivered it and the client's team owned rollout — a normal consulting outcome.
- **It is React 18 + Vite, NOT Next.js.** Three *other* N&B projects genuinely are Next.js, so an interviewer may probe this one specifically.
- **No error-monitoring tooling exists in this codebase**, and Paolo did not install, configure or deploy monitoring on any N&B project. He *consumed* monitoring as a diagnostic tool elsewhere — correct verbs there are *diagnosed, root-caused, traced*. Never *instrumented, integrated, set up*.
- **"Gamified" is not supported** — no points, levels, leaderboards or streaks exist. The commission economics live on the partner's platform, not in anything he built.
- The automated image-moderation integration was **written by teammates**. He built the *human* review layer downstream of it — "the human review and approval layer of a two-stage moderation system".
- The visual design work was led by another engineer. Paolo's frontend work was **structural** — state architecture, routing, data flow, edit flows, admin UI, storefront and cart.
- **Zero verified users. Do not borrow user figures from other projects.**

---

## Nuts and Bolts AI — AI Content Generation Platform

**Client: a legal-marketing agency serving US law firms (name confidential). June–August 2025, ~9 weeks.**
**Role on this project: full-stack — feature owner for the news→suggestion→digest pipeline, sole author of the self-serve product and the scheduler service, and repo maintainer on the backend.**

**This is the AI/LLM-heaviest project on Paolo's record, and the only one where the product *is* an LLM
pipeline rather than an app that happens to call an LLM.** When a visitor asks about AI/ML engineering,
LLM application work, prompt engineering, or AI evaluation, this is the client project to lead with.

The product: a multi-tenant "content agent" that ingests trending news, ranks it with an LLM for
relevance to the client's audience, suggests blog and newsletter topics, generates the content with
cited sources and an AI image, and emails a curated digest on a schedule. A human review gate sits in
front of every generation step.

### Scale and ownership
- 135 commits across five repositories in ~9 weeks
- **56% of the surviving Python in the production backend**, 90% of the scheduler service, and 97% of the self-serve frontend, by line attribution at HEAD
- Merged 26 of 30 pull requests across the five repos as maintainer
- Authored the suggested-content, daily-digest and auth blueprints — 22 REST endpoints
- 19 sole-authored technical documents

### What he owned
- **The news → suggestion pipeline, end to end.** None of it existed before him: news ingestion against a curated, tiered source allow-list; LLM relevance ranking; structured topic suggestion; persistence, API and UI — plus a 3-agent CrewAI crew for the multi-agent path, with graceful fallback to a single-call tool when the crew returned a malformed shape.
- **Defensive LLM output validation.** Ranking dozens of articles in a single call, the model would silently drop items — send 40, get 32 back. He stated the required count several ways in the prompt and echoed back the full expected ID set, then deliberately *didn't trust it*: the code diffs returned IDs against expected and appends anything missing with an explicit "missed by model" reason. The principle — a prompt is a request, not a guarantee, so anything you actually need is checked in code — recurs throughout his work.
- **A historical back-testing harness for non-deterministic AI output. This is the standout engineering story in his whole record.** Quality complaints about the digest were impossible to debug: you got one sample per day, and the input (the news itself) changed daily, so a complaint was unreproducible by definition. He threaded a simulated-date parameter through the news tool so it computes its publication window relative to a chosen date, then wrote an 870-line harness that replays both pipeline stages independently for each of the last seven days and measures **day-over-day article overlap** — the direct numeric proxy for the client's actual requirement that no two digests repeat. The committed result files show it was run against the real pipeline rather than written and shelved.
### Accuracy constraints (part 1)
- **The backend is Flask, NOT FastAPI.** There is no FastAPI anywhere in any of the five repositories. Stating FastAPI would be caught in any technical screen.
- **The frontends are React 18 / Create React App, NOT Next.js.** Everything deployed on **Replit, NOT Vercel**.
- **He did NOT build the CrewAI blog-generation platform.** It was architected by another engineer four months before he joined; Paolo authored one of its six crews. Correct framing: he built the news-ingestion and content-suggestion pipeline, including a 3-agent crew, *inside an existing CrewAI-based platform*.

---

## Nuts and Bolts AI — AI Content Generation Platform (Scheduling, Governance & Self-Serve)

**Client: the same legal-marketing platform (name confidential). June–August 2025.**
Continues from the AI content platform section above — same engagement, same nine weeks.

- **An unattended scheduled service.** A standalone APScheduler service with cron triggers pinned to a timezone so the schedule survives DST; per-user opt-in evaluation before generating; per-run audit logging; duplicate suppression tracking what each user had already been sent; and a health-check HTTP server so run history was inspectable without database access. Plus the digest email layer — responsive HTML templating and per-recipient send with partial-failure tolerance, so one bad address doesn't abort the batch.
- **Retrieval-source governance, three layers deep.** The client sells marketing services to law firms, so a generated article citing a competitor firm is worse than no article. Layer 1 injects source constraints into the research prompts so bad sources are never retrieved. Layer 2 uses a small reasoning model to extract blacklist rules out of the user's free-text instructions, so "don't cite other law firms" becomes a real constraint with zero frontend changes. Layer 3 is a cost-tiered removal cascade that only spends an API call after cheap URL and title pattern checks fail, with per-domain caching. Then the part everyone gets wrong: deleting a citation means renumbering the survivors *and* every in-text reference.
- **Converting the product from manual per-client redeployment into a self-serve multi-tenant SaaS** — sole author of the React application and of the backend JWT auth layer, including an identity-mapping layer between the auth provider's UUIDs and the existing integer user column. He wrote up three options with tradeoffs, chose mapping as the only one with zero blast radius on three live deployments, and shipped it on both ends of the stack.
- **Root-caused and fixed a production authentication hang** — unbounded async auth calls with no timeouts, racing against the auth-state listener. He added timeout guards on every async path, race protection, and graceful degradation so every failure path lands in a usable state. He had shipped an "emergency recovery" button while diagnosing, then deleted it once the root cause was fixed.
- **A six-week generative-quality feedback loop.** The client read each morning's AI-generated newsletter and filed a ticket about what was wrong with it; each became a prompt, model or retrieval change shipped within days. The fix that mattered most wasn't a bigger model — it was pasting three newsletters the client had written themselves into the prompt as few-shot exemplars, because a house voice is a rhythm you can't describe in the abstract but a model will copy on sight. He also added word-count validation with automatic regeneration when output missed target, and provider fallback when the primary image model hit an org-permissions failure.
- A per-stage LLM cost breakdown for the client, and Langfuse tracing with deliberately chosen custom generation metadata on the pipelines he built.

### Stack
**Python 3.10–3.12, Flask 3.x** (9 blueprints), Gunicorn, threaded async job processing, `uv` ·
**React 18 / Create React App**, React Router v6, Context API, error boundaries · PostgreSQL via
Supabase (schema design, JSONB settings modeling, multi-tenant row filtering), Supabase Auth (JWT) ·
**OpenAI** (GPT-4.1 / 4o / 4.1-mini / o1-mini / o3-mini / gpt-image-1, with deliberate per-task model
selection), **Perplexity** (sonar family, grounded research with citations), **Replicate / FLUX** image
fallback, **CrewAI**, **Langfuse + OpenLIT** tracing · APScheduler, SMTP/MIME email · Replit.

### Accuracy constraints — this entry previously carried four stack-level errors
- **The backend is Flask, NOT FastAPI.** There is no FastAPI anywhere in any of the five repositories. Stating FastAPI would be caught in any technical screen.
- **The frontends are React 18 / Create React App, NOT Next.js.** No SSR, no app or pages router.
- **Everything deployed on Replit, NOT Vercel.**
- **He did NOT build the automated fact-verification.** The verification crew and claim-extraction functions were written by another engineer before he joined. Never claim fact-verification as his work. What IS his: citation and footnote integrity, and fixing link-preservation defects in the verification prompts.
- **He did NOT build the CrewAI blog-generation platform.** It was architected by another engineer four months before he joined; Paolo authored one of its six crews. Correct framing: he built the news-ingestion and content-suggestion pipeline, including a 3-agent crew, *inside an existing CrewAI-based platform*. Never claim authorship of the platform itself.
- **There is no claim-validation eval harness on this project.** Do not use the word "evals" for it. What exists is the back-testing harness covering news selection and digest generation — a better story anyway.
- **No user, engagement, revenue or time-saved numbers exist.** Three client deployments plus an internal instance and the self-serve app is the ceiling, and that is a *deployment* count, not a user count.
- **Built, deployed and handed back — not confirmed to have reached the client's own audience.** The scheduled digest demonstrably ran and produced output the client reviewed daily, but the confirmed recipients were the consultancy's own staff, for testing. Safe verbs: *built, designed, shipped, deployed*. Never: *served, drove, delivered to customers, in production for the client*.
- The per-post cost figure originated with another engineer. Paolo performed the per-stage breakdown — claim the breakdown, not a cost reduction.

---

## Stratpoint Technologies
**AI Engineer - Rapid Prototyping Unit**
**July 2023 to July 2024**

Worked in the AI labs team at a software outsourcing company on a confidential client research engagement. [NDA: the client, its industry, the application domain, datasets, specific algorithms, and detailed results are NOT shareable publicly. Stick to the generic summary below; if asked for specifics, say it's under NDA and direct the visitor to email Paolo at pjsandejas@gmail.com.]

### ML Screening Tasks (Confidential)
Completed ML screening tasks that secured a major client research partnership.

- Predictive modeling and computer-vision feature-matching pipelines
- Achieved >95% model accuracy
- Stack: Python, scikit-learn, pandas, AWS SageMaker, OpenCV, Jupyter Notebook

### Research-Paper Chat Assistant
First main project after securing the partnership.

- Chat assistant allowing researchers to query a specific area of research
- Connected to Semantic Scholar API to pull relevant academic papers
- Full-paper context feeding into Gemini proved more effective than vector DB retrieval for the paper sizes involved
- Stack: Gemini API, LangChain, ReAct framework | Deployed to Hugging Face Spaces

### Team Scaling
Team grew from 4 to 13 engineers during tenure. Established ML best practices through code reviews and technical documentation.

---

## Kodexa
**Associate Product Manager (worked more as a Software Engineer in practice)**
**~2022 – 2023 · part-time while finishing BS at University of the Philippines**

Kodexa focused on transforming unstructured data (receipts, meter readings, invoices) into structured data.

- Built a Snowflake data connector in Java, referencing existing S3 and Azure connectors
- Trained approximately 150 invoice vendor formats for an OCR document parsing model using regex-based annotation scripts (project involved several thousand vendor invoice formats total)
- Built Apache Superset dashboards to visualize invoice training progress for a large enterprise client — critical for maintaining client transparency on a multi-thousand-vendor project
