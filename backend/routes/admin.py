from fastapi.routing import APIRouter

from backend.models import CrawlLog, SessionLocal
from backend.services.knowledge_store import get_knowledge_store

router = APIRouter(prefix="/api", tags=["admin"])

ks = get_knowledge_store


@router.get("/admin/knowledge-stats")
async def knowledge_stats():
    return {
        "total_chunks": ks().count(),
        "collection_name": ks().collection_name,
    }


@router.get("/admin/crawl-logs")
async def crawl_logs(limit: int = 20):
    db = SessionLocal()
    try:
        logs = (
            db.query(CrawlLog)
            .order_by(CrawlLog.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "id": log.id,
                "source": log.source,
                "papers_found": log.papers_found,
                "papers_added": log.papers_added,
                "topics": log.topics,
                "notable_findings": log.notable_findings,
                "status": log.status,
                "created_at": log.created_at.isoformat() if log.created_at else None,
            }
            for log in logs
        ]
    finally:
        db.close()


@router.post("/admin/trigger-crawl")
async def trigger_crawl():
    from backend.ingestion.crawl_orchestrator import run_full_ingestion
    result = await run_full_ingestion()
    return result
