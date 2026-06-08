import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

DEDUP_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "ingested_hashes.json"


class DeduplicationLayer:
    def __init__(self):
        self._hashes: dict[str, str] = {}
        self._load()

    def _load(self):
        if DEDUP_PATH.exists():
            try:
                self._hashes = json.loads(DEDUP_PATH.read_text(encoding="utf-8"))
            except Exception:
                self._hashes = {}

    def _save(self):
        DEDUP_PATH.parent.mkdir(exist_ok=True)
        DEDUP_PATH.write_text(json.dumps(self._hashes, indent=2, ensure_ascii=False), encoding="utf-8")

    def is_duplicate(self, identifier: str, content: str) -> bool:
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        key = f"{identifier}:{content_hash[:16]}"

        if identifier in self._hashes:
            return True

        if content_hash in self._hashes.values():
            return True

        self._hashes[identifier] = content_hash
        self._save()
        return False

    def mark_ingested(self, identifier: str, content: str):
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        self._hashes[identifier] = content_hash
        self._save()

    @property
    def count(self) -> int:
        return len(self._hashes)

    def clear(self):
        self._hashes = {}
        self._save()


_dedup_instance: Optional[DeduplicationLayer] = None


def get_dedup_layer() -> DeduplicationLayer:
    global _dedup_instance
    if _dedup_instance is None:
        _dedup_instance = DeduplicationLayer()
    return _dedup_instance
