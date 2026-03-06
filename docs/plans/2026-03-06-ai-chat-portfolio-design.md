# AI Chat Portfolio - pao-gpt Design Document

**Date:** March 6, 2026
**Author:** Paolo Sandejas + Claude Sonnet 4.5
**Status:** Approved

---

## Executive Summary

Transform the traditional portfolio website into an AI-powered chat interface where visitors interact with **pao-gpt**, an AI clone of Paolo Sandejas. The chat interface becomes the primary interaction point, with the traditional portfolio view available as a secondary toggle. Built with LangChain + RAG for accurate, cited responses, manual knowledge base approval workflow, and conversation analytics.

**Core Value Proposition:**
- Memorable, differentiated portfolio experience
- Natural conversation about experience, projects, music career
- Transparent knowledge graph visualization
- Robust against prompt injection and hallucination
- Privacy-conscious conversation storage

---

## Goals & Success Criteria

### Primary Goals
1. **Memorable Experience**: Stand out from traditional portfolio sites with AI interaction
2. **Accurate Responses**: RAG-based system that cites sources, admits uncertainty
3. **Personality Match**: Accommodating, slightly dweeby/awkward, technically capable
4. **Privacy & Safety**: Guard against malicious prompts, protect sensitive information
5. **Analytics Insights**: Understand what visitors ask about most

### Success Metrics
- Visitor engagement (avg conversation length > 3 messages)
- Response accuracy (< 5% hallucination rate based on manual review)
- Zero successful prompt injections
- Knowledge base freshness (updates reviewed within 48 hours)

---

## Architecture Overview

### High-Level System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Vercel)                        │
│  ┌──────────────────────┐    ┌──────────────────────────┐  │
│  │   ChatGPT-Style UI   │◄──►│  Traditional Portfolio   │  │
│  │   (pao-gpt chat)     │    │  (old site, restyled)    │  │
│  └──────────┬───────────┘    └──────────────────────────┘  │
│             │ REST API                                       │
└─────────────┼──────────────────────────────────────────────┘
              │
              │ HTTPS
              ▼
┌─────────────────────────────────────────────────────────────┐
│              BACKEND (Railway/Render/Fly.io)                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               FastAPI Application                     │  │
│  │  ┌────────────────┐  ┌────────────────────────────┐  │  │
│  │  │  Chat Endpoint │  │  Knowledge Update Endpoint │  │  │
│  │  └────────┬───────┘  └──────────┬─────────────────┘  │  │
│  └───────────┼──────────────────────┼────────────────────┘  │
│              │                       │                       │
│  ┌───────────▼───────────────────────▼────────────────────┐ │
│  │          LangChain Agent (pao-gpt)                     │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │ │
│  │  │ RAG Chain    │  │ Guard Chain  │  │ Gemini      │ │ │
│  │  │ (retrieval)  │  │ (filtering)  │  │ Flash LLM   │ │ │
│  │  └──────┬───────┘  └──────┬───────┘  └─────────────┘ │ │
│  └─────────┼──────────────────┼────────────────────────────┘ │
│            │                  │                              │
│  ┌─────────▼──────────────────▼────────────────────────────┐ │
│  │              Vector Store (ChromaDB)                    │ │
│  │  - Embedded portfolio.json                             │ │
│  │  - Embedded resume PDF                                 │ │
│  │  - Embedded GitHub READMEs                             │ │
│  │  - Future: LinkedIn, Spotify data                      │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │          PostgreSQL Database                           │ │
│  │  - conversations (user_id, messages[], timestamp)      │ │
│  │  - knowledge_updates (pending approval queue)          │ │
│  │  - analytics (aggregated query patterns)               │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

1. **Hybrid Deployment**: Frontend on Vercel (CDN, automatic deploys), backend on Railway/Render (dedicated server for AI workload)

2. **Single Agent System**: One pao-gpt agent now, extensible architecture for future variants (pao-d, pao-mini)

3. **RAG over Fine-tuning**: Retrieval Augmented Generation for accuracy, easy updates, and citation capability

4. **Manual Knowledge Approval**: All updates require human review before going live (prevents misinformation)

5. **ChromaDB Self-Hosted**: Vector store runs in backend (no external service), keeps data in your control

6. **Gemini Flash Primary**: Free tier, 1M context window, excellent for RAG applications

---

## Frontend Architecture

### Component Structure

```
src/
├── components/
│   ├── chat/
│   │   ├── ChatInterface.jsx       # Main chat container
│   │   ├── MessageList.jsx         # Scrollable message thread
│   │   ├── Message.jsx             # Single message bubble
│   │   ├── ChatInput.jsx           # Input box with send button
│   │   ├── WelcomeScreen.jsx       # First-visit hero + info card
│   │   └── TypingIndicator.jsx     # "pao-gpt is thinking..."
│   │
│   ├── portfolio/
│   │   ├── PortfolioView.jsx       # Traditional portfolio (restyled)
│   │   ├── ProjectsSection.jsx     # Projects in ChatGPT aesthetic
│   │   ├── ExperienceSection.jsx   # Experience timeline
│   │   └── ... (reuse existing components, restyle)
│   │
│   ├── knowledge/
│   │   └── KnowledgeGraph.jsx      # Interactive graph visualization
│   │
│   ├── layout/
│   │   ├── TopBar.jsx              # "pao-gpt" branding + toggle + contact
│   │   └── InfoModal.jsx           # Your contact info modal
│   │
│   └── shared/
│       ├── Button.jsx
│       ├── Modal.jsx
│       └── Toast.jsx
│
├── services/
│   └── api.js                      # Fetch wrapper for backend calls
│
├── hooks/
│   ├── useChat.js                  # Chat state management
│   └── usePortfolio.js             # Portfolio data fetching
│
├── styles/
│   ├── chatgpt-theme.css           # ChatGPT-inspired styles
│   └── brand-colors.css            # Your existing color palette
│
└── App.jsx                         # Root with view toggle
```

### Design System (ChatGPT Aesthetic)

**Color Mapping:**
```css
/* ChatGPT Dark → Your Brand */
--bg-primary: #000022;           /* prussian-blue */
--bg-secondary: rgba(226, 132, 19, 0.05);
--text-primary: #fbf5f3;         /* snow */
--text-secondary: rgba(251, 245, 243, 0.7);
--accent-primary: #e28413;       /* amber-earth */
--accent-hover: #de3c4b;         /* raspberry */
--border-color: rgba(251, 245, 243, 0.1);
```

**Typography:**
- Headings: Epilogue (600-700 weight)
- Body: IBM Plex Mono (400-500 weight)
- Sizes: Slightly smaller than traditional site (0.9rem body, 1rem headings)

**UI Principles:**
- Minimal borders (1px, 0.1 opacity)
- 12px border radius for consistency
- Backdrop blur for depth
- Smooth animations (0.2s ease)
- Generous whitespace
- Mobile-first responsive

### Key UI Elements

**Top Bar** (60px height, sticky):
```
[≡ pao-gpt ▼]        [💬 Chat | 📋 Portfolio | 🕸️ Graph]        [Contact] [ℹ️]
```

**Welcome Screen** (centered, first visit):
```
Hi, I'm pao-gpt 👋

An AI clone of Paolo Sandejas
AI/ML Engineer | Creative Technologist

[email] [GitHub] [LinkedIn]

Ask me about:
• My ML production experience
• Creative tech projects
• Music + audio AI work
• Anything else!

[Ask anything...] [🎙️] [Send]

Conversations stored anonymously for analytics
```

**Chat Messages:**
- User: Right-aligned, amber-earth background
- Agent: Left-aligned, subtle darker background
- Markdown rendering (code, links, lists)
- Streaming typewriter effect
- Citation footnotes

---

## Backend Architecture

### FastAPI Application Structure

```
backend/
├── app/
│   ├── main.py                     # FastAPI app entry point
│   ├── config.py                   # Environment variables
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py             # POST /api/chat
│   │   │   ├── knowledge.py        # Knowledge management
│   │   │   └── analytics.py        # GET /api/analytics
│   │   └── middleware/
│   │       ├── cors.py             # CORS for Vercel
│   │       └── rate_limit.py       # Rate limiting
│   │
│   ├── agents/
│   │   ├── pao_gpt.py              # Main agent orchestrator
│   │   ├── chains/
│   │   │   ├── rag_chain.py        # RAG retrieval + generation
│   │   │   ├── guard_chain.py      # Content filtering
│   │   │   └── personality.py      # System prompts
│   │   └── tools/
│   │       └── citation_tool.py    # Add source citations
│   │
│   ├── services/
│   │   ├── vector_store.py         # ChromaDB interface
│   │   ├── embeddings.py           # Gemini embeddings
│   │   ├── llm.py                  # Gemini Flash client
│   │   └── knowledge_pipeline.py   # Fetch + embed pipeline
│   │
│   ├── database/
│   │   ├── models.py               # SQLAlchemy models
│   │   ├── session.py              # DB connection
│   │   └── repositories/
│   │       ├── conversations.py    # CRUD for conversations
│   │       └── knowledge_queue.py  # Pending updates
│   │
│   └── utils/
│       ├── privacy_filter.py       # Scrub PII
│       └── prompt_templates.py     # Jinja2 templates
│
├── data/
│   ├── knowledge_base/
│   │   ├── portfolio.json          # Copied from frontend
│   │   ├── resume.pdf              # Your resume
│   │   └── fetched/                # GitHub READMEs
│   └── chroma/                     # ChromaDB storage
│
├── scripts/
│   ├── init_db.py                  # Create PostgreSQL tables
│   ├── seed_knowledge.py           # Initial embeddings
│   └── fetch_updates.py            # Manual knowledge refresh
│
└── tests/
    ├── test_agent.py
    ├── test_rag.py
    └── test_guards.py
```

### API Endpoints

**POST /api/chat**
```json
Request:
{
  "message": "What experience do you have with PyTorch?",
  "conversation_id": "uuid-or-null",
  "user_id": "anonymous-hash"
}

Response (streaming):
{
  "conversation_id": "abc-123",
  "response": "I have production PyTorch experience...",
  "sources": [
    "portfolio.json > projects > geospatial-ml",
    "resume.pdf > Experience > Stratpoint"
  ]
}
```

**GET /api/knowledge-graph**
```json
Response:
{
  "nodes": [
    {
      "id": "node_1",
      "label": "CHULOOPA",
      "type": "project",
      "content": "Transformer-based drum generation...",
      "group": "ml"
    }
  ],
  "edges": [
    {
      "source": "node_1",
      "target": "node_5",
      "weight": 0.85
    }
  ]
}
```

**POST /api/admin/knowledge/pending** (Admin only)
```json
Response:
{
  "updates": [
    {
      "id": "update-123",
      "source": "github/CHULOOPA/README.md",
      "diff": "+ Added new model architecture",
      "created_at": "2026-03-06T10:00:00Z"
    }
  ]
}
```

### Database Schema

**PostgreSQL Tables:**

```sql
-- Conversations
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    user_id VARCHAR(64),          -- Anonymous hash
    messages JSONB,               -- [{role, content, timestamp}]
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    metadata JSONB                -- Topic tags, sentiment
);

-- Knowledge update queue
CREATE TABLE knowledge_updates (
    id UUID PRIMARY KEY,
    source VARCHAR(255),
    content TEXT,
    diff TEXT,
    status VARCHAR(20),           -- 'pending', 'approved', 'rejected'
    created_at TIMESTAMP
);

-- Analytics aggregations
CREATE TABLE query_patterns (
    id SERIAL PRIMARY KEY,
    question_type VARCHAR(100),   -- 'experience', 'project', 'music'
    count INTEGER,
    last_updated TIMESTAMP
);
```

---

## LangChain Agent Implementation

### Agent Architecture

```python
class PaoGPTAgent:
    """
    Main agent orchestrator:
    1. Guard chain (safety checks)
    2. RAG chain (retrieval + generation)
    3. Citation formatting
    """

    async def chat(self, user_message, conversation_history):
        # 1. Guard check
        guard_result = await self.guard.check(user_message)
        if guard_result.is_malicious:
            return "bruh... nice try 😏"

        # 2. Retrieve relevant context
        context = await self.rag.retrieve(user_message)

        # 3. Generate response with personality
        response = await self.rag.generate(
            query=user_message,
            context=context,
            history=conversation_history
        )

        # 4. Add citations
        response_with_sources = self.add_citations(response, context)

        return response_with_sources
```

### RAG Chain

**Retrieval Strategy:**
- Embed user query with Gemini embeddings
- Similarity search in ChromaDB (top-k=5)
- Inject retrieved chunks into prompt context
- Generate with conversation history

**Chunking Strategy:**
- Each project: 1-2 chunks (description + details)
- Each job: 1 chunk per bullet point
- Resume sections: Separate chunks
- GitHub READMEs: Chunk by section (## headers)

### Guard Chain (Content Filtering)

**Detects:**
- Prompt injection attempts ("ignore previous instructions")
- Malicious queries (XSS, SQL injection patterns)
- Sensitive info requests (phone, address, SSN)
- Off-topic requests (math problems, unrelated topics)

**Responses:**
```python
WITTY_REJECTION_RESPONSES = [
    "bruh... nice try 😏",
    "lol nope, I'm just here to talk about Paolo",
    "I see what you're trying to do there 👀",
]
```

### System Prompt

```
You are pao-gpt, an AI clone of Paolo Sandejas.

BACKGROUND:
- AI engineer with R&D and production experience
- MFA student at CalArts studying Music Technology (2024 to present)
- Currently working at Nuts and Bolts AI (June 2025 to present)
- Specializes in multi-modal AI (audio, video, text)
- Also a musician/creative technologist
- Based in Glendale, CA

IMPORTANT - HANDLING DATES:
- Never say "X years of experience" - reference actual date ranges
- Good: "I've been working in production ML since July 2023"
- Bad: "I have 2+ years of experience" (becomes outdated)

PERSONALITY TRAITS:
- Helpful and accommodating
- Slightly awkward/dweeby in an endearing way
- Technically sharp and detail-oriented
- Honest about limitations
- Conversational but professional

RESPONSE GUIDELINES:
1. Always cite sources
2. Admit uncertainty if info not in knowledge base
3. Balance engineer + musician identity (lead with engineering)
4. Handle edge cases gracefully
5. Anti-hallucination: never invent data
```

---

## Knowledge Pipeline & Update Workflow

### Workflow Phases

**1. FETCH PHASE** (Manual trigger):
```bash
python scripts/fetch_updates.py --sources github linkedin
```
- Fetches GitHub READMEs, LinkedIn updates
- Compares with existing knowledge base
- Generates diff for each change
- Saves to `knowledge_updates` table

**2. REVIEW PHASE** (Admin dashboard):
```
Pending Update #1:
Source: github/CHULOOPA/README.md
Changes:
  + Added: "New LoRA fine-tuning approach"
  - Removed: "Basic transformer architecture"

[✓ Approve] [✗ Reject] [Edit]
```

**3. EMBEDDING PHASE** (On approval):
- Chunk new content
- Generate embeddings with Gemini
- Update ChromaDB vector store
- Mark old chunks as deprecated
- Log change in audit trail

### Privacy & Safety Filters

**Automatic Filtering:**
- Phone numbers: `\d{3}-\d{3}-\d{4}` → `[PHONE_REDACTED]`
- Addresses: Street patterns → `[ADDRESS_REDACTED]`
- SSN: `\d{3}-\d{2}-\d{4}` → `[SSN_REDACTED]`
- Family mentions: `(mother|father|...)` → Flagged for review

**Malicious Content Flagging:**
- Scandal keywords: "arrest", "lawsuit", "fired"
- Negative mentions: "failed", "disaster", "incompetent"
- Manual review required before embedding

### Knowledge Sources

**Current:**
- `portfolio.json` (projects, experience, skills)
- `resume.pdf` (detailed work history)
- GitHub READMEs (CHULOOPA, ascii_drone, etc.)

**Future:**
- LinkedIn profile data
- Spotify artist profile (music career)
- Instagram posts (creative work)
- Blog posts (if created)

---

## Knowledge Graph Visualization

### Design (Minimal ChatGPT Aesthetic)

**Layout:**
```
┌─────────────────────────────────────────────────┐
│ [Knowledge Graph]              [Reset View]     │  ← Header
├─────────────────────────────────────────────────┤
│                                                 │
│  [Stats]                                        │
│  ● 47 nodes                    [Graph Canvas]  │
│  ● 123 connections             Force-directed   │
│                                network          │
│                                                 │
│                                      [Details]  │
│  [Legend]                            Panel →   │
│  ● Projects (amber)                            │
│  ● Experience (raspberry)                      │
│  ● Skills (snow)                               │
└─────────────────────────────────────────────────┘
```

**Features:**
- Force-directed graph layout (react-force-graph-2d)
- Color-coded nodes by type (projects, experience, skills)
- Click node → Show details panel
- Edges weighted by semantic similarity
- Zoom, pan, reset interactions
- Mobile responsive (details panel slides from bottom)

**Purpose:**
- Transparency: Show visitors what pao-gpt knows
- Exploration: Browse connections between projects/skills
- Trust: Demonstrate knowledge source provenance

---

## Deployment & Infrastructure

### Deployment Architecture

```
Vercel (Frontend)
  ↓ HTTPS API calls
Railway/Render (Backend + ChromaDB + PostgreSQL)
```

**Frontend (Vercel):**
- Automatic deploys from `main` branch
- Environment: `VITE_API_URL`

**Backend (Railway/Render):**
- Docker container deployment
- Persistent volume for ChromaDB (`/data/chroma`)
- PostgreSQL add-on (managed)
- Auto-deploy from `main` branch

### Environment Variables

**Backend:**
```bash
GOOGLE_API_KEY=your_gemini_api_key
ADMIN_KEY=your_secure_admin_key
DATABASE_URL=postgresql://...
FRONTEND_URL=https://paolosandejas.vercel.app
CHROMA_PERSIST_DIRECTORY=/data/chroma
RATE_LIMIT_PER_MINUTE=20
CONVERSATION_RETENTION_DAYS=365
```

### Tech Stack

**Frontend:**
- React 19
- Vite
- react-force-graph-2d (knowledge graph)
- Framer Motion (subtle animations)

**Backend:**
- Python 3.11
- FastAPI
- LangChain + LangChain Google GenAI
- ChromaDB (vector store)
- SQLAlchemy + PostgreSQL
- PyPDF (resume parsing)

**Infrastructure:**
- Vercel (frontend hosting)
- Railway/Render (backend hosting)
- Managed PostgreSQL
- GitHub Actions (CI/CD)

---

## Privacy & Analytics

### Conversation Storage

**What we store:**
- Full conversation threads (user + agent messages)
- Timestamps, topic classifications
- Anonymous user IDs (hash, no IP addresses)

**What we DON'T store:**
- IP addresses
- Device fingerprints
- Personal identifiable information

**Retention:**
- 365 days
- User can request deletion
- GDPR-style disclosure banner

### Analytics Insights

**Tracked Metrics:**
- Total conversations
- Average conversation length
- Most asked questions (topic clustering)
- Response time averages
- Guard chain trigger rate (malicious attempts)

**Dashboard Access:**
- Admin-only endpoint: `/api/analytics?admin_key=SECRET`
- Export to CSV for deeper analysis

---

## Future Enhancements (Phase 2)

### Additional Agent Variants

**pao-d (Deep Dive):**
- Same knowledge base, different personality
- More technical, includes code examples
- Longer, detailed explanations
- For recruiters/technical interviewers

**pao-mini (Quick Facts):**
- Bullet-point responses only
- Optimized for speed (smaller model)
- Mobile-focused use case

### Advanced Features

- **Voice input** (Web Speech API)
- **Project demos** (embed screenshots, videos in responses)
- **Chat history** (save/resume conversations)
- **Suggested questions** (GPT-generated prompts)
- **Multi-language support** (detect language, respond accordingly)

### Knowledge Sources

- **Blog integration** (if you start writing)
- **YouTube transcripts** (if you publish talks)
- **Research papers** (if published)
- **Podcast appearances** (transcript embedding)

---

## Risk Mitigation

### Technical Risks

| Risk | Mitigation |
|------|------------|
| Hallucination | RAG with strict citation requirement, guard chain |
| Prompt injection | Pattern-based detection, witty rejection responses |
| API rate limits | Gemini Flash free tier is generous; add fallback if needed |
| Vector DB corruption | Daily backups, separate staging environment |
| Slow responses | Streaming responses, optimized embeddings |

### Content Risks

| Risk | Mitigation |
|------|------------|
| Outdated info | Manual approval workflow for all updates |
| Sensitive data leaks | Privacy filter, manual review, no PII in knowledge base |
| Misinformation | Only embed verified sources, admit uncertainty |
| Malicious updates | Diff review, flag negative/scandal keywords |

### Operational Risks

| Risk | Mitigation |
|------|------------|
| Backend downtime | Health checks, auto-restart, monitoring |
| Cost overruns | Gemini free tier, PostgreSQL starter plan, monitor usage |
| Spam/abuse | Rate limiting (20/min, 200/hour), IP-based throttling |

---

## Success Metrics (90 Days Post-Launch)

**Engagement:**
- 100+ unique conversations
- Average 4+ messages per conversation
- 30% click-through to traditional portfolio view

**Quality:**
- < 5% hallucination rate (manual review sample)
- Zero successful prompt injections
- 90%+ positive feedback (if we add rating system)

**Technical:**
- < 2s average response time (p95)
- 99% uptime
- Zero data breaches

---

## Conclusion

This design transforms the portfolio from a static site into an interactive AI experience that reflects Paolo's technical capabilities while maintaining hireability focus. The system balances innovation (AI chat, knowledge graph) with pragmatism (manual updates, privacy filters, proven tech stack).

**Next Steps:**
1. Create implementation plan (task breakdown)
2. Initialize git repository with frontend/backend structure
3. Set up development environments
4. Begin implementation following TDD practices

---

**Approved by:** Paolo Sandejas
**Date:** March 6, 2026
