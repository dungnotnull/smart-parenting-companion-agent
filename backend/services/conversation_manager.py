from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from backend.models import ConversationTurn, SessionLocal
from backend.services.encryption import decrypt, encrypt


class ConversationManager:
    MAX_HISTORY_TURNS = 10

    def __init__(self):
        self._db: Optional[Session] = None

    @property
    def db(self) -> Session:
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def start_session(self, child_id: int) -> str:
        return str(uuid4())

    def save_turn(
        self,
        child_id: int,
        session_id: str,
        role: str,
        content: str,
        emotion: Optional[str] = None,
        evidence_level: Optional[str] = None,
        safety_triggered: bool = False,
        llm_provider: Optional[str] = None,
        token_count: int = 0,
        cost_estimate: float = 0.0,
    ):
        turn = ConversationTurn(
            child_id=child_id,
            session_id=session_id,
            role=role,
            content_encrypted=encrypt(content),
            emotion=emotion,
            evidence_level=evidence_level,
            safety_triggered=safety_triggered,
            llm_provider_used=llm_provider,
            token_count=token_count,
            cost_estimate=cost_estimate,
        )
        self.db.add(turn)
        self.db.commit()

    def get_recent_history(self, child_id: int, session_id: str, limit: int = MAX_HISTORY_TURNS) -> list[dict]:
        turns = (
            self.db.query(ConversationTurn)
            .filter(
                ConversationTurn.child_id == child_id,
                ConversationTurn.session_id == session_id,
            )
            .order_by(ConversationTurn.created_at.desc())
            .limit(limit)
            .all()
        )
        history: list[dict] = []
        for turn in reversed(turns):
            history.append({
                "role": turn.role,
                "content": decrypt(turn.content_encrypted),
                "emotion": turn.emotion,
            })
        return history

    def build_history_context(self, child_id: int, session_id: str) -> str:
        history = self.get_recent_history(child_id, session_id)
        if not history:
            return ""

        lines = ["## Recent Conversation History"]
        for turn in history:
            role_label = "Parent" if turn["role"] == "user" else "Assistant"
            lines.append(f"{role_label}: {turn['content']}")
        return "\n".join(lines)

    def close(self):
        if self._db:
            self._db.close()
            self._db = None


_conversation_manager_instance: Optional[ConversationManager] = None


def get_conversation_manager() -> ConversationManager:
    global _conversation_manager_instance
    if _conversation_manager_instance is None:
        _conversation_manager_instance = ConversationManager()
    return _conversation_manager_instance
