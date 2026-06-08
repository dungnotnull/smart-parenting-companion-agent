from typing import Optional


class ResearchSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        self.model_name = model_name
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            try:
                from transformers import pipeline
                self._pipeline = pipeline(
                    "summarization",
                    model=self.model_name,
                    max_length=130,
                    min_length=30,
                    truncation=True,
                )
            except Exception:
                self._pipeline = False
        return self._pipeline if self._pipeline is not False else None

    def summarize(self, text: str, max_input_length: int = 1024) -> str:
        pipe = self.pipeline
        if pipe is None:
            return text[:300] + "..." if len(text) > 300 else text

        truncated = text[:max_input_length]
        try:
            result = pipe(truncated)
            return result[0]["summary_text"]
        except Exception:
            return truncated[:200] + "..." if len(truncated) > 200 else truncated


_research_summarizer_instance: Optional[ResearchSummarizer] = None


def get_research_summarizer() -> ResearchSummarizer:
    global _research_summarizer_instance
    if _research_summarizer_instance is None:
        _research_summarizer_instance = ResearchSummarizer()
    return _research_summarizer_instance
