from datetime import datetime, timezone
from typing import Optional

from backend.services.llm_router import get_llm_router


class ConversationSummarizer:
    def __init__(self):
        self.llm = get_llm_router()

    async def summarize_history(self, turns: list[dict]) -> str:
        if len(turns) < 3:
            return ""

        transcript = "\n".join(
            f"{'Parent' if t['role'] == 'user' else 'Assistant'}: {t['content']}"
            for t in turns
        )

        system_prompt = (
            "You are a conversation summarizer for a parenting companion AI. "
            "Summarize the conversation below into 3-5 bullet points capturing: "
            "key topics discussed, parenting concerns raised, advice given, "
            "milestones mentioned, and emotional context. "
            "Be concise and factual — this summary will be used as memory context "
            "for future turns in this session."
        )

        try:
            summary = await self.llm.generate(system_prompt, transcript)
            return summary
        except Exception:
            return self._fallback_summarize(turns)

    def _fallback_summarize(self, turns: list[dict]) -> str:
        topics: set[str] = set()
        for turn in turns:
            text = turn["content"].lower()
            for topic_kw in ["sleep", "feed", "eat", "milestone", "development",
                              "vaccine", "tantrum", "behavior", "school", "sick",
                              "fever", "anxiety", "screen", "language", "walk",
                              "crawl", "talk", "nutrition", "growth"]:
                if topic_kw in text:
                    topics.add(topic_kw)

        if not topics:
            return "General parenting conversation."

        topic_labels = {
            "sleep": "sleep",
            "feed": "feeding", "eat": "feeding", "nutrition": "nutrition",
            "milestone": "developmental milestones", "development": "development",
            "vaccine": "vaccination",
            "tantrum": "behavior management", "behavior": "behavior",
            "school": "school/education",
            "sick": "illness", "fever": "fever management",
            "anxiety": "anxiety/mental health",
            "screen": "screen time",
            "language": "language development",
            "walk": "motor development", "crawl": "motor development",
            "talk": "language development",
            "growth": "growth tracking",
        }

        labeled = list(set(topic_labels.get(t, t) for t in topics))
        return f"Topics discussed: {', '.join(sorted(labeled))}."


_conversation_summarizer_instance: Optional[ConversationSummarizer] = None


def get_conversation_summarizer() -> ConversationSummarizer:
    global _conversation_summarizer_instance
    if _conversation_summarizer_instance is None:
        _conversation_summarizer_instance = ConversationSummarizer()
    return _conversation_summarizer_instance
