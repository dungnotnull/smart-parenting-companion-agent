import hashlib
import time
from typing import Optional

CACHE_TTL_SECONDS = 300


class PromptCache:
    def __init__(self):
        self._cache: dict[str, tuple[float, str]] = {}

    def _hash(self, prefix: str, profile_json: str) -> str:
        return hashlib.sha256(f"{prefix}|{profile_json}".encode()).hexdigest()

    def get(self, prefix: str, profile_json: str) -> Optional[str]:
        key = self._hash(prefix, profile_json)
        entry = self._cache.get(key)
        if entry is None:
            return None
        cached_at, cached_prefix = entry
        if time.time() - cached_at > CACHE_TTL_SECONDS:
            del self._cache[key]
            return None
        return cached_prefix

    def set(self, prefix: str, profile_json: str, full_system_prompt: str):
        key = self._hash(prefix, profile_json)
        self._cache[key] = (time.time(), full_system_prompt)

    def clear(self):
        self._cache.clear()

    @property
    def size(self) -> int:
        now = time.time()
        expired = [k for k, (ts, _) in self._cache.items() if now - ts > CACHE_TTL_SECONDS]
        for k in expired:
            del self._cache[k]
        return len(self._cache)


_prompt_cache_instance: Optional[PromptCache] = None


def get_prompt_cache() -> PromptCache:
    global _prompt_cache_instance
    if _prompt_cache_instance is None:
        _prompt_cache_instance = PromptCache()
    return _prompt_cache_instance


def build_cacheable_system_prompt(child_context: str, history_context: str, rag_context: str, register_prompt: str) -> tuple[str, str]:
    cacheable_prefix = (
        f"You are Smart Parenting Companion, an evidence-based AI parenting guide.\n\n"
        f"## Child Developmental Context\n{child_context}\n\n"
        f"## Tone Guidance\n{register_prompt}\n\n"
    )
    variable_suffix = (
        f"## Evidence-Based Knowledge Context\n{rag_context}\n\n"
        f"{history_context}\n\n"
        f"## Response Guidelines\n"
        f"- Ground your answer in the provided evidence-based knowledge context\n"
        f"- Reference specific sources with their evidence level badge (RCT, guideline, etc.)\n"
        f"- Calibrate all advice to the child's specific age and developmental stage\n"
        f"- If the evidence is insufficient, acknowledge the limits of current research\n"
    )
    full_prompt = cacheable_prefix + variable_suffix
    return cacheable_prefix, full_prompt
