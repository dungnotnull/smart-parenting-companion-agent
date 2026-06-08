from typing import Optional

from backend.config import CHROMA_PERSIST_DIR


class KnowledgeStoreService:
    def __init__(self, persist_dir: str = CHROMA_PERSIST_DIR, collection_name: str = "parenting_knowledge"):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self._client = None
        self._collection = None

    @property
    def client(self):
        if self._client is None:
            try:
                import chromadb
                from chromadb.config import Settings
                self._client = chromadb.PersistentClient(
                    path=self.persist_dir,
                    settings=Settings(anonymized_telemetry=False),
                )
            except Exception:
                self._client = False
        return self._client if self._client is not False else None

    @property
    def collection(self):
        if self._collection is None:
            client = self.client
            if client is not None:
                try:
                    self._collection = client.get_or_create_collection(
                        name=self.collection_name,
                        metadata={"hnsw:space": "cosine"},
                    )
                except Exception:
                    self._collection = False
            else:
                self._collection = False
        return self._collection if self._collection is not False else None

    def query(
        self,
        query_embedding: list[float],
        top_k: int = 8,
        filter_stage: Optional[str] = None,
    ) -> list[dict]:
        coll = self.collection
        if coll is None:
            return []

        where_filter = None
        if filter_stage:
            where_filter = {"age_stage": filter_stage}

        results = coll.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        chunks = []
        ids_list = results.get("ids", [[]])[0]
        docs_list = results.get("documents", [[]])[0]
        metas_list = results.get("metadatas", [[]])[0]
        dists_list = results.get("distances", [[]])[0]

        for i in range(len(ids_list)):
            chunks.append({
                "id": ids_list[i] if i < len(ids_list) else "",
                "text": docs_list[i] if i < len(docs_list) else "",
                "metadata": metas_list[i] if i < len(metas_list) else {},
                "distance": dists_list[i] if i < len(dists_list) else 1.0,
            })
        return chunks

    def upsert_chunks(self, chunks: list[dict]):
        coll = self.collection
        if coll is None:
            return

        ids = [c["id"] for c in chunks]
        documents = [c["text"] for c in chunks]
        metadatas = [c.get("metadata", {}) for c in chunks]
        embeddings = [c.get("embedding") for c in chunks]

        if any(e is None for e in embeddings):
            return

        coll.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def count(self) -> int:
        coll = self.collection
        if coll is None:
            return 0
        return coll.count()

    def delete_by_ids(self, ids: list[str]):
        coll = self.collection
        if coll is None:
            return
        coll.delete(ids=ids)


_knowledge_store_instance: Optional[KnowledgeStoreService] = None


def get_knowledge_store() -> KnowledgeStoreService:
    global _knowledge_store_instance
    if _knowledge_store_instance is None:
        _knowledge_store_instance = KnowledgeStoreService()
    return _knowledge_store_instance
