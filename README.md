<h1 align="center">Smart Parenting Companion</h1>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11-blue?style=flat-square&logo=python" alt="Python 3.11" />
  <img src="https://img.shields.io/badge/fastapi-0.111-teal?style=flat-square&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/react-18-61dafb?style=flat-square&logo=react" alt="React 18" />
  <img src="https://img.shields.io/badge/typescript-5.4-3178c6?style=flat-square&logo=typescript" alt="TypeScript" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License MIT" />
  <img src="https://img.shields.io/badge/privacy-first-8b5cf6?style=flat-square" alt="Privacy First" />
</p>

<p align="center">
  <strong>Evidence-based AI parenting guide — from birth to adulthood, always learning.</strong>
</p>

<p align="center">
  A privacy-first, self-improving AI companion that answers parenting questions grounded in peer-reviewed pediatric research, calibrated to your child's exact developmental stage, and continuously updated with the latest scientific findings.
</p>

---

## Why This Exists

Parents face an impossible information landscape. A 2023 Pew Research survey found that **62% of parents of children under 12 feel overwhelmed by conflicting parenting advice online**. Generic search engines return the same results whether your child is 3 weeks old or 13 years old. Social media algorithms amplify engagement, not accuracy — anti-vaccine content, sleep-training misinformation, and nutritional myths share the same ranking surface as AAP and WHO guidelines.

Pediatricians are the gold standard, but access is limited — by appointment availability, by cost, by geography. And even the best parenting books published three years ago cannot incorporate findings from last month's pediatric journals.

**Smart Parenting Companion** solves all of these problems at once:

| Problem | Solution |
|---|---|
| Information overload | Single, trusted source grounded in peer-reviewed research only |
| No developmental context | Every response calibrated to your child's exact age, stage, and milestones |
| Misinformation risk | Every claim tagged with evidence level (RCT > meta-analysis > observational > expert opinion) |
| No memory across sessions | Encrypted family profiles persist across every interaction |
| Access barriers | Runs locally on your machine — no appointments, no costs, no waiting |
| Static knowledge | Weekly auto-ingestion of new research from PubMed, AAP, WHO, ArXiv, and JCPP |

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│  Parent asks a question ──▶ Safety Filter ──▶ Emotion Detector      │
│                                                    │                │
│  Age-Stage Context ◀── Child Profile (encrypted)   │                │
│         │                                          │                │
│         ▼                                          ▼                │
│  Query Embedding ──▶ ChromaDB Vector Search ──▶ Evidence Re-Ranker   │
│                                                            │        │
│  System Prompt Assembly ◀── RAG Context + History + Tone   │        │
│         │                                                           │
│         ▼                                                           │
│  LLM Router (Claude → GPT-4o → Ollama)                              │
│         │                                                           │
│         ▼                                                           │
│  Streaming Response ──▶ WebSocket ──▶ Parent receives answer         │
│                                                    │                │
│  Conversation History ◀────────────────────────────┘                │
│  (AES-256 encrypted, stored locally only)                            │
└─────────────────────────────────────────────────────────────────────┘
```

Every response passes through **seven layers** before reaching the parent:

1. **Safety Filter** — Rule-based emergency keyword detection. Words like "not breathing," "seizure," or "unconscious" bypass everything and return an immediate "seek emergency care now" message. No LLM is called. No exceptions.
2. **Emotion Detector** — RoBERTa model classifies the parent's emotional tone (28 emotions). A stressed parent asking about fevers gets a warm, reassuring response. A curious parent asking about milestones gets a calm, informational one. The register modifier is passed directly into the LLM system prompt.
3. **Age-Stage Context Injector** — Pulls the child's encrypted profile, computes their exact developmental stage (newborn / infant / toddler / preschool / school-age / early adolescent / late adolescent), and retrieves the corresponding WHO milestones, Erikson stage, Piaget stage, and stage-specific guidance. Every LLM prompt is prefixed with this context.
4. **RAG Pipeline** — The parent's question + child context is embedded and queried against ChromaDB. The top-K research chunks (from AAP Bright Futures, WHO guidelines, PubMed RCTs, and more) are retrieved and re-ranked by evidence quality — RCTs beat meta-analyses, which beat observational studies, which beat expert opinions. Publication year adds a recency boost.
5. **Conversation Memory** — The last 10 turns of conversation are loaded from encrypted SQLite storage. For sessions exceeding 10 turns, earlier messages are compressed into a summary. This prevents context window overflow while preserving conversational continuity.
6. **LLM Router** — Pluggable dispatch to Claude, GPT-4o, or local Ollama (Phi-3-mini). Full fallback chain: if Claude is unavailable, it tries GPT-4o. If both are down, it falls back to your local model. All streaming, all async.
7. **Response** — Tokens stream back to the React UI via WebSocket. The mandatory disclaimer is appended. Usage is logged. The conversation is encrypted and saved.

---

## Features

### Core

| Feature | Description |
|---|---|
| **Multi-Child Profiles** | Support unlimited children per family, each with independent developmental timelines |
| **Age-Stage Aware Q&A** | Every response calibrated to the child's exact developmental stage (8 stages, newborn → adulthood) |
| **RAG-Grounded Responses** | All answers backed by retrieved peer-reviewed research, never just LLM generation |
| **Evidence-Level Badges** | Every claim tagged: `RCT`, `Meta-Analysis`, `Guideline`, `Observational`, `Expert Opinion` |
| **Medical Emergency Detection** | Hardcoded safety layer — emergency keywords trigger immediate professional referral, bypass LLM entirely |
| **Streaming WebSocket Chat** | Token-by-token streaming response display with markdown rendering |
| **Milestone Tracker** | Log developmental milestones across 5 domains (motor, language, cognitive, social-emotional, self-care) |
| **Growth Charts** | Weight and height plotted against WHO Child Growth Standards percentile curves (Recharts) |
| **Offline Mode** | Full local operation via Ollama + Phi-3-mini — no internet required after initial setup |
| **Weekly Auto-Update** | APScheduler cron ingests new research from 5 sources every Sunday at 03:00 |

### Intelligence

| Feature | Model / Approach |
|---|---|
| **Emotion-Adaptive Responses** | `SamLowe/roberta-base-go_emotions` — 28-class emotion detection with register mapping |
| **Research Summarization** | `facebook/bart-large-cnn` — abstracts distilled to 3–5 sentence digestible summaries |
| **Entity Extraction** | `dslim/bert-base-NER` + regex — age ranges, conditions, interventions extracted as metadata filters |
| **Milestone Delay Detection** | WHO upper-bound windows — flags milestones 4+ weeks overdue with severity ratings and recommendations |
| **Conversation Summarization** | LLM-powered compression of long sessions into context summaries |
| **Evidence Quality Scoring** | 6-tier classification (RCT=1 → expert-opinion=5) with confidence scoring, sample-size detection, and statistics awareness |
| **Prompt Caching** | Claude-compatible cacheable prefix architecture — family profile + developmental context cached, variable RAG context appended |

### Operations

| Feature | Description |
|---|---|
| **Pluggable LLM Backend** | Claude → GPT-4o → Ollama fallback chain. Single `LLM_PROVIDER` env var to switch |
| **Token Tracking & Cost Estimation** | Per-provider, per-date usage and cost logged to JSON. Full model pricing table |
| **Rate Limiting** | Sliding-window per-IP limiter (configurable requests/minute) |
| **Retry with Exponential Backoff** | Jittered retry on 429/5xx with configurable max attempts and delay caps |
| **API Key Rotation** | Multi-key per provider, round-robin dispatch with persistence |
| **Vietnamese Language Support** | Full VI translations of all prompts, milestones, emergency responses, and the Vietnam EPI vaccination schedule |
| **LLM Evaluation Harness** | 50-query golden test set (EN + VI) with automated characteristic checking |

### Security

| Concern | Mitigation |
|---|---|
| Family profile PII | AES-256-GCM encryption at rest — name, health notes, and conversation content stored as ciphertext |
| PII in external API calls | Child's full name replaced with role descriptor ("your 18-month-old daughter") before any LLM call |
| Network security | Security headers middleware: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy |
| API abuse | Sliding-window rate limiter on all `/api/*` routes |
| Input validation | Body size limits (10MB max), content-type enforcement |
| Knowledge ingestion | Network access scoped to whitelisted research domains only |

---

## Architecture

```
smart-parenting-companion/
├── backend/
│   ├── app.py                         # FastAPI entry point + APScheduler cron
│   ├── config.py                      # Environment-driven configuration
│   ├── models/__init__.py             # 5 SQLAlchemy tables with AES-256 encryption
│   ├── routes/
│   │   ├── chat.py                    # POST /api/chat, WS /api/chat/stream
│   │   ├── profile.py                 # Child profiles, milestones, growth logs CRUD
│   │   └── admin.py                   # Knowledge stats, crawl triggers, crawl history
│   ├── services/
│   │   ├── safety_filter.py           # Emergency keyword detection layer
│   │   ├── age_stage_mapper.py        # DOB → developmental stage + WHO milestones + Erikson + Piaget
│   │   ├── embedding.py               # SentenceTransformer wrapper with deterministic fallback
│   │   ├── knowledge_store.py         # ChromaDB CRUD with graceful degradation
│   │   ├── llm_router.py              # Claude → GPT-4o → Ollama with streaming + fallback
│   │   ├── rag_pipeline.py            # Query → embed → retrieve → evidence-rank → assemble
│   │   ├── family_profile.py          # Encrypted profile + milestone + growth CRUD
│   │   ├── conversation_manager.py    # Session state + 10-turn encrypted history
│   │   ├── emotion_detector.py        # RoBERTa-go-emotions + register modifier
│   │   ├── research_summarizer.py     # BART-CNN abstractive summarization
│   │   ├── entity_extractor.py        # BERT-NER + regex entity extraction
│   │   ├── milestone_delay_detector.py # WHO upper-bound delay detection with severity
│   │   ├── conversation_summarizer.py  # LLM-powered session compression
│   │   ├── prompt_cache.py            # Claude cacheable prefix with TTL invalidation
│   │   ├── token_tracker.py           # Usage + cost estimation with JSON persistence
│   │   ├── rate_limiter.py            # Sliding-window per-IP rate limiter
│   │   ├── retry.py                   # Exponential backoff with jitter + fallback chain
│   │   ├── api_key_rotator.py         # Multi-key round-robin persistence
│   │   ├── vietnamese_i18n.py         # Full VI localization (prompts, milestones, EPI schedule)
│   │   ├── eval_harness.py            # 50-query golden test set evaluation framework
│   │   ├── knowledge_seeder.py        # 30 evidence-grounded AAP/WHO seed chunks
│   │   └── middleware.py              # Rate limit + security headers + request validation
│   └── ingestion/
│       ├── pubmed.py                  # PubMed NCBI E-utilities API + dev mock fallback
│       ├── crawl_orchestrator.py      # 5-source orchestration (PubMed, AAP, WHO, ArXiv, JCPP)
│       ├── dedup.py                   # SHA-256 hash-based deduplication with persistence
│       ├── evidence_scorer.py         # 6-tier evidence classification with quality scoring
│       └── skb_updater.py             # SECOND-KNOWLEDGE-BRAIN.md auto-append protocol
├── frontend/
│   └── src/
│       ├── App.tsx                    # 3-panel shell (chat + sidebar + context)
│       ├── components/
│       │   ├── ChatWindow.tsx         # Streaming markdown chat with safety alert display
│       │   ├── ChatInput.tsx          # Multi-line input with shift-enter support
│       │   ├── ProfilePanel.tsx       # Child selector + create form with VI/EN toggle
│       │   ├── DevelopmentalPanel.tsx  # Stage, Erikson, Piaget, milestones display
│       │   ├── ChildDashboard.tsx     # Milestone tracker + growth chart container
│       │   ├── MilestoneTracker.tsx   # 5-domain milestone logging with color-coded history
│       │   ├── GrowthChart.tsx        # WHO weight/height charts via Recharts
│       │   └── AdminDashboard.tsx     # Knowledge stats, manual crawl trigger, crawl history
│       ├── hooks/useWebSocket.ts      # WebSocket streaming with state management
│       └── lib/
│           ├── types.ts               # Full TypeScript interfaces
│           └── api.ts                 # REST API client
├── scripts/
│   ├── seed_knowledge_base.py         # Initial knowledge base seeding
│   └── crawl_pubmed.py                # Standalone PubMed crawler
├── docker-compose.yml                 # Multi-service orchestration (backend + frontend + optional ChromaDB/Ollama)
├── Dockerfile                          # Backend container (Python 3.11-slim)
├── frontend/Dockerfile.frontend       # Frontend container (Node 20, production build)
├── requirements.txt                   # Python dependencies
├── .env.example                       # All configuration keys documented
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md  # Phase-by-phase completion log
├── SECOND-KNOWLEDGE-BRAIN.md          # Self-updating research knowledge base
└── PROJECT-detail.md                  # Full technical specification
```

---

## Quick Start

### Prerequisites

- **Python 3.11+** — [python.org](https://www.python.org/downloads/)
- **Node.js 18+** — [nodejs.org](https://nodejs.org/)
- **Docker + Docker Compose** *(optional — for containerized deployment)*

### 1. Clone

```bash
git clone https://github.com/dungnotnull/smart-parenting-companion-agent.git
cd smart-parenting-companion-agent
```

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env` and set at minimum:
```env
ENCRYPTION_KEY=your-256-bit-secure-random-key-here
LLM_PROVIDER=claude               # or "openai" or "ollama"
LLM_CLAUDE_API_KEY=sk-ant-...     # if using Claude
```

Generate a secure encryption key:
```bash
python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"
```

### 3. Backend

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database and seed knowledge base
python scripts/seed_knowledge_base.py

# Start the backend
python main.py
```

The API server starts at `http://localhost:8000`. Open `http://localhost:8000/docs` for the interactive Swagger documentation.

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

### 5. Docker Compose (alternative)

```bash
# Basic stack (backend + frontend)
docker compose up -d

# With ChromaDB as a separate service
docker compose --profile chroma up -d

# Full local AI stack (backend + frontend + ChromaDB + Ollama)
docker compose --profile full up -d
```

---

## Configuration Reference

| Variable | Required | Description | Default |
|---|---|---|---|
| `LLM_PROVIDER` | Yes | LLM backend: `claude`, `openai`, `ollama` | `claude` |
| `LLM_CLAUDE_API_KEY` | If Claude | Anthropic API key | — |
| `LLM_CLAUDE_MODEL` | No | Claude model ID | `claude-sonnet-4-6` |
| `LLM_OPENAI_API_KEY` | If OpenAI | OpenAI API key | — |
| `LLM_OPENAI_MODEL` | No | OpenAI model ID | `gpt-4o` |
| `OLLAMA_BASE_URL` | No | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | No | Ollama model name | `phi3:mini` |
| `ENCRYPTION_KEY` | **Yes** | 32-byte base64 key for AES-256-GCM | — |
| `SQLITE_PATH` | No | Path to encrypted profile database | `data/family_profiles.db` |
| `CHROMA_PERSIST_DIR` | No | ChromaDB storage directory | `data/chroma_store` |
| `CRAWL_SCHEDULE_DAY` | No | Day for weekly research crawl | `sun` |
| `CRAWL_SCHEDULE_HOUR` | No | Hour for weekly crawl (24h) | `3` |
| `CRAWL_SCHEDULE_MINUTE` | No | Minute for weekly crawl | `0` |
| `LOG_LEVEL` | No | Logging level | `INFO` |

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/profile` | Create a child profile |
| `GET` | `/api/profile/{child_id}` | Get child profile with developmental context |
| `PUT` | `/api/profile/{child_id}` | Update child profile |
| `GET` | `/api/profile/family/{family_id}` | List all children for a family |
| `POST` | `/api/profile/milestone` | Log a developmental milestone |
| `GET` | `/api/profile/{child_id}/milestones` | Get milestone history |
| `POST` | `/api/profile/growth` | Log a growth measurement |
| `GET` | `/api/profile/{child_id}/growth` | Get growth history |
| `POST` | `/api/chat` | Send a message, receive a response |
| `WS` | `/api/chat/stream` | WebSocket streaming chat |
| `GET` | `/api/admin/knowledge-stats` | Knowledge base statistics |
| `GET` | `/api/admin/crawl-logs` | Recent crawl history |
| `POST` | `/api/admin/trigger-crawl` | Manually trigger a research crawl |
| `GET` | `/health` | Health check |

---

## Data Flow: A Message End-to-End

1. **Parent types** "My 8-month-old isn't crawling yet, should I be worried?" in the React chat UI
2. **WebSocket** transmits the message to FastAPI at `/api/chat/stream`
3. **Safety Filter** scans for emergency keywords — none found, proceeds
4. **Emotion Detector** classifies the message as `anxiety` → sets response register to `warm_reassuring`
5. **Child Profile** is loaded from encrypted SQLite → DOB computed → stage is `infant` (8 months)
6. **Developmental Context** assembled: "Infant, 8 months. Erikson: Trust vs. Mistrust. Piaget: Sensorimotor. Key milestones: rolls over, sits without support, crawls, pulls to stand..."
7. **RAG Pipeline** embeds the query + context, searches ChromaDB, retrieves 8 chunks about infant motor development, re-ranks by evidence quality and recency
8. **Conversation History** loads the last 10 turns from this session
9. **System Prompt** is assembled: cacheable prefix (profile + context + tone) + RAG context + history + response guidelines
10. **LLM Router** dispatches to Claude → response streams back token by token
11. **Disclaimer** is appended: "This information is for educational purposes only..."
12. **Conversation** is encrypted and saved to SQLite
13. **Token usage** is tracked, cost is estimated, stats are persisted

---

## The Weekly Knowledge Loop

Every Sunday at 03:00 local time, the system automatically:

1. **Crawls 5 research sources** — PubMed NCBI E-utilities (10 pediatric queries), AAP Journals RSS (2 feeds), WHO Child Health RSS + HTML, ArXiv (3 AI + neurodevelopment queries), Journal of Child Psychology and Psychiatry RSS
2. **Deduplicates** — SHA-256 hash check against all previously ingested papers
3. **Scores evidence quality** — classifies study design (RCT / meta-analysis / systematic review / guideline / observational / case study / expert opinion), assigns confidence, detects sample sizes and statistics
4. **Summarizes** — BART distills each abstract to 3–5 digestible sentences
5. **Extracts entities** — BERT-NER pulls age ranges, medical conditions, interventions, and organizations as metadata
6. **Embeds and upserts** — chunks are embedded and stored in ChromaDB with full metadata
7. **Updates the knowledge base** — appends a dated entry to `SECOND-KNOWLEDGE-BRAIN.md` with papers added, topics covered, and notable findings

You can also trigger a manual crawl at any time from the Admin Dashboard or via `POST /api/admin/trigger-crawl`.

---

## The Knowledge Base

The `SECOND-KNOWLEDGE-BRAIN.md` file in the repository root is the project's living, self-updating knowledge base. It contains:

- **Core theoretical foundations** — Piaget's cognitive stages, Vygotsky's Zone of Proximal Development, Bronfenbrenner's Ecological Systems Theory, Bowlby & Ainsworth Attachment Theory, Erikson's Psychosocial Stages
- **Key domain areas** — nutrition & feeding (WHO/AAP guidelines), sleep science (National Sleep Foundation recommendations), vaccination (Vietnam EPI + AAP/CDC schedules), screen time (AAP 2023 guidance), mental health screening (PHQ-A, ASQ-3)
- **Curated research papers** — landmark studies (LEAP Trial, NICHD child care study, NCS-A adolescent mental health), with DOI, year, venue, and relevance notes
- **State-of-the-art ML models** — language models (Phi-3, Mistral, Gemma), embedding models (BGE, MiniLM), specialized models (RoBERTa emotions, BART summarizer, BERT-NER, OPUS translation)
- **Tools, libraries & frameworks** — full version and source links for every dependency
- **Knowledge update log** — dated entries for every ingestion run, tracking sources crawled, papers added, topics covered, and notable findings

---

## Safety & Limitations

This is **not a medical device**. It provides educational information grounded in peer-reviewed research. It does not diagnose, treat, or prescribe.

**What it does well:**
- Retrieves and synthesizes evidence-based pediatric guidelines
- Calibrates advice to age and developmental stage
- Detects medical emergencies and immediately refers to professional care
- Tags every claim with evidence level so you know what's a guideline vs. expert opinion
- Updates weekly with new research

**What it cannot do:**
- Replace a pediatrician. Ever. If you are concerned about your child's health, see a doctor.
- Guarantee 100% accuracy. RAG reduces hallucination substantially, but no AI is infallible.
- Handle medical emergencies beyond detection and referral. It will not generate clinical advice for emergency scenarios.

**Hard safety guarantees:**
- Emergency keywords (`not breathing`, `seizure`, `unconscious`, `choking`, `fever 104`, `suicide`) trigger an immediate hardcoded "seek emergency care now" response. The LLM is never called. This cannot be overridden.
- Every clinical response includes the mandatory disclaimer: "This information is for educational purposes only..."
- Child names are never transmitted to external APIs — replaced with role descriptors before any LLM call.

---

## Models

| Model | Purpose | Size | Source |
|---|---|---|---|
| `microsoft/Phi-3-mini-4k-instruct` | Primary local offline Q&A | ~2.5 GB (Q4_K_M) | HuggingFace |
| `mistralai/Mistral-7B-Instruct-v0.3` | Higher-quality local inference fallback | ~4.5 GB (Q4_K_M) | HuggingFace |
| `BAAI/bge-large-en-v1.5` | Primary knowledge retrieval embeddings | ~1.3 GB | HuggingFace |
| `sentence-transformers/all-MiniLM-L6-v2` | Fast query embedding | ~90 MB | HuggingFace |
| `SamLowe/roberta-base-go_emotions` | Parent emotion classification (28 classes) | ~500 MB | HuggingFace |
| `facebook/bart-large-cnn` | Research paper abstractive summarization | ~1.6 GB | HuggingFace |
| `dslim/bert-base-NER` | Named entity extraction from papers | ~420 MB | HuggingFace |

All models run locally. No model outputs are sent to external services.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI, Uvicorn, WebSockets |
| ML Inference | HuggingFace Transformers, Sentence-Transformers, llama-cpp-python |
| Vector Store | ChromaDB (persistent, cosine similarity, HNSW index) |
| Database | SQLite (via SQLAlchemy ORM) + AES-256-GCM encryption |
| LLM Clients | Anthropic SDK, OpenAI SDK, Ollama REST API |
| Web Crawling | crawl4ai, NCBI E-utilities API, RSS/Atom parsing |
| Task Scheduling | APScheduler (AsyncIOScheduler) |
| Frontend | React 18, TypeScript 5, Vite, Tailwind CSS |
| Charts | Recharts (WHO percentile growth curves) |
| Containerization | Docker, Docker Compose (multi-service with health checks) |

---

## Contributing

Contributions are welcome. Areas where help is especially valuable:

- **New research sources** — Add a crawler for a pediatric journal or research database in `backend/ingestion/`
- **Language support** — Extend `vietnamese_i18n.py` patterns for additional languages
- **Safety filter expansion** — Add emergency keywords and response templates for languages and cultural contexts
- **Model evaluation** — Add queries to the golden test set in `backend/services/eval_harness.py`
- **Frontend polish** — Improve the React UI, add accessibility features, or create mobile-responsive layouts

Before submitting a PR, please ensure:

1. New features include appropriate safety checks
2. Changes to the LLM pipeline preserve the full fallback chain (Claude → GPT-4o → Ollama)
3. Knowledge ingestion changes maintain deduplication and evidence classification
4. All medical-adjacent responses include the mandatory disclaimer
5. The prompt caching architecture is preserved (cacheable prefix + variable suffix)

---

## License

MIT © 2026 Claude

---

## Disclaimer

This software provides educational information only. It is not a medical device and does not provide medical advice, diagnosis, or treatment. Always consult your pediatrician or a qualified healthcare provider regarding any concerns about your child's health or development. In case of a medical emergency, call your local emergency number immediately.

The information provided by this software is sourced from peer-reviewed research and evidence-based guidelines, but no representation is made as to its accuracy, completeness, or suitability for any particular purpose. Use at your own discretion.
