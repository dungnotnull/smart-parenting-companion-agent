import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

KEY_ROTATION_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "api_keys.json"


class ApiKeyRotator:
    def __init__(self):
        self._keys: dict[str, list[str]] = {}
        self._indices: dict[str, int] = {}
        self._load()

    def _load(self):
        if KEY_ROTATION_PATH.exists():
            try:
                data = json.loads(KEY_ROTATION_PATH.read_text(encoding="utf-8"))
                self._keys = data.get("keys", {})
            except Exception:
                self._keys = {}

    def _save(self):
        KEY_ROTATION_PATH.parent.mkdir(exist_ok=True)
        KEY_ROTATION_PATH.write_text(
            json.dumps({"keys": self._keys, "updated_at": ""}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def add_key(self, provider: str, key: str):
        if provider not in self._keys:
            self._keys[provider] = []
        if key not in self._keys[provider]:
            self._keys[provider].append(key)
        self._save()

    def remove_key(self, provider: str, key: str):
        if provider in self._keys and key in self._keys[provider]:
            self._keys[provider].remove(key)
            self._save()

    def get_next_key(self, provider: str) -> Optional[str]:
        provider_keys = self._keys.get(provider, [])
        if not provider_keys:
            return None
        if provider not in self._indices:
            self._indices[provider] = 0
        idx = self._indices[provider]
        key = provider_keys[idx % len(provider_keys)]
        self._indices[provider] = (idx + 1) % len(provider_keys)
        return key

    def get_key_at(self, provider: str, index: int) -> Optional[str]:
        provider_keys = self._keys.get(provider, [])
        if 0 <= index < len(provider_keys):
            return provider_keys[index]
        return None

    def count(self, provider: str) -> int:
        return len(self._keys.get(provider, []))

    def all_providers(self) -> list[str]:
        return list(self._keys.keys())


_api_key_rotator_instance: Optional[ApiKeyRotator] = None


def get_api_key_rotator() -> ApiKeyRotator:
    global _api_key_rotator_instance
    if _api_key_rotator_instance is None:
        _api_key_rotator_instance = ApiKeyRotator()
    return _api_key_rotator_instance
