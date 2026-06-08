from typing import Optional


class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except Exception:
                self._model = False
        return self._model if self._model is not False else None

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self._fallback_embed(texts)

    def embed_query(self, text: str) -> list[float]:
        return self.embed([text])[0]

    @staticmethod
    def _fallback_embed(texts: list[str]) -> list[list[float]]:
        import hashlib
        results = []
        for t in texts:
            h = hashlib.sha256(t.encode()).digest()
            vec = [((b / 255.0) * 2 - 1) for b in h[:384]]
            if len(vec) < 384:
                vec += [0.0] * (384 - len(vec))
            results.append(vec)
        return results


_embedding_instance: Optional[EmbeddingService] = None


def get_embedding_service(model_name: str = "all-MiniLM-L6-v2") -> EmbeddingService:
    global _embedding_instance
    if _embedding_instance is None:
        _embedding_instance = EmbeddingService(model_name)
    return _embedding_instance
