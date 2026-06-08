import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import (
    CRAWL_SCHEDULE_DAY,
    CRAWL_SCHEDULE_HOUR,
    CRAWL_SCHEDULE_MINUTE,
    LOG_LEVEL,
)
from backend.models import init_db
from backend.routes.admin import router as admin_router
from backend.routes.chat import router as chat_router
from backend.routes.profile import router as profile_router
from backend.services.middleware import (
    RateLimitMiddleware,
    RequestValidationMiddleware,
    SecurityHeadersMiddleware,
)

logging.basicConfig(level=getattr(logging, LOG_LEVEL.upper(), logging.INFO))
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Smart Parenting Companion",
    version="0.1.0",
    description="Evidence-based AI parenting guide — birth to adulthood, always learning",
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestValidationMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(profile_router)
app.include_router(admin_router)


@app.on_event("startup")
async def on_startup():
    logger.info("Initializing database...")
    init_db()
    logger.info("Database ready.")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_weekly_crawl,
        "cron",
        day_of_week=CRAWL_SCHEDULE_DAY,
        hour=CRAWL_SCHEDULE_HOUR,
        minute=CRAWL_SCHEDULE_MINUTE,
        id="weekly_crawl",
    )
    scheduler.start()
    logger.info(
        "Weekly crawl scheduled: every %s at %02d:%02d",
        CRAWL_SCHEDULE_DAY,
        CRAWL_SCHEDULE_HOUR,
        CRAWL_SCHEDULE_MINUTE,
    )


@app.get("/health")
async def health():
    return {"status": "ok", "service": "smart-parenting-companion"}


async def run_weekly_crawl():
    logger.info("Starting weekly knowledge base crawl...")
    try:
        from backend.ingestion.crawl_orchestrator import run_full_ingestion
        from backend.ingestion.skb_updater import append_update_log

        result = await run_full_ingestion()
        logger.info(
            "Crawl complete: %d new papers, %d chunks from %d sources",
            result.get("new_papers", 0),
            result.get("chunks_added", 0),
            len(result.get("sources", {})),
        )

        sources_str = ", ".join(
            f"{k}:{v}" for k, v in result.get("sources", {}).items() if v > 0
        )
        append_update_log(
            source=sources_str,
            papers_added=result.get("chunks_added", 0),
            topics=list(result.get("sources", {}).keys()),
            notable_findings=result.get("notable", ""),
        )
    except Exception as e:
        logger.error("Weekly crawl failed: %s", e)
