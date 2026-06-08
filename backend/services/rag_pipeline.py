from typing import Optional

from backend.services.embedding import get_embedding_service
from backend.services.knowledge_store import get_knowledge_store


EVIDENCE_WEIGHTS = {
    "RCT": 1.3,
    "meta-analysis": 1.25,
    "systematic-review": 1.2,
    "guideline": 1.15,
    "observational": 0.9,
    "expert-opinion": 0.7,
}


def rank_by_evidence(chunks: list[dict]) -> list[dict]:
    for c in chunks:
        evidence = c.get("metadata", {}).get("evidence_level", "expert-opinion")
        weight = EVIDENCE_WEIGHTS.get(evidence, 0.7)
        year = c.get("metadata", {}).get("year", 2020)
        year_boost = min((year - 2015) * 0.02, 0.1)
        c["rank_score"] = (1.0 - c.get("distance", 1.0)) * weight + year_boost
    return sorted(chunks, key=lambda c: c.get("rank_score", 0), reverse=True)


class RAGPipeline:
    def __init__(self):
        self.embedding_service = get_embedding_service()
        self.knowledge_store = get_knowledge_store()

    def query(
        self,
        user_message: str,
        child_context: str,
        top_k: int = 8,
    ) -> tuple[list[dict], str]:
        query_text = f"{child_context}\n\n{user_message}"
        query_embedding = self.embedding_service.embed_query(query_text)

        raw_chunks = self.knowledge_store.query(query_embedding, top_k=top_k)
        ranked_chunks = rank_by_evidence(raw_chunks)

        context_parts: list[str] = []
        for i, chunk in enumerate(ranked_chunks):
            meta = chunk.get("metadata", {})
            evidence = meta.get("evidence_level", "expert-opinion")
            source = meta.get("source", "unknown")
            year = meta.get("year", "n/a")
            context_parts.append(
                f"[Source {i+1}] ({evidence.upper()} | {source} | {year})\n{chunk['text']}"
            )

        full_context = "\n\n---\n\n".join(context_parts)
        return ranked_chunks, full_context


_rag_pipeline_instance: Optional[RAGPipeline] = None


def get_rag_pipeline() -> RAGPipeline:
    global _rag_pipeline_instance
    if _rag_pipeline_instance is None:
        _rag_pipeline_instance = RAGPipeline()
    return _rag_pipeline_instance
