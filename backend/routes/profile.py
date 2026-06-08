from datetime import date
from typing import Optional

from fastapi.routing import APIRouter
from pydantic import BaseModel

from backend.services.family_profile import get_family_profile_service

router = APIRouter(prefix="/api", tags=["profile"])

fps = get_family_profile_service


class CreateChildRequest(BaseModel):
    family_id: str = "default"
    name: str
    dob: str
    sex: str
    health_notes: str = ""
    preferred_language: str = "en"


class UpdateChildRequest(BaseModel):
    name: Optional[str] = None
    health_notes: Optional[str] = None
    preferred_language: Optional[str] = None


class LogMilestoneRequest(BaseModel):
    child_id: int
    domain: str
    milestone_label: str
    achieved_date: str
    notes: str = ""


class LogGrowthRequest(BaseModel):
    child_id: int
    measured_date: str
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    head_circumference_cm: Optional[float] = None


@router.post("/profile")
async def create_child(req: CreateChildRequest):
    child = fps().create_child(
        family_id=req.family_id,
        name=req.name,
        dob=date.fromisoformat(req.dob),
        sex=req.sex,
        health_notes=req.health_notes,
        preferred_language=req.preferred_language,
    )
    return fps().get_child(child.id)


@router.get("/profile/{child_id}")
async def get_child(child_id: int):
    child = fps().get_child(child_id)
    if child is None:
        return {"error": "Child profile not found"}
    return child


@router.put("/profile/{child_id}")
async def update_child(child_id: int, req: UpdateChildRequest):
    updated = fps().update_child(
        child_id,
        **{k: v for k, v in req.model_dump().items() if v is not None},
    )
    if updated is None:
        return {"error": "Child profile not found"}
    return fps().get_child(child_id)


@router.get("/profile/family/{family_id}")
async def list_children(family_id: str):
    return fps().list_children(family_id)


@router.post("/profile/milestone")
async def log_milestone(req: LogMilestoneRequest):
    milestone = fps().log_milestone(
        child_id=req.child_id,
        domain=req.domain,
        milestone_label=req.milestone_label,
        achieved_date=date.fromisoformat(req.achieved_date),
        notes=req.notes,
    )
    return {"id": milestone.id, "status": "logged"}


@router.get("/profile/{child_id}/milestones")
async def get_milestones(child_id: int):
    return fps().get_milestones(child_id)


@router.post("/profile/growth")
async def log_growth(req: LogGrowthRequest):
    entry = fps().log_growth(
        child_id=req.child_id,
        measured_date=date.fromisoformat(req.measured_date),
        weight_kg=req.weight_kg,
        height_cm=req.height_cm,
        head_circumference_cm=req.head_circumference_cm,
    )
    return {"id": entry.id, "status": "logged"}


@router.get("/profile/{child_id}/growth")
async def get_growth_logs(child_id: int):
    return fps().get_growth_logs(child_id)
