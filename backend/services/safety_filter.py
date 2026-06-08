from datetime import date
from typing import Optional

EMERGENCY_KEYWORDS: list[str] = [
    "not breathing",
    "stopped breathing",
    "turning blue",
    "seizure",
    "convulsion",
    "unconscious",
    "choking",
    "swallowed poison",
    "burned",
    "bleeding heavily",
    "won't wake up",
    "fever 104",
    "fever over 104",
    "fever 105",
    "neck stiffness",
    "purple rash",
    "meningitis",
    "anaphylaxis",
    "severe allergic",
    "overdose",
    "drowning",
    "electrocuted",
    "broken bone",
    "head injury",
    "lost consciousness",
    "can't breathe",
    "difficulty breathing",
    "severe burn",
    "carbon monoxide",
    "infant fever 38",
    "newborn fever",
    "baby fever 39",
    "infant under 3 months fever",
]

EMERGENCY_RESPONSE = (
    "⚠️ **This sounds like a potential medical emergency.**\n\n"
    "Please **stop using this chat immediately** and:\n"
    "- Call **115** (Vietnam) or your local emergency number\n"
    "- Go to the nearest **hospital emergency department**\n"
    "- Contact your **pediatrician** right away\n\n"
    "This AI companion is not equipped to handle medical emergencies. "
    "Your child's safety is the absolute priority."
)

HIGH_CONCERN_KEYWORDS: list[str] = [
    "suicide",
    "kill myself",
    "want to die",
    "self-harm",
    "cutting myself",
]

HIGH_CONCERN_RESPONSE = (
    "💙 **I'm hearing things that deeply concern me about your child's safety.**\n\n"
    "Please reach out immediately:\n"
    "- **Vietnam Mental Health Hotline**: 1900 6233\n"
    "- **Child helpline (Vietnam)**: 111\n"
    "- Go to the nearest hospital emergency department\n"
    "- Contact a mental health professional\n\n"
    "Your child needs urgent professional support. This conversation is not a substitute."
)


def check_safety(text: str) -> dict:
    text_lower = text.lower()
    triggered_high = [kw for kw in HIGH_CONCERN_KEYWORDS if kw in text_lower]
    if triggered_high:
        return {
            "safe": False,
            "level": "critical",
            "message": HIGH_CONCERN_RESPONSE,
            "keywords_matched": triggered_high,
        }

    triggered_emergency = [kw for kw in EMERGENCY_KEYWORDS if kw in text_lower]
    if triggered_emergency:
        return {
            "safe": False,
            "level": "emergency",
            "message": EMERGENCY_RESPONSE,
            "keywords_matched": triggered_emergency,
        }

    return {"safe": True, "level": "ok", "message": None, "keywords_matched": []}
