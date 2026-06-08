import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from backend.models import ConversationTurn, SessionLocal

logger = logging.getLogger(__name__)

MODEL_PRICING: dict[str, dict[str, float]] = {
    "claude-sonnet-4-6": {"input_per_1k": 0.003, "output_per_1k": 0.015},
    "claude-sonnet-4-20250514": {"input_per_1k": 0.003, "output_per_1k": 0.015},
    "claude-3-opus": {"input_per_1k": 0.015, "output_per_1k": 0.075},
    "gpt-4o": {"input_per_1k": 0.0025, "output_per_1k": 0.01},
    "gpt-4o-mini": {"input_per_1k": 0.00015, "output_per_1k": 0.0006},
    "ollama": {"input_per_1k": 0.0, "output_per_1k": 0.0},
}


STATS_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "token_stats.json"
STATS_PATH.parent.mkdir(exist_ok=True)


def load_stats() -> dict:
    if STATS_PATH.exists():
        try:
            return json.loads(STATS_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"total_tokens": 0, "total_cost": 0.0, "by_provider": {}, "by_date": {}, "requests": 0}


def save_stats(stats: dict):
    STATS_PATH.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    pricing = MODEL_PRICING.get(model, MODEL_PRICING.get("gpt-4o", {"input_per_1k": 0.01, "output_per_1k": 0.01}))
    input_cost = (input_tokens / 1000.0) * pricing["input_per_1k"]
    output_cost = (output_tokens / 1000.0) * pricing["output_per_1k"]
    return round(input_cost + output_cost, 6)


def track_usage(
    provider: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
):
    cost = estimate_cost(model, input_tokens, output_tokens)
    stats = load_stats()

    stats["total_tokens"] += input_tokens + output_tokens
    stats["total_cost"] += cost
    stats["requests"] += 1

    if provider not in stats["by_provider"]:
        stats["by_provider"][provider] = {"tokens": 0, "cost": 0.0, "requests": 0}
    stats["by_provider"][provider]["tokens"] += input_tokens + output_tokens
    stats["by_provider"][provider]["cost"] += cost
    stats["by_provider"][provider]["requests"] += 1

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if today not in stats["by_date"]:
        stats["by_date"][today] = {"tokens": 0, "cost": 0.0, "requests": 0}
    stats["by_date"][today]["tokens"] += input_tokens + output_tokens
    stats["by_date"][today]["cost"] += cost
    stats["by_date"][today]["requests"] += 1

    save_stats(stats)
    logger.debug("Token usage: %d in + %d out = $%.6f (%s/%s)", input_tokens, output_tokens, cost, provider, model)

    return {"input_tokens": input_tokens, "output_tokens": output_tokens, "cost": cost}
