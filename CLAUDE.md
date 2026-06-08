---
project: smart-parenting-companion
tagline: "Evidence-based AI parenting guide — birth to adulthood, always learning"
status: Phase 0 — Research & Environment Setup
---

# smart-parenting-companion — Project Memory

## Core Problem
Parents face an overwhelming, often contradictory flood of parenting advice with no reliable, personalized, evidence-based guide. This agent aggregates pediatric medicine, child development psychology, nutrition science, sleep research, and educational theory into a single conversational companion. It adapts its guidance to each child's specific age, developmental stage, and family context — from the first day home from the hospital through the final years of adolescence — and continuously grows smarter by ingesting new peer-reviewed research every week.

## Architecture Summary
- **Platform**: Python 3.11 + FastAPI backend; React web UI + optional CLI
- **ML Stack**: Local SLM (Phi-3-mini / Mistral-7B-Instruct) for offline Q&A; sentence-transformers for semantic retrieval; crawl4ai for weekly knowledge ingestion
- **Local SLM**: `microsoft/Phi-3-mini-4k-instruct` (primary offline model)
- **External APIs**: Claude API (primary reasoning), GPT-4o (secondary), Ollama (local inference)
- **Storage**: SQLite + AES-256 for family profiles; ChromaDB for knowledge vector store
- **Privacy**: All family-identifiable data (child profiles, chat history) stored and processed locally; no PII transmitted to external APIs

## Key Technical Decisions
1. **Age-stage context injection**: Every LLM prompt is prefixed with the child's current developmental stage (infant / toddler / school-age / adolescent) and corresponding WHO/AAP developmental milestones, ensuring all advice is developmentally appropriate
2. **RAG-first architecture**: All answers are grounded in the local evidence-based knowledge base before any LLM call, reducing hallucination risk in this safety-critical domain
3. **Evidence-level tagging**: Each knowledge chunk is tagged with its evidence level (RCT > meta-analysis > observational > expert opinion); this metadata is passed to the LLM as context
4. **crawl4ai weekly pipeline**: Scheduled crawler targets PubMed, AAP, WHO, and ArXiv weekly to update the knowledge base with newly published research
5. **Multi-child profiles**: Supports multiple children per family with independent developmental timelines, milestone trackers, and personalized response baselines
6. **Safety-first emergency detection**: Medical emergency keyword/pattern detection triggers an immediate "seek professional care now" response and suppresses all LLM-generated clinical alternatives
7. **Pluggable LLM backend**: `LLM_PROVIDER` env var switches between Claude / GPT-4o / local Ollama with graceful fallback chain

## External LLM API Integrations
| Provider | Purpose | Config Key |
|---|---|---|
| Anthropic Claude (claude-sonnet-4-6) | Primary conversational reasoning, advice generation | `LLM_CLAUDE_API_KEY` |
| OpenAI GPT-4o | Secondary fallback when Claude unavailable | `LLM_OPENAI_API_KEY` |
| Ollama (local) | Full offline / maximum-privacy mode | `OLLAMA_BASE_URL` |

## HuggingFace Models
| Model ID | Purpose | Link |
|---|---|---|
| microsoft/Phi-3-mini-4k-instruct | Local SLM for offline Q&A | https://huggingface.co/microsoft/Phi-3-mini-4k-instruct |
| mistralai/Mistral-7B-Instruct-v0.3 | Higher-quality local inference fallback | https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3 |
| BAAI/bge-large-en-v1.5 | High-quality knowledge retrieval embeddings | https://huggingface.co/BAAI/bge-large-en-v1.5 |
| sentence-transformers/all-MiniLM-L6-v2 | Fast semantic search, query embedding | https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 |
| SamLowe/roberta-base-go_emotions | Parent emotion detection for empathetic response framing | https://huggingface.co/SamLowe/roberta-base-go_emotions |
| facebook/bart-large-cnn | Research paper abstractive summarization | https://huggingface.co/facebook/bart-large-cnn |
| dslim/bert-base-NER | Named entity extraction from research papers | https://huggingface.co/dslim/bert-base-NER |

## Current Active Development Tasks
- [ ] Scaffold project directory structure and Python virtual environment
- [ ] Implement child profile data model (SQLite + AES-256 encryption)
- [ ] Build crawl4ai ingestion pipeline (PubMed / AAP / WHO / ArXiv sources)
- [ ] Set up ChromaDB vector store and embedding pipeline
- [ ] Implement RAG pipeline with age-stage context injection
- [ ] Build conversational API (FastAPI + WebSocket for streaming)
- [ ] Integrate pluggable LLM backend (Claude / GPT-4o / Ollama)
- [ ] Implement safety-first medical emergency detection layer
- [ ] Build React web UI with streaming chat interface
- [ ] Add weekly cron for SECOND-KNOWLEDGE-BRAIN auto-update

## Related Files
- `PROJECT-detail.md` — full technical specification and feature list
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase-by-phase development roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — self-improving knowledge base with research papers and auto-update protocol
