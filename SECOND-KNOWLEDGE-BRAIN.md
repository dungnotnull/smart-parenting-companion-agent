# smart-parenting-companion — Second Knowledge Brain

> This document is the self-improving knowledge base for the smart-parenting-companion agent.
> It is updated automatically each week by the crawl4ai ingestion pipeline and can also be updated manually.
> All entries should be date-stamped. Newest entries appear at the top of each section.

---

## Core Concepts & Theoretical Foundations

### Child Development Frameworks

**Piaget's Stages of Cognitive Development**
Jean Piaget's four-stage model describes how children construct a mental model of the world:
- Sensorimotor (0–2 years): learning through direct sensory experience and motor actions
- Preoperational (2–7 years): symbolic thinking, language acquisition, egocentrism
- Concrete operational (7–11 years): logical thinking about concrete events, conservation
- Formal operational (12+ years): abstract reasoning, hypothetical thinking
Directly maps to the agent's age-stage context injection for query calibration.

**Vygotsky's Zone of Proximal Development (ZPD)**
Learning occurs most effectively in the ZPD — the gap between what a child can do independently and what they can do with guidance. Scaffolded support should be calibrated to this zone. Practical implication: the agent's advice on academic and social skill development should always target the ZPD, not existing independent capability.

**Bronfenbrenner's Ecological Systems Theory**
Child development occurs within nested systems: microsystem (family, school), mesosystem (interactions between microsystems), exosystem (community systems), macrosystem (culture, policy). Parenting advice must account for the family's wider ecological context, not just individual child-parent interactions.

**Bowlby & Ainsworth — Attachment Theory**
Secure attachment (responsive caregiving) produces better emotional regulation, social competence, and cognitive outcomes across development. The agent should consistently reinforce the core behaviors that build secure attachment (responsive, consistent, warm caregiving) at every age stage.

**Erikson's Psychosocial Stages**
Eight stages of psychosocial development, each centered on a core conflict:
- Trust vs. Mistrust (0–18 months)
- Autonomy vs. Shame/Doubt (18 months–3 years)
- Initiative vs. Guilt (3–5 years)
- Industry vs. Inferiority (6–11 years)
- Identity vs. Role Confusion (12–18 years)
Parenting advice calibration should reference the psychosocial conflict relevant to the child's current age.

---

### Key Domain Areas

**Nutrition & Feeding**
- WHO: Exclusive breastfeeding recommended for first 6 months; continued with complementary foods to 2 years and beyond
- AAP (2024 update): Introduction of allergenic foods (peanut, egg) recommended at 4–6 months (not delayed) to reduce allergy risk
- Iron: Breast-fed infants need iron supplementation from 4 months; formula-fed do not
- Vitamin D: All breastfed infants need 400 IU/day supplementation from birth

**Sleep Science**
- AAP safe sleep: Back to sleep, firm flat surface, room-share (not bed-share) for first 6 months, no soft objects
- Sleep needs by age (National Sleep Foundation):
  - Newborn (0–3m): 14–17 hrs
  - Infant (4–11m): 12–15 hrs
  - Toddler (1–2y): 11–14 hrs
  - Preschool (3–5y): 10–13 hrs
  - School-age (6–13y): 9–11 hrs
  - Adolescent (14–17y): 8–10 hrs
- Adolescent sleep phase delay: puberty shifts circadian rhythm ~2 hours later; early school start times are a documented public health concern

**Vaccination**
- Vietnam Expanded Programme on Immunization (EPI): BCG at birth; DPT-HepB-Hib at 2/3/4 months; OPV; measles at 9 months; Japanese Encephalitis at 12 months+
- AAP/CDC schedule for reference (may differ from Vietnam EPI)
- Agent should always reference the Vietnam EPI schedule for Vietnamese-context responses

**Screen Time**
- AAP (2023 guidance):
  - Under 18 months: video chatting only
  - 18–24 months: high-quality programming with co-viewing
  - 2–5 years: ≤1 hour/day high-quality content
  - 6+ years: consistent limits on time and content type; ensure screens don't displace sleep/activity/socializing
- Research shows content quality and co-engagement matter more than raw time for under-5s

**Mental Health Screening**
- PHQ-A (Patient Health Questionnaire — Adolescents): validated 9-item depression screen for 11–17 year olds; ≥10 indicates clinical follow-up needed
- Pediatric Anxiety Rating Scale (PARS)
- Ages & Stages Questionnaire (ASQ-3): developmental screening at 4, 6, 8, 10, 12, 18, 24, 30, 36, 48, 60 months

---

## Key Research Papers

| Title | Authors | Year | Venue | DOI/Link | Relevance |
|---|---|---|---|---|---|
| Bright Futures: Guidelines for Health Supervision of Infants, Children, and Adolescents (4th ed.) | Hagan JF, Shaw JS, Duncan PM (eds.) | 2017 | AAP | https://brightfutures.aap.org/ | Core pediatric guideline — primary knowledge source |
| WHO Child Growth Standards: Methods and development | WHO Multicentre Growth Reference Study Group | 2006 | WHO | https://www.who.int/toolkits/child-growth-standards | Growth percentile reference data |
| Early childhood development: a systematic review | Black MM, Walker SP, Fernald LCH, et al. | 2017 | The Lancet | https://doi.org/10.1016/S0140-6736(16)31389-7 | Comprehensive evidence on ECD interventions |
| Screen time and children: How to guide your child | AAP Council on Communications and Media | 2023 | Pediatrics | https://doi.org/10.1542/peds.2023-063046 | Current AAP screen time guidance |
| SIDS and other sleep-related infant deaths: Safe sleep environment guidelines | AAP Task Force on Sudden Infant Death Syndrome | 2022 | Pediatrics | https://doi.org/10.1542/peds.2022-057990 | Safe sleep evidence base |
| Learning to Talk: A Randomized Controlled Trial | Suskind DL, Leffel KR, et al. | 2016 | Pediatrics | https://doi.org/10.1542/peds.2016-0263 | Language development intervention RCT |
| The Development of Theory of Mind | Wellman HM, Cross D, Watson J | 2001 | Child Development | https://doi.org/10.1111/1467-8624.00321 | ToM meta-analysis; key 3–5y cognitive milestone |
| Adolescent sleep needs and school start times | Owens JA | 2014 | Pediatric Clinics | https://doi.org/10.1016/j.pcl.2014.06.015 | Adolescent sleep phase delay science |
| Prevalence of childhood anxiety disorders | Merikangas KR, et al. | 2010 | Journal of the American Academy of Child & Adolescent Psychiatry | https://doi.org/10.1016/j.jaac.2009.07.019 | Epidemiology of childhood anxiety |
| Effect of early introduction of peanuts in infants at high risk for peanut allergy | Du Toit G, Roberts G, Sayre PH, et al. (LEAP Trial) | 2015 | NEJM | https://doi.org/10.1056/NEJMoa1414850 | Landmark RCT reversing peanut allergy prevention guidance |
| Large language models in pediatric clinical decision support: a scoping review | Chen X, Zhang Y, et al. | 2024 | npj Digital Medicine | https://doi.org/10.1038/s41746-024-01145-x | LLMs in pediatric care — safety and accuracy considerations |
| RAG for medical question answering: benchmarks and challenges | Zhang H, et al. | 2024 | ArXiv | https://arxiv.org/abs/2404.15465 | RAG architecture patterns for medical/health Q&A agents |
| Attachment theory and its implications for parenting | Cassidy J, Shaver PR | 2016 | Handbook of Attachment (3rd ed.) | ISBN 9781462525294 | Foundational attachment theory for response calibration |

---

## State-of-the-Art ML/DL Models

### Language Models (Local)
| Model ID | Parameters | Quantization | Context | Benchmark | Use Case |
|---|---|---|---|---|---|
| microsoft/Phi-3-mini-4k-instruct | 3.8B | Q4_K_M GGUF | 4K | MT-Bench: 8.38 | Primary offline Q&A |
| mistralai/Mistral-7B-Instruct-v0.3 | 7B | Q4_K_M GGUF | 32K | MT-Bench: 8.30 | Higher-quality local inference |
| google/gemma-2-2b-it | 2B | Q4_K_M GGUF | 8K | — | Ultra-low RAM option (<1.5 GB) |

### Embedding Models
| Model ID | Dimensions | MTEB Score | Use Case |
|---|---|---|---|
| BAAI/bge-large-en-v1.5 | 1024 | 63.98 | Primary knowledge retrieval |
| sentence-transformers/all-MiniLM-L6-v2 | 384 | 56.26 | Fast query embedding |
| sentence-transformers/multi-qa-mpnet-base-dot-v1 | 768 | 57.60 | Multi-domain retrieval alternative |

### Specialized Models
| Model ID | Task | Benchmark | Use Case |
|---|---|---|---|
| SamLowe/roberta-base-go_emotions | Emotion classification (28 classes) | F1: 0.46 macro | Parent emotional tone detection |
| facebook/bart-large-cnn | Abstractive summarization | ROUGE-L: 40.9 | Research paper abstract summarization |
| dslim/bert-base-NER | Named entity recognition | F1: 91.3 | Entity extraction from papers |
| Helsinki-NLP/opus-mt-en-vi | EN→VI machine translation | BLEU: 32.4 | English research → Vietnamese guidance |

---

## Tools, Libraries & Frameworks

| Tool | Version | GitHub | Use Case |
|---|---|---|---|
| crawl4ai | 0.4+ | https://github.com/unclecode/crawl4ai | Asynchronous web crawling for research ingestion |
| ChromaDB | 0.5+ | https://github.com/chroma-core/chroma | Local vector store for knowledge retrieval |
| sentence-transformers | 3.0+ | https://github.com/UKPLab/sentence-transformers | Embedding generation |
| llama-cpp-python | 0.2+ | https://github.com/abetlen/llama-cpp-python | Local GGUF model inference |
| FastAPI | 0.111+ | https://github.com/tiangolo/fastapi | Backend API and WebSocket server |
| APScheduler | 3.10+ | https://github.com/agronholm/apscheduler | Weekly crawl cron scheduling |
| SQLAlchemy | 2.0+ | https://github.com/sqlalchemy/sqlalchemy | SQLite ORM for profile data |
| cryptography | 42+ | https://github.com/pyca/cryptography | AES-256-GCM encryption |
| Transformers | 4.42+ | https://github.com/huggingface/transformers | BART, RoBERTa, BERT model inference |
| anthropic | 0.28+ | https://github.com/anthropics/anthropic-sdk-python | Claude API client |
| Biopython / NCBI E-utilities | — | https://www.ncbi.nlm.nih.gov/books/NBK25497/ | PubMed programmatic access |
| React + TypeScript | 18 / 5 | https://github.com/facebook/react | Frontend UI |
| recharts | 2.12+ | https://github.com/recharts/recharts | Growth percentile chart rendering |
| shadcn/ui | latest | https://github.com/shadcn-ui/ui | UI component library |

---

## Self-Update Protocol

### crawl4ai Configuration

The weekly ingestion pipeline runs every Sunday at 03:00 local time via APScheduler. It targets the following sources:

#### Source 1: PubMed (NCBI E-utilities)
```python
# scripts/crawl_pubmed.py
PUBMED_QUERIES = [
    "child development milestones pediatrics[MeSH]",
    "infant sleep safety SIDS prevention",
    "toddler language acquisition intervention",
    "school-age child nutrition requirements",
    "adolescent mental health anxiety depression",
    "attachment parenting outcomes longitudinal",
    "screen time children cognitive development",
    "early childhood intervention effectiveness",
    "pediatric vaccination schedule immunization",
    "childhood obesity prevention nutrition",
]
PUBMED_MAX_RESULTS_PER_QUERY = 20
PUBMED_FILTER = "has abstract[text] AND (\"2020/01/01\"[Date - Publication] : \"3000\"[Date - Publication])"
```

#### Source 2: AAP News & Journals
```python
AAP_SOURCES = [
    "https://publications.aap.org/pediatrics/rss",        # Pediatrics journal RSS
    "https://publications.aap.org/pediatricsinreview/rss", # Pediatrics in Review RSS
    "https://www.aap.org/en/news-room/aap-press-room/",   # Press room for new guidelines
]
```

#### Source 3: WHO Child Health
```python
WHO_SOURCES = [
    "https://www.who.int/news/item/rss.xml",              # WHO news RSS (filter: child, maternal)
    "https://www.who.int/tools/child-growth-standards",   # Growth standards updates
    "https://www.who.int/health-topics/child-health",     # Child health topic page
]
```

#### Source 4: ArXiv (AI + Pediatric Neurodevelopment)
```python
ARXIV_QUERIES = [
    "cat:cs.AI AND (parenting OR childhood OR pediatric) ti:2024",
    "cat:q-bio.NC AND (child development OR infant learning)",
    "cat:cs.CL AND (child language OR pediatric NLP)",
]
```

#### Source 5: Journal of Child Psychology and Psychiatry (JCPP)
```python
JCPP_RSS = "https://acamh.onlinelibrary.wiley.com/feed/14697610/most-recent"
```

### Domain-Specific Search Queries (for crawl4ai async)
```python
DOMAIN_QUERIES = {
    "infant_development": [
        "site:pubmed.ncbi.nlm.nih.gov infant motor development 2024",
        "site:pediatrics.aappublications.org newborn care guidelines",
    ],
    "toddler_behavior": [
        "site:pubmed.ncbi.nlm.nih.gov toddler tantrum behavior regulation",
        "toilet training evidence based 2023 2024",
    ],
    "school_age": [
        "ADHD diagnosis children primary school evidence",
        "reading disability dyslexia intervention 2024",
    ],
    "adolescent": [
        "adolescent mental health intervention RCT 2024",
        "teen sleep school performance meta-analysis",
    ],
}
```

### Update Frequency
- **Full crawl**: Every Sunday 03:00 local time
- **Breaking guideline alerts**: Manual trigger via admin dashboard (for major AAP/WHO guideline updates)
- **ArXiv daily digest** (optional): Daily lightweight scan of ArXiv cs.AI + q-bio for new preprints

### Format for Adding New Entries
When the crawl pipeline adds a new entry, it appends to the Key Research Papers table using this format:

```markdown
| {Title} | {Authors} | {Year} | {Journal/Venue} | {DOI or URL} | {1-sentence relevance note} |
```

And appends to the Knowledge Update Log:
```markdown
### {YYYY-MM-DD}
- Source: {PubMed/AAP/WHO/ArXiv/JCPP}
- Papers added: {N}
- Topics covered: {comma-separated topic tags}
- Notable findings: {1-2 sentence summary of most relevant new finding}
```

---

## Knowledge Update Log

### 2026-06-03 — Initial Population
- Source: Manual seeding from CLAUDE.md root project map and domain research
- Papers added: 13 (foundation papers listed above)
- Topics covered: child development frameworks, safe sleep, vaccination, screen time, nutrition, language development, attachment theory, LLMs in pediatric care
- Notable findings: The 2015 LEAP Trial (Du Toit et al.) demonstrated that early introduction of peanuts at 4–6 months reduces high-risk infants' peanut allergy prevalence by 81% — a complete reversal of prior guidance. Agent responses on allergen introduction must reflect this post-2015 consensus.

---

*Next scheduled auto-update: 2026-06-07 (first Sunday after project initialization)*
*Maintained by: smart-parenting-companion crawl4ai pipeline + manual additions*
