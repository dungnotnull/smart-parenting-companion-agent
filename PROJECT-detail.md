# smart-parenting-companion — Project Detail

## Executive Summary
`smart-parenting-companion` is a privacy-first, continuously learning AI agent that serves as a trusted parenting companion from a child's birth through adulthood. It answers parent questions, provides evidence-based developmental advice, tracks milestones, and adapts its knowledge base weekly by ingesting new pediatric and educational research. Unlike generic chatbots, every response is grounded in peer-reviewed sources, tagged with evidence level, and calibrated to the specific developmental stage of the family's child(ren). The system operates primarily offline (via local SLM) with optional cloud LLM integration for more complex queries.

---

## Problem Statement
Parenting is among the most high-stakes and information-dense domains a person will navigate. Key pain points include:

- **Information overload**: A 2023 survey by the Pew Research Center found that 62% of parents of children under 12 report feeling overwhelmed by conflicting parenting advice online.
- **Lack of developmental context**: Generic search results return the same advice regardless of whether the child is 3 weeks old or 13 years old. Age-calibrated, stage-aware guidance is rare.
- **Misinformation risk**: Anti-vaccine content, sleep-training misinformation, and nutritional myths are prevalent and share the same ranking surface as AAP/WHO guidelines.
- **No memory or continuity**: Parents repeat the same context (child's age, health history, concerns) in every search; no tool builds a persistent understanding of their specific family.
- **Accessibility barriers**: Access to pediatricians for non-urgent developmental questions is limited by appointment availability, cost, and geography.
- **Static knowledge**: Books and apps published years ago cannot incorporate findings from last month's pediatric journals.

**Solution**: A locally-hosted AI agent that builds a persistent, encrypted family profile, retrieves from a continuously updated evidence-based knowledge base, and provides calibrated, stage-aware advice with clear citations and evidence levels.

---

## Target Users & Use Cases

### Primary Users
- **New parents (0–2 years)**: Feeding schedules, sleep training methods, vaccination timelines, developmental milestone tracking, postpartum parent mental health
- **Parents of toddlers (2–5 years)**: Language development, behavioral management, toilet training, nutritional needs, daycare readiness
- **Parents of school-age children (5–12 years)**: Academic support strategies, screen time guidelines, social development, learning differences (ADHD, dyslexia screening prompts), physical activity
- **Parents of adolescents (12–18 years)**: Mental health conversations, puberty guidance, identity development, academic pressure, digital safety

### Use Cases
1. "My 8-month-old isn't crawling yet — is this a concern?"
2. "What are evidence-based strategies for managing a 4-year-old's tantrum?"
3. "My 10-year-old seems anxious about school — when should I seek professional help?"
4. "What does the latest research say about screen time for under-2s?"
5. "My teenager is struggling with sleep — what does the science say about adolescent sleep needs?"
6. "Can you track that my daughter hit her first word milestone today?"

---

## Architecture Overview

```
┌───────────────────────────────────────────────────────────────────┐
│                    smart-parenting-companion                       │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                      User Interface Layer                     │ │
│  │   React Web UI (chat + milestone tracker + profile manager)  │ │
│  │              CLI (optional, for power users)                  │ │
│  └────────────────────────┬─────────────────────────────────────┘ │
│                           │ WebSocket / REST                       │
│  ┌────────────────────────▼─────────────────────────────────────┐ │
│  │                     FastAPI Core Service                      │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐│ │
│  │  │ Conversation │  │  Safety      │  │ Age-Stage Context   ││ │
│  │  │ Manager      │  │  Filter      │  │ Injector            ││ │
│  │  │ (session,    │  │ (emergency   │  │ (WHO/AAP milestones ││ │
│  │  │  history)    │  │  detection)  │  │  per child profile) ││ │
│  │  └──────┬───────┘  └──────────────┘  └─────────────────────┘│ │
│  └─────────┼────────────────────────────────────────────────────┘ │
│            │                                                        │
│  ┌─────────▼────────────────────────────────────────────────────┐ │
│  │                       RAG Pipeline                            │ │
│  │  Query Embedding → ChromaDB Retrieval → Evidence Ranking     │ │
│  │  → Context Assembly → LLM Prompt Construction                │ │
│  └─────────┬────────────────────────────────────────────────────┘ │
│            │                                                        │
│  ┌─────────▼────────────────────────────────────────────────────┐ │
│  │                   Pluggable LLM Backend                       │ │
│  │   Claude API ──┐                                             │ │
│  │   GPT-4o      ─┼─► LLMRouter (fallback chain)               │ │
│  │   Ollama/Phi3 ─┘                                             │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    Knowledge & Data Layer                     │ │
│  │  ┌──────────────────────┐   ┌─────────────────────────────┐ │ │
│  │  │  ChromaDB            │   │  SQLite + AES-256           │ │ │
│  │  │  (vector store)      │   │  Family Profiles            │ │ │
│  │  │  - research chunks   │   │  - child profiles           │ │ │
│  │  │  - guidelines        │   │  - milestone logs           │ │ │
│  │  │  - Q&A history       │   │  - conversation history     │ │ │
│  │  └──────────────────────┘   └─────────────────────────────┘ │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              Knowledge Ingestion Pipeline (Weekly)            │ │
│  │  crawl4ai → PubMed / AAP / WHO / ArXiv / JCPP               │ │
│  │  → Paper Summarizer (BART) → Chunker → Embedder → ChromaDB  │ │
│  └──────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology | Source |
|---|---|---|
| Backend framework | FastAPI 0.111 | pip |
| WebSocket streaming | FastAPI WebSocket + uvicorn | pip |
| Vector store | ChromaDB 0.5 | pip |
| Embedding models | sentence-transformers, BAAI/bge-large | HuggingFace |
| Local SLM inference | llama-cpp-python / Ollama | PyPI / GitHub |
| LLM client (Claude) | anthropic SDK 0.28+ | pip |
| LLM client (GPT-4o) | openai SDK 1.30+ | pip |
| Web crawler | crawl4ai 0.4 | pip |
| Research summarizer | transformers (BART) | HuggingFace |
| NER extraction | transformers (BERT-NER) | HuggingFace |
| Emotion detection | transformers (RoBERTa) | HuggingFace |
| Database | SQLite 3 (built-in) | stdlib |
| Encryption | cryptography (AES-256-GCM) | pip |
| Task scheduling | APScheduler 3.10 | pip |
| Frontend framework | React 18 + TypeScript | npm |
| UI components | shadcn/ui | npm |
| Markdown rendering | react-markdown | npm |
| API communication | axios + socket.io-client | npm |
| Package management | uv (Python), npm (JS) | pip / npm |

---

## ML/DL Models

### Primary Models

| Model ID | Task | Quantization | VRAM | Link |
|---|---|---|---|---|
| microsoft/Phi-3-mini-4k-instruct | Local offline Q&A (primary SLM) | Q4_K_M GGUF | ~2.5 GB | https://huggingface.co/microsoft/Phi-3-mini-4k-instruct |
| mistralai/Mistral-7B-Instruct-v0.3 | Higher-quality local inference | Q4_K_M GGUF | ~4.5 GB | https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3 |
| BAAI/bge-large-en-v1.5 | Knowledge retrieval embeddings | full precision | ~1.3 GB | https://huggingface.co/BAAI/bge-large-en-v1.5 |
| sentence-transformers/all-MiniLM-L6-v2 | Fast query embedding | full precision | ~90 MB | https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 |
| facebook/bart-large-cnn | Research paper summarization | full precision | ~1.6 GB | https://huggingface.co/facebook/bart-large-cnn |
| SamLowe/roberta-base-go_emotions | Parent emotion classification | full precision | ~500 MB | https://huggingface.co/SamLowe/roberta-base-go_emotions |
| dslim/bert-base-NER | Named entity extraction | full precision | ~420 MB | https://huggingface.co/dslim/bert-base-NER |

### Fine-Tuning Plan
No fine-tuning is planned for the MVP. The primary strategy is RAG-augmented prompting with a curated pediatric knowledge base. If evaluation reveals the local SLM consistently gives developmentally inappropriate advice, a LoRA fine-tune on a pediatric Q&A dataset (e.g., MedQuAD filtered for pediatrics) will be considered in Phase 4.

### Training Data Sources (if fine-tuning pursued)
- MedQuAD: Medical Question Answering Dataset (NLM) — filtered for pediatric questions
- iCliniq Pediatrics Q&A dataset
- AAP published guidelines formatted as instruction pairs
- WHO Child Growth Standards documentation

---

## External LLM API Integration

The system uses a **pluggable LLM router** controlled by a single `LLM_PROVIDER` environment variable. All providers share the same interface contract.

```python
# config.py
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "claude")  # "claude" | "openai" | "ollama"
LLM_CLAUDE_API_KEY = os.getenv("LLM_CLAUDE_API_KEY")
LLM_CLAUDE_MODEL = os.getenv("LLM_CLAUDE_MODEL", "claude-sonnet-4-6")
LLM_OPENAI_API_KEY = os.getenv("LLM_OPENAI_API_KEY")
LLM_OPENAI_MODEL = os.getenv("LLM_OPENAI_MODEL", "gpt-4o")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")
```

**Fallback chain**: Claude → GPT-4o → Ollama (local). If all cloud providers are unavailable, the system falls back to local Ollama and notes reduced response quality to the user.

**Prompt caching**: The system prompt (containing family profile context and developmental stage milestones) is structured as a cacheable prefix using Claude's prompt caching feature, reducing API costs for long sessions.

---

## Feature Specification

### MVP Features (Phase 1–2)
- [x] Multi-child family profile creation (name, DOB, sex, health notes)
- [x] Age-stage aware Q&A (infant / toddler / school-age / adolescent)
- [x] RAG-grounded responses with source citations
- [x] Evidence-level indicator (RCT / guideline / expert opinion) on each response
- [x] WHO/AAP developmental milestone checklist per child per age bracket
- [x] Manual milestone tracking (parent logs when child achieves a milestone)
- [x] Medical emergency detection with hard-coded "see a doctor immediately" responses
- [x] Streaming chat interface (WebSocket)
- [x] Local data storage (SQLite + AES-256)
- [x] Offline-capable local SLM mode
- [x] Weekly knowledge base auto-update via crawl4ai

### Advanced Features (Phase 3–5)
- [ ] Personalized developmental insights: detects milestone delays and raises gentle alerts
- [ ] Growth tracker: weight/height percentile charts using WHO Child Growth Standards
- [ ] Daily parenting tip push notifications (browser notifications API)
- [ ] "Ask a question" shortcut panel with pre-filled common questions per age stage
- [ ] Research digest: weekly email/notification summarizing new research relevant to the child's current age stage
- [ ] Multi-language support: Vietnamese (for primary user base) and English
- [ ] Emotion-aware responses: detects stressed/anxious tone in parent messages and adjusts response register accordingly
- [ ] Export family health timeline as PDF
- [ ] Community Q&A knowledge base expansion (curated, not user-generated raw)
- [ ] Integration with national vaccination schedule (Vietnam TIÊM CHỦNG MỞ RỘNG schedule)
- [ ] Sleep tracker with science-based recommendations per age stage
- [ ] Nutrition log with age-appropriate macro/micronutrient guidance
- [ ] Screen time guideline advisor calibrated to latest AAP guidance
- [ ] Adolescent mental health check-in with PHQ-A screener prompts and professional referral triggers

---

## Full E2E Data Flow

1. **Parent sends a message** via React chat UI (WebSocket connection to FastAPI)
2. **Safety filter** scans the incoming message for medical emergency keywords (fever >39°C in infant under 3 months, difficulty breathing, seizure, etc.) — if triggered, returns hardcoded emergency response immediately
3. **Emotion detector** (RoBERTa) classifies parent's emotional tone → influences response register (calm/informational vs. warm/reassuring)
4. **Age-stage context injector** loads the selected child's profile from SQLite → computes current developmental stage and retrieves relevant WHO/AAP milestone checklist
5. **Query embedding** (all-MiniLM-L6-v2 or bge-large) converts the parent message + child context into a dense vector
6. **ChromaDB retrieval** fetches top-K (K=8) most relevant knowledge chunks from the vector store, ranked by cosine similarity and re-ranked by evidence level
7. **Prompt assembly**: system prompt (family profile + developmental stage + milestones) + retrieved context chunks (with source, year, evidence level) + conversation history (last 10 turns) + parent message
8. **LLM router** sends assembled prompt to configured provider (Claude → GPT-4o → Ollama fallback chain)
9. **Streaming response** is sent token-by-token back to the React UI via WebSocket
10. **Post-processing**: extract cited sources, format evidence badges, append "this is not medical advice" disclaimer if response touches clinical topics
11. **Conversation history** and any milestone updates are written to SQLite (AES-256 encrypted)
12. **Weekly cron (APScheduler)**:
    - crawl4ai fetches new research from PubMed, AAP, WHO, ArXiv
    - BART summarizes each paper abstract to 3–5 sentences
    - BERT-NER extracts entities (conditions, interventions, age ranges)
    - Chunks are embedded (bge-large) and upserted into ChromaDB
    - SECOND-KNOWLEDGE-BRAIN.md update log entry is appended

---

## Privacy & Security

| Concern | Mitigation |
|---|---|
| Family profile data | SQLite database encrypted at-rest with AES-256-GCM; key derived from a user-set password via PBKDF2 |
| PII in LLM calls | Child's full name is never sent to external APIs; replaced with a role descriptor ("your 18-month-old daughter") |
| Conversation history | Stored locally only; never uploaded to any server |
| Medical advice liability | Every response involving clinical topics appends a mandatory disclaimer; emergency detection forces professional care referral |
| crawl4ai web access | Network access scoped to whitelisted research domain list only; no arbitrary URL following |
| API keys | Stored in `.env` file excluded from version control; never logged |
| Child photos (if milestone gallery added) | Stored locally, never transmitted; face detection disabled by design |

---

## Key Python/JS Dependencies

### Python (requirements.txt)
```
fastapi==0.111.0
uvicorn[standard]==0.30.1
websockets==12.0
anthropic==0.28.0
openai==1.35.0
chromadb==0.5.3
sentence-transformers==3.0.1
transformers==4.42.0
llama-cpp-python==0.2.79
crawl4ai==0.4.0
apscheduler==3.10.4
sqlalchemy==2.0.30
cryptography==42.0.8
pydantic==2.7.4
torch==2.3.1
accelerate==0.31.0
bitsandbytes==0.43.1
```

### JavaScript (package.json)
```
react: ^18.3.0
typescript: ^5.4.0
socket.io-client: ^4.7.5
axios: ^1.7.2
react-markdown: ^9.0.1
@shadcn/ui: latest
recharts: ^2.12.7  (milestone / growth charts)
date-fns: ^3.6.0
```

---

## Improvement Suggestions

1. **Sibling-aware advice**: When a family has multiple children, the agent should detect when advice for one child's age stage might affect sibling dynamics (e.g., regression behavior in toddler when newborn arrives)
2. **Partner/co-parent sync**: A lightweight sync protocol (local network only) so two devices (two parents) share the same family profile without cloud storage
3. **Grandparent mode**: A simplified, higher-contrast UI variant with shorter responses and clearer action steps for grandparents who may also be caregivers
4. **School-specific integrations**: Connect with Vietnamese school calendar to deliver back-to-school readiness checklists at the right time of year
5. **Pediatrician visit preparation**: Generate a structured list of questions to bring to the next well-child visit based on milestone data and recent concerns logged
6. **Bi-directional feedback loop**: Parent can rate each response (thumbs up/down) → low-rated responses are logged and used to retrain retrieval ranking weights (no LLM fine-tuning required)
7. **Wearable data integration (future)**: Accept sleep and activity data from smartwatches/baby monitors to provide data-grounded sleep coaching
8. **Multilingual knowledge base**: Most high-quality pediatric research is in English; build a translation pipeline (e.g., Helsinki-NLP/opus-mt-en-vi) to make the Vietnamese-language responses reference-backed
9. **Developmental red-flag proactive alerts**: At each age milestone boundary (6m, 9m, 12m, 18m, 24m, 36m …), proactively prompt the parent to assess key developmental checkpoints rather than waiting for them to ask
10. **Anonymous aggregated insights (opt-in)**: Federated aggregation of anonymized milestone timing data to produce community baselines without any PII leaving the device
