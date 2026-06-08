import asyncio
import logging
import random
from typing import Any, Callable, Coroutine

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
BASE_DELAY_SECONDS = 1.0
MAX_DELAY_SECONDS = 30.0
JITTER_FACTOR = 0.1


def _retryable_exception(e: Exception) -> bool:
    err_msg = str(e).lower()
    retryable_patterns = [
        "rate limit", "too many requests", "429",
        "server error", "500", "502", "503", "504",
        "timeout", "connection reset", "connection refused",
        "temporarily unavailable", "overloaded",
    ]
    return any(p in err_msg for p in retryable_patterns)


async def with_retry(
    fn: Callable[..., Coroutine[Any, Any, Any]],
    *args: Any,
    max_retries: int = MAX_RETRIES,
    base_delay: float = BASE_DELAY_SECONDS,
    max_delay: float = MAX_DELAY_SECONDS,
    **kwargs: Any,
) -> Any:
    last_exception: Optional[Exception] = None

    for attempt in range(max_retries + 1):
        try:
            return await fn(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt == max_retries:
                raise

            if not _retryable_exception(e):
                raise

            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = delay * JITTER_FACTOR * (2 * random.random() - 1)
            total_delay = delay + jitter

            logger.warning(
                "Retry attempt %d/%d after %.1fs for error: %s",
                attempt + 1, max_retries, total_delay, str(e)[:100],
            )
            await asyncio.sleep(total_delay)

    if last_exception:
        raise last_exception
    raise RuntimeError("Retry logic error — unreachable")


async def with_fallback(
    primary_fn: Callable[..., Coroutine[Any, Any, Any]],
    fallback_fn: Callable[..., Coroutine[Any, Any, Any]],
    *args: Any,
    **kwargs: Any,
) -> Any:
    try:
        return await primary_fn(*args, **kwargs)
    except Exception as e:
        logger.warning("Primary call failed: %s. Attempting fallback.", str(e)[:100])
        return await fallback_fn(*args, **kwargs)
