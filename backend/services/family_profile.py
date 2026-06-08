from datetime import date, datetime
from typing import Optional

from sqlalchemy.orm import Session

from backend.models import ChildProfile, GrowthLog, MilestoneLog, SessionLocal
from backend.services.age_stage_mapper import get_developmental_context
from backend.services.encryption import decrypt, encrypt


class FamilyProfileService:
    def __init__(self):
        self._db: Optional[Session] = None

    @property
    def db(self) -> Session:
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def create_child(
        self,
        family_id: str,
        name: str,
        dob: date,
        sex: str,
        health_notes: str = "",
        preferred_language: str = "en",
    ) -> ChildProfile:
        child = ChildProfile(
            family_id=family_id,
            name_encrypted=encrypt(name),
            dob=dob,
            sex=sex,
            health_notes_encrypted=encrypt(health_notes),
            preferred_language=preferred_language,
        )
        self.db.add(child)
        self.db.commit()
        self.db.refresh(child)
        return child

    def get_child(self, child_id: int) -> Optional[dict]:
        child = self.db.query(ChildProfile).filter(ChildProfile.id == child_id).first()
        if child is None:
            return None
        ctx = get_developmental_context(child.dob)
        return {
            "id": child.id,
            "family_id": child.family_id,
            "name": decrypt(child.name_encrypted),
            "dob": child.dob.isoformat(),
            "sex": child.sex,
            "health_notes": decrypt(child.health_notes_encrypted),
            "preferred_language": child.preferred_language,
            "developmental_context": ctx,
        }

    def list_children(self, family_id: str) -> list[dict]:
        children = (
            self.db.query(ChildProfile)
            .filter(ChildProfile.family_id == family_id)
            .all()
        )
        results: list[dict] = []
        for c in children:
            ctx = get_developmental_context(c.dob)
            results.append({
                "id": c.id,
                "name": decrypt(c.name_encrypted),
                "dob": c.dob.isoformat(),
                "sex": c.sex,
                "preferred_language": c.preferred_language,
                "stage": ctx["stage"],
                "age_months": ctx["age_months"],
            })
        return results

    def update_child(self, child_id: int, **kwargs) -> Optional[ChildProfile]:
        child = self.db.query(ChildProfile).filter(ChildProfile.id == child_id).first()
        if child is None:
            return None
        if "name" in kwargs:
            child.name_encrypted = encrypt(kwargs["name"])
        if "health_notes" in kwargs:
            child.health_notes_encrypted = encrypt(kwargs["health_notes"])
        if "preferred_language" in kwargs:
            child.preferred_language = kwargs["preferred_language"]
        child.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(child)
        return child

    def log_milestone(
        self,
        child_id: int,
        domain: str,
        milestone_label: str,
        achieved_date: date,
        notes: str = "",
    ) -> MilestoneLog:
        milestone = MilestoneLog(
            child_id=child_id,
            domain=domain,
            milestone_label=milestone_label,
            achieved_date=achieved_date,
            notes_encrypted=encrypt(notes),
        )
        self.db.add(milestone)
        self.db.commit()
        self.db.refresh(milestone)
        return milestone

    def get_milestones(self, child_id: int) -> list[dict]:
        logs = (
            self.db.query(MilestoneLog)
            .filter(MilestoneLog.child_id == child_id)
            .order_by(MilestoneLog.achieved_date.desc())
            .all()
        )
        return [
            {
                "id": l.id,
                "domain": l.domain,
                "milestone_label": l.milestone_label,
                "achieved_date": l.achieved_date.isoformat(),
                "notes": decrypt(l.notes_encrypted),
            }
            for l in logs
        ]

    def log_growth(
        self,
        child_id: int,
        measured_date: date,
        weight_kg: Optional[float] = None,
        height_cm: Optional[float] = None,
        head_circumference_cm: Optional[float] = None,
    ) -> GrowthLog:
        entry = GrowthLog(
            child_id=child_id,
            measured_date=measured_date,
            weight_kg=weight_kg,
            height_cm=height_cm,
            head_circumference_cm=head_circumference_cm,
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_growth_logs(self, child_id: int) -> list[dict]:
        logs = (
            self.db.query(GrowthLog)
            .filter(GrowthLog.child_id == child_id)
            .order_by(GrowthLog.measured_date.desc())
            .all()
        )
        return [
            {
                "id": l.id,
                "measured_date": l.measured_date.isoformat(),
                "weight_kg": l.weight_kg,
                "height_cm": l.height_cm,
                "head_circumference_cm": l.head_circumference_cm,
            }
            for l in logs
        ]

    def close(self):
        if self._db:
            self._db.close()
            self._db = None


_family_profile_service_instance: Optional[FamilyProfileService] = None


def get_family_profile_service() -> FamilyProfileService:
    global _family_profile_service_instance
    if _family_profile_service_instance is None:
        _family_profile_service_instance = FamilyProfileService()
    return _family_profile_service_instance
