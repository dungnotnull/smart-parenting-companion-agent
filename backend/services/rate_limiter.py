import time
from collections import defaultdict
from typing import Optional

from fastapi import Request
from fastapi.responses import JSONResponse


class RateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._buckets: dict[str, list[float]] = defaultdict(list)

    def _clean_bucket(self, key: str, now: float):
        cutoff = now - self.window_seconds
        self._buckets[key] = [t for t in self._buckets[key] if t > cutoff]

    def check(self, key: str) -> tuple[bool, dict]:
        now = time.time()
        self._clean_bucket(key, now)
        bucket = self._buckets[key]

        if len(bucket) >= self.max_requests:
            retry_after = int(bucket[0] + self.window_seconds - now) + 1
            return False, {
                "limited": True,
                "retry_after_seconds": retry_after,
                "limit": self.max_requests,
                "window_seconds": self.window_seconds,
                "remaining": 0,
            }

        bucket.append(now)
        remaining = self.max_requests - len(bucket)
        return True, {
            "limited": False,
            "limit": self.max_requests,
            "window_seconds": self.window_seconds,
            "remaining": remaining,
        }

    def get_key(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For", "")
        client_ip = forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else "unknown")
        return f"rate_limit:{client_ip}"


_global_rate_limiter: Optional[RateLimiter] = None


def get_rate_limiter(max_requests: int = 60, window_seconds: int = 60) -> RateLimiter:
    global _global_rate_limiter
    if _global_rate_limiter is None:
        _global_rate_limiter = RateLimiter(max_requests, window_seconds)
    return _global_rate_limiter
