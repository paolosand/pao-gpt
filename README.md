# Paolo Sandejas - Portfolio Website

A distinctive, production-grade portfolio website showcasing AI/ML engineering expertise with creative technical applications.

## Design Philosophy

**Technical Precision Meets Creative Energy**

This portfolio combines modern brutalism with energetic accents, featuring:
- Bold color palette (prussian blue, amber earth, raspberry, cherry)
- IBM Plex Mono + Epilogue typography for technical credibility
- Geometric layouts with unexpected energy
- Smooth animations via Framer Motion
- Optional interactive p5.js maze exploration

## Features

### Core Portfolio
- **Landing Page**: Clear value proposition with immediate hireability focus
- **Projects Grid**: Filterable showcase of ML and creative tech work
- **Skills**: Technical stack organized by category
- **Experience**: Timeline of production ML work
- **Education**: Academic background with research focus
- **Contact**: Multiple connection points
- **AI Chat (pao-gpt)**: Interactive chatbot clone powered by RAG and Google Gemini

### Interactive Maze (Coming Soon)
- Top-down dungeon-style navigation
- Rooms representing different projects and experiences
- p5.js canvas rendering with GSAP animations
- Minimap and quick navigation options

## Tech Stack

### Frontend
- **Framework**: React + Vite
- **Animation**: Framer Motion
- **Graphics**: p5.js (for maze)
- **Styling**: Custom CSS with design system
- **Hosting**: Vercel/Netlify ready

### Backend (pao-gpt)
- **Framework**: FastAPI + Uvicorn
- **AI/LLM**: LangChain + Google Gemini
- **Vector Store**: ChromaDB (RAG knowledge base)
- **Database**: PostgreSQL + SQLAlchemy
- **Rate Limiting**: SlowAPI
- **Testing**: pytest + pytest-asyncio

## pao-gpt: AI Clone Chat Backend

An intelligent chatbot that acts as Paolo's digital clone, answering questions about his background, projects, and expertise using RAG (Retrieval-Augmented Generation).

### Features

**Safety-First Architecture**
- Guard chain validates incoming messages for malicious content
- Response filtering prevents sensitive information leakage
- Rate limiting (configurable per minute)

**RAG-Powered Responses**
- ChromaDB vector store for knowledge base
- Full-context retrieval for accurate answers
- Google Gemini for generation
- Personality-driven responses matching Paolo's tone

**Conversation Management**
- PostgreSQL storage for conversation history
- Multi-turn conversation support
- Optional conversation persistence (configurable)

### API Endpoints

```
POST /api/chat
- Send message to pao-gpt
- Rate limited (default: 10/minute)
- Returns response with conversation_id

GET /health
- Health check endpoint

GET /
- API status
```

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your GOOGLE_API_KEY and other settings

# Initialize database
python scripts/init_db.py

# Seed knowledge base
python scripts/seed_knowledge.py

# Run development server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest
```

### Configuration

Key environment variables in `.env`:

```bash
# Required
GOOGLE_API_KEY=your_gemini_api_key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/paogpt

# Frontend
FRONTEND_URL=http://localhost:5173

# Optional
RATE_LIMIT_PER_MINUTE=10
ENABLE_CONVERSATION_STORAGE=true
```

### Architecture

```
backend/
├── app/
│   ├── agents/
│   │   ├── pao_gpt.py          # Main orchestrator
│   │   └── chains/
│   │       ├── guard_chain.py   # Safety checks
│   │       ├── rag_chain.py     # Retrieval + generation
│   │       └── personality.py   # Response tone/style
│   ├── api/
│   │   └── routes/chat.py       # FastAPI endpoints
│   ├── database/
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── session.py           # DB connection
│   │   └── repositories/
│   ├── services/
│   │   ├── vector_store.py      # ChromaDB wrapper
│   │   ├── embeddings.py        # Text embedding service
│   │   ├── llm.py               # Gemini integration
│   │   └── knowledge_loader.py  # PDF/text ingestion
│   ├── config.py                # Settings management
│   └── main.py                  # FastAPI app
├── scripts/
│   ├── init_db.py               # Database initialization
│   └── seed_knowledge.py        # Load knowledge base
└── tests/                       # Comprehensive test suite
```

## Design System

### Colors
```css
--snow: #fbf5f3;          /* Backgrounds */
--prussian-blue: #000022;  /* Primary text, dark sections */
--amber-earth: #e28413;    /* Primary accent, CTAs */
--raspberry: #de3c4b;      /* Secondary accent, hovers */
--intense-cherry: #c42847; /* Strong emphasis, active states */
```

### Typography
- **Headings**: Epilogue (700-900 weight)
- **Body**: IBM Plex Mono (400-600 weight)
- **Scale**: Fluid typography with clamp()

### Spacing
- Base unit: 4px
- Scale: 1, 2, 3, 4, 6, 8, 12, 16, 20, 24

## Getting Started

### Frontend Only

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Full Stack (Frontend + Backend)

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Set up .env with GOOGLE_API_KEY, DATABASE_URL, etc.
python scripts/init_db.py
python scripts/seed_knowledge.py
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173` and the backend API at `http://localhost:8000`.

## Project Structure

```
portfolio-site/
├── src/                         # Frontend (React + Vite)
│   ├── components/
│   │   ├── Navigation.jsx/css
│   │   ├── Hero.jsx/css
│   │   ├── Projects.jsx/css
│   │   ├── Skills.jsx/css
│   │   ├── Experience.jsx/css
│   │   ├── Education.jsx/css
│   │   ├── Contact.jsx/css
│   │   └── MazeExplorer.jsx/css
│   ├── data/
│   │   └── portfolio.json
│   ├── App.jsx/css
│   ├── index.css
│   └── main.jsx
├── backend/                     # pao-gpt API (FastAPI)
│   ├── app/
│   │   ├── agents/             # AI agent logic
│   │   ├── api/                # REST endpoints
│   │   ├── database/           # PostgreSQL models
│   │   ├── services/           # ChromaDB, LLM, embeddings
│   │   ├── config.py
│   │   └── main.py
│   ├── scripts/                # Setup & seeding
│   ├── tests/                  # Test suite
│   └── requirements.txt
├── public/
│   └── Paolo_Sandejas_Resume.pdf
└── package.json
```

## Content Updates

Update your portfolio content in `src/data/portfolio.json`:
- Personal information
- Projects with descriptions, tags, links
- Work experience
- Education

## Deployment

### Vercel
```bash
npm run build
vercel --prod
```

### Netlify
```bash
npm run build
netlify deploy --prod --dir=dist
```

## Design Principles

### Avoiding "AI Slop" Aesthetics
- ✅ Distinctive font pairing (IBM Plex Mono + Epilogue)
- ✅ Bold, intentional color palette with high contrast
- ✅ Geometric layouts with asymmetry
- ✅ Purposeful animations (staggered reveals, magnetic hovers)
- ✅ Custom components (no generic templates)
- ❌ No Inter/Roboto/system fonts
- ❌ No purple gradients on white
- ❌ No cookie-cutter layouts
- ❌ No slow typing animations

### Hireability Focus
- Clear role and location in header
- Immediate value propositions
- Technical depth showcased first
- Direct resume download access
- Project categorization (ML vs Creative)
- Production metrics where applicable

## License

© 2026 Paolo Sandejas. All rights reserved.
