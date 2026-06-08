from typing import Optional


class EmotionDetector:
    def __init__(self, model_name: str = "SamLowe/roberta-base-go_emotions"):
        self.model_name = model_name
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            try:
                from transformers import pipeline
                self._pipeline = pipeline(
                    "text-classification",
                    model=self.model_name,
                    top_k=3,
                )
            except Exception:
                self._pipeline = False
        return self._pipeline if self._pipeline is not False else None

    def detect(self, text: str) -> dict:
        pipe = self.pipeline
        if pipe is None:
            return {"top_emotion": "neutral", "confidence": 0.0, "all": []}

        results = pipe(text)
        all_emotions = [
            {"label": r["label"], "score": round(r["score"], 4)}
            for r in (results[0] if isinstance(results, list) else results)
        ]
        top = all_emotions[0] if all_emotions else {"label": "neutral", "score": 0.0}
        return {
            "top_emotion": top["label"],
            "confidence": top["score"],
            "all": all_emotions,
        }

    def get_register_modifier(self, top_emotion: str) -> str:
        warm_emotions = {"sadness", "fear", "anxiety", "anger", "grief", "disappointment", "nervousness"}
        calm_emotions = {"neutral", "curiosity", "surprise", "approval", "realization"}
        positive_emotions = {"joy", "gratitude", "love", "relief", "pride", "excitement", "optimism"}

        if top_emotion in warm_emotions:
            return "warm_reassuring"
        elif top_emotion in positive_emotions:
            return "celebratory"
        else:
            return "calm_informational"


_emotion_detector_instance: Optional[EmotionDetector] = None


def get_emotion_detector() -> EmotionDetector:
    global _emotion_detector_instance
    if _emotion_detector_instance is None:
        _emotion_detector_instance = EmotionDetector()
    return _emotion_detector_instance
