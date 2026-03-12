# agent/voice_agent.py

import json
import sys
import os
import asyncio
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, function_tool
from livekit.agents import Agent, AgentSession
from livekit.plugins import openai, silero
from agent.prompts import SYSTEM_PROMPT
from agent.tools import (
    find_doctor,
    get_available_slots,
    book_appointment,
    cancel_user_appointment,
    check_appointment_status,
    reschedule_appointment,
    emergency_triage,
    get_internal_location,
    get_hospital_info,
    save_voice_log,
)
from database import SessionLocal
from crud.voice_session import get_session_by_livekit_sid, create_voice_session
from schemas.voice_session import VoiceSessionCreate


# ✅ Fix 1 - All tools async def
@function_tool()
async def find_doctor_tool(symptoms: str) -> str:
    """Find a doctor based on patient symptoms"""
    return json.dumps(find_doctor(symptoms))


@function_tool()
async def get_slots_tool(doctor_id: int) -> str:
    """Get available appointment slots for a doctor"""
    db = SessionLocal()
    try:
        return json.dumps(get_available_slots(db, doctor_id))
    finally:
        db.close()


@function_tool()
async def book_appointment_tool(user_id: int, doctor_id: int, slot_id: int) -> str:
    """Book an appointment for the patient"""
    db = SessionLocal()
    try:
        return json.dumps(book_appointment(db, user_id, doctor_id, slot_id))
    finally:
        db.close()


@function_tool()
async def cancel_appointment_tool(appointment_id: int) -> str:
    """Cancel an existing appointment"""
    db = SessionLocal()
    try:
        return json.dumps(cancel_user_appointment(db, appointment_id))
    finally:
        db.close()


@function_tool()
async def check_status_tool(appointment_id: int) -> str:
    """Check status of an existing appointment"""
    db = SessionLocal()
    try:
        return json.dumps(check_appointment_status(db, appointment_id))
    finally:
        db.close()


@function_tool()
async def reschedule_tool(appointment_id: int, new_slot_id: int) -> str:
    """Reschedule an existing appointment to a new slot"""
    db = SessionLocal()
    try:
        return json.dumps(reschedule_appointment(db, appointment_id, new_slot_id))
    finally:
        db.close()


@function_tool()
async def emergency_tool(situation: str) -> str:
    """Handle emergency situations like chest pain or unconscious patient"""
    return json.dumps(emergency_triage(situation))


@function_tool()
async def location_tool(place: str) -> str:
    """Find internal hospital locations like pharmacy or ward"""
    return json.dumps(get_internal_location(place))


@function_tool()
async def hospital_info_tool() -> str:
    """Get hospital info like address and emergency number"""
    return json.dumps(get_hospital_info())


def extract_user_id_from_room(room_name: str) -> int | None:
    try:
        return int(room_name.split("_")[-1])
    except Exception:
        return None


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    room_name = ctx.room.name

    user_id = None
    if ctx.room.metadata:
        try:
            user_id = int(ctx.room.metadata)
        except Exception:
            pass

    if not user_id:
        user_id = extract_user_id_from_room(room_name)

    print(f"[AGENT] Room: {room_name} | User ID: {user_id}")

    db = SessionLocal()
    try:
        session_obj = get_session_by_livekit_sid(db, room_name)
        if not session_obj:
            session_obj = create_voice_session(db, VoiceSessionCreate(
                user_id=user_id,
                livekit_sid=room_name,
            ))
            print(f"[AGENT] New session created: {session_obj.id}")
        else:
            if session_obj.user_id is None and user_id:
                session_obj.user_id = user_id
                db.commit()
            print(f"[AGENT] Existing session found: {session_obj.id}")
        session_id = session_obj.id
    finally:
        db.close()

    dynamic_prompt = SYSTEM_PROMPT
    if user_id:
        dynamic_prompt += (
            f"\n\n## Current User"
            f"\n- User ID: {user_id}"
            f"\n- Always use user_id={user_id} when booking or cancelling appointments."
        )

    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(voice="alloy"),
    )

    last_user_transcript = {"text": ""}

    @session.on("user_input_transcribed")
    def on_user_transcribed(event) -> None:
        if hasattr(event, "is_final") and event.is_final:
            last_user_transcript["text"] = event.transcript
            print(f"[TRANSCRIPT] {event.transcript}")

    async def _save_log(event) -> None:
        try:
            item = event.item
            if hasattr(item, "role") and item.role == "assistant":

                # ✅ Fix 2 - content list ho sakta hai
                agent_response = ""
                if hasattr(item, "content") and item.content:
                    if isinstance(item.content, list):
                        agent_response = " ".join(
                            c if isinstance(c, str) else getattr(c, "text", "")
                            for c in item.content
                        )
                    else:
                        agent_response = str(item.content)

                transcript = last_user_transcript["text"]
                if not transcript:
                    return

                is_emergency = any(word in transcript.lower() for word in [
                    "chest pain", "can't breathe", "unconscious",
                    "severe bleeding", "stroke", "heart attack"
                ])

                db = SessionLocal()
                try:
                    save_voice_log(
                        db=db,
                        session_id=session_id,
                        transcript=transcript,
                        ai_response=agent_response,
                        sentiment="neutral",
                        is_emergency=is_emergency,
                    )
                    print(f"[LOG SAVED] session={session_id} emergency={is_emergency}")
                finally:
                    db.close()

                last_user_transcript["text"] = ""
        except Exception as e:
            print(f"[LOG ERROR] {e}")

    @session.on("conversation_item_added")
    def on_conversation_item(event) -> None:
        asyncio.create_task(_save_log(event))

    await session.start(
        room=ctx.room,
        agent=Agent(
            instructions=dynamic_prompt,
            tools=[
                find_doctor_tool,
                get_slots_tool,
                book_appointment_tool,
                cancel_appointment_tool,
                check_status_tool,
                reschedule_tool,
                emergency_tool,
                location_tool,
                hospital_info_tool,
            ],
        ),
    )

    await session.say(
        "Hello! Welcome to City Hospital. I am Eve, your voice assistant. How can I help you today?",
        allow_interruptions=True,
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))