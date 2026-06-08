import json
from datetime import date
from typing import Optional
from uuid import uuid4

from fastapi import WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter
from pydantic import BaseModel

from backend.services.age_stage_mapper import get_developmental_context
from backend.services.conversation_manager import get_conversation_manager
from backend.services.emotion_detector import get_emotion_detector
from backend.services.family_profile import get_family_profile_service
from backend.services.llm_router import DISCLAIMER, get_llm_router
from backend.services.rag_pipeline import get_rag_pipeline
from backend.services.safety_filter import check_safety

router = APIRouter(prefix="/api", tags=["chat"])

fps = get_family_profile_service
cm = get_conversation_manager
rag = get_rag_pipeline
llm = get_llm_router
emotion = get_emotion_detector


class ChatPayload(BaseModel):
    child_id: int
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    safety_triggered: bool
    emotion: Optional[dict] = None
    evidence_sources: list[dict] = []


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatPayload):
    session_id = payload.session_id or cm().start_session(payload.child_id)

    safety_result = check_safety(payload.message)
    if not safety_result["safe"]:
        cm().save_turn(
            child_id=payload.child_id,
            session_id=session_id,
            role="user",
            content=payload.message,
            safety_triggered=True,
        )
        cm().save_turn(
            child_id=payload.child_id,
            session_id=session_id,
            role="assistant",
            content=safety_result["message"],
            safety_triggered=True,
        )
        return ChatResponse(
            response=safety_result["message"],
            session_id=session_id,
            safety_triggered=True,
        )

    child = fps().get_child(payload.child_id)
    if child is None:
        return ChatResponse(
            response="Child profile not found. Please create a profile first.",
            session_id=session_id,
            safety_triggered=False,
        )

    dev_ctx = child["developmental_context"]
    child_context = (
        f"Child: {child['name']}, Age: {dev_ctx['age_months']} months, "
        f"Stage: {dev_ctx['stage']}, Sex: {child['sex']}\n"
        f"Erikson Stage: {dev_ctx['erikson_stage']}\n"
        f"Piaget Stage: {dev_ctx['piaget_stage']}\n"
        f"Key Milestones: {', '.join(dev_ctx['key_milestones'])}\n"
        f"Stage Guidance: {dev_ctx['stage_guidance']}"
    )

    emotion_result = emotion().detect(payload.message)
    register = emotion().get_register_modifier(emotion_result["top_emotion"])

    cm().save_turn(
        child_id=payload.child_id,
        session_id=session_id,
        role="user",
        content=payload.message,
        emotion=emotion_result["top_emotion"],
    )

    _, rag_context = rag().query(payload.message, child_context)

    history_context = cm().build_history_context(payload.child_id, session_id)

    register_prompt = {
        "warm_reassuring": (
            "The parent's message indicates distress or anxiety. "
            "Frame your response with warmth, empathy, and reassurance while providing accurate evidence-based information."
        ),
        "celebratory": (
            "The parent sounds positive and engaged. "
            "Match their tone with warmth and encouragement while providing evidence-based information."
        ),
        "calm_informational": (
            "The parent is asking an informational question. "
            "Provide clear, calm, evidence-based information without unnecessary emotional framing."
        ),
    }.get(register, "Provide evidence-based parenting guidance.")

    system_prompt = (
        f"You are Smart Parenting Companion, an evidence-based AI parenting guide.\n\n"
        f"## Child Developmental Context\n{child_context}\n\n"
        f"## Tone Guidance\n{register_prompt}\n\n"
        f"## Evidence-Based Knowledge Context\n{rag_context}\n\n"
        f"{history_context}\n\n"
        f"## Response Guidelines\n"
        f"- Ground your answer in the provided evidence-based knowledge context\n"
        f"- Reference specific sources with their evidence level badge (RCT, guideline, etc.)\n"
        f"- Calibrate all advice to the child's specific age and developmental stage\n"
        f"- If the evidence is insufficient, acknowledge the limits of current research\n"
    )

    response_text = await llm().generate(system_prompt, payload.message)
    full_response = response_text + DISCLAIMER

    cm().save_turn(
        child_id=payload.child_id,
        session_id=session_id,
        role="assistant",
        content=full_response,
        evidence_level="mixed",
    )

    return ChatResponse(
        response=full_response,
        session_id=session_id,
        safety_triggered=False,
        emotion={"top": emotion_result["top_emotion"], "register": register},
    )


@router.websocket("/chat/stream")
async def chat_stream(websocket: WebSocket):
    await websocket.accept()

    try:
        data = await websocket.receive_text()
        payload_raw = json.loads(data)
        child_id = payload_raw.get("child_id")
        message = payload_raw.get("message", "")
        session_id = payload_raw.get("session_id", str(uuid4()))

        if not child_id:
            await websocket.send_text(json.dumps({"type": "error", "content": "child_id is required"}))
            await websocket.close()
            return

        safety_result = check_safety(message)
        if not safety_result["safe"]:
            await websocket.send_text(json.dumps({
                "type": "safety_alert",
                "content": safety_result["message"],
                "level": safety_result["level"],
                "session_id": session_id,
            }))
            await websocket.close()
            return

        child = fps().get_child(int(child_id))
        if child is None:
            await websocket.send_text(json.dumps({
                "type": "error",
                "content": "Child profile not found.",
                "session_id": session_id,
            }))
            await websocket.close()
            return

        dev_ctx = child["developmental_context"]
        child_context = (
            f"Child: {child['name']}, Age: {dev_ctx['age_months']} months, "
            f"Stage: {dev_ctx['stage']}, Sex: {child['sex']}\n"
            f"Erikson Stage: {dev_ctx['erikson_stage']}\n"
            f"Piaget Stage: {dev_ctx['piaget_stage']}\n"
            f"Key Milestones: {', '.join(dev_ctx['key_milestones'])}\n"
            f"Stage Guidance: {dev_ctx['stage_guidance']}"
        )

        emotion_result = emotion().detect(message)
        register = emotion().get_register_modifier(emotion_result["top_emotion"])

        cm().save_turn(
            child_id=int(child_id),
            session_id=session_id,
            role="user",
            content=message,
            emotion=emotion_result["top_emotion"],
        )

        _, rag_context = rag().query(message, child_context)
        history_context = cm().build_history_context(int(child_id), session_id)

        register_prompt = {
            "warm_reassuring": (
                "The parent's message indicates distress or anxiety. "
                "Frame your response with warmth, empathy, and reassurance while providing accurate evidence-based information."
            ),
            "celebratory": (
                "The parent sounds positive and engaged. "
                "Match their tone with warmth and encouragement while providing evidence-based information."
            ),
            "calm_informational": (
                "The parent is asking an informational question. "
                "Provide clear, calm, evidence-based information without unnecessary emotional framing."
            ),
        }.get(register, "Provide evidence-based parenting guidance.")

        system_prompt = (
            f"You are Smart Parenting Companion, an evidence-based AI parenting guide.\n\n"
            f"## Child Developmental Context\n{child_context}\n\n"
            f"## Tone Guidance\n{register_prompt}\n\n"
            f"## Evidence-Based Knowledge Context\n{rag_context}\n\n"
            f"{history_context}\n\n"
            f"## Response Guidelines\n"
            f"- Ground your answer in the provided evidence-based knowledge context\n"
            f"- Reference specific sources with their evidence level badge\n"
            f"- Calibrate all advice to the child's specific age and developmental stage\n"
            f"- If the evidence is insufficient, acknowledge the limits of current research\n"
        )

        await websocket.send_text(json.dumps({
            "type": "meta",
            "emotion": {"top": emotion_result["top_emotion"], "register": register},
            "session_id": session_id,
        }))

        full_response = ""
        async for token in llm().generate_stream(system_prompt, message):
            full_response += token
            await websocket.send_text(json.dumps({"type": "token", "content": token}))

        full_response += DISCLAIMER
        await websocket.send_text(json.dumps({"type": "token", "content": DISCLAIMER}))
        await websocket.send_text(json.dumps({"type": "done"}))

        cm().save_turn(
            child_id=int(child_id),
            session_id=session_id,
            role="assistant",
            content=full_response,
            evidence_level="mixed",
        )

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_text(json.dumps({"type": "error", "content": str(e)}))
    finally:
        try:
            await websocket.close()
        except Exception:
            pass
