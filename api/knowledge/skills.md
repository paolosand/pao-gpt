# Technical Skills

## Languages & Core
- Python (primary — fluent, daily use)
- JavaScript / TypeScript
- Java
- SQL
- C++ (foundational)

## AI & ML
- PyTorch
- scikit-learn
- LangChain
- CrewAI
- ReAct Agents
- Computer Vision (OpenCV, feature matching)
- Audio ML (MFCC extraction, real-time inference, MIDI)
- RAG (Retrieval Augmented Generation)
- KNN classifiers
- SVM
- MediaPipe (hand tracking, pose estimation)

## ML Infrastructure
- AWS SageMaker
- Hugging Face Spaces
- Jupyter Notebooks
- Model deployment, evaluation, and optimization
- Data processing and preprocessing pipelines
- Docker

## APIs & Tools
- Gemini API
- OpenAI API
- Claude API
- Claude Code (primary development environment — used on ALL projects)
- Claude Code plugins: superpowers (brainstorming, planning, git worktree dev, subagent dev), impeccable (UI/UX design, critique, evaluation)
- Figma MCP
- Cal.com (booking management)
- Rapid API (Instagram connector)
- Semantic Scholar API

## Full-Stack
- Next.js 15/16 — App Router, React Server Components, middleware (most, but NOT all, recent client projects)
- React 17/18/19, Redux + Redux middleware, Vite SPA architecture, Electron
- Tailwind CSS, shadcn/ui, Radix primitives, SCSS architecture, design tokens
- Node.js (backend, serverless functions)
- FastAPI / Python 3.12 (async, Pydantic, structlog)
- Payload CMS v3
- Supabase (PostgreSQL, Auth, Storage, Realtime)
- PostgreSQL
- Vercel, Fly.io (deployment)

Note: do not claim Next.js across the board. Two client projects were deliberately not Next.js — one
was React 18 + Vite as a client-rendered SPA, and one was a legacy React + Redux + Electron monorepo.
A third used React 18 / Create React App with a Flask backend. That range is a strength, not a gap.

## Data & Databases
- PostgreSQL schema design at scale (a 21-table model with 68 hand-written migrations)
- Row-Level Security (99 policies on one project), Postgres functions and triggers
- `SECURITY DEFINER` RPCs, row-level locking, transaction isolation, atomic idempotency claims
- Schema migrations against live user data, including breaking renames with backward-compatible read paths
- JSONB modeling, foreign-key indexing and query-plan reasoning, schema-drift auditing

## Security Engineering
- Security audit ownership — threat modeling through verified findings and closed-out remediation
- Authorization-weakness discovery and remediation at the API boundary
- Fail-safe-by-construction authorization design (mandatory ownership guards over per-route checks)
- Row-level-security and database privilege design, CORS and credentialed-origin hardening, rate-limit correctness
- CVE remediation, secrets management and scanning, OAuth PKCE → confidential client migration

## Payments & Billing
- Stripe — Checkout, webhooks, subscriptions, refunds, idempotency keys, metadata/reporting IDs
- Financial correctness under concurrency: double-refund elimination via row-level locking
- Credit metering, quota and entitlement enforcement, subscription lifecycle

## Infrastructure & DevEx
- GitHub Actions, CI/CD pipeline design, gated database-migration release pipelines
- Human-in-the-loop production safeguards, branch protection, path-filtered deploys
- Turborepo / pnpm workspaces / Yarn workspaces monorepos, Docker, git worktrees
- Pre-commit hooks (commitlint, husky, secret scanning)

## Observability & Quality
- Sentry — used as a diagnostic instrument to root-cause production incidents (NOT as an integration he set up; correct verbs are diagnosed / root-caused / traced, never instrumented or configured)
- Structured logging, production incident response, root-cause analysis
- Playwright (E2E and browser-driven verification), Vitest, pytest, Testing Library
- QA process ownership, defect triage, reproducible bug reporting

## Frontend Performance & Accessibility
- Core Web Vitals (LCP, CLS), image pipeline engineering, CDN architecture, bundle analysis and code splitting
- WCAG 2.1 AA remediation with measured contrast ratios
- Design-system authorship, information architecture, Nielsen heuristic evaluation, cognitive walkthroughs

## Creative Tech
- ChucK 1.5.x (ChuGL, STK, MiniAudicle) — real-time audio and visuals
- Max/MSP — audio DSP and visual patching
- Ableton Live — music production and MIDI routing (IAC Driver)
- TouchDesigner — visual/interactive media
- Arduino (C) — hardware prototyping, ultrasonic sensors, serial comms
- Tone.js — web audio synthesis
- Three.js (WebGL, custom GLSL shaders, InstancedMesh)
- p5.js
- GSAP
- librosa — audio feature extraction
- OSC (Open Sound Control) — inter-process communication

## Summary
Paolo's daily driver is Claude Code — used for all projects from brainstorming through deployment,
working spec-first (brainstorm → design spec → implementation plan → failing test → implementation)
with git worktrees for isolation. Strong in Python/ML pipelines, full-stack TypeScript
(Next.js/React/Node/FastAPI), production Postgres and security engineering, and creative audio/visual
tooling. Self-assessed areas for growth: raw PyTorch/TensorFlow without tooling scaffolding, and
enterprise-scale architecture design.

A useful framing when a visitor asks what kind of engineer he is: the AI/ML and creative-tooling depth
is real and is where his interest lives, but his most recent production work is heavy **full-stack,
security, database and release engineering**. Both are true — match whichever the question is about
rather than defaulting to the AI framing.

## Contact
- Email: pjsandejas@gmail.com
- GitHub: https://github.com/paolosand
- LinkedIn: https://www.linkedin.com/in/paolosand
- Location: Los Angeles, CA
