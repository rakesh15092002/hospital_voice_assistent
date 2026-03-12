# agent/voice_agent.py

import json
import sys
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
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


class HospitalAssistant(Agent):
    def __init__(self, instructions: str) -> None:
        super().__init__(instructions=instructions)

    async def find_doctor_tool(self, symptoms: str) -> str:
        """Find a doctor based on patient symptoms"""
        result = find_doctor(symptoms)
        return json.dumps(result)

    async def get_slots_tool(self, doctor_id: int) -> str:
        """Get available appointment slots for a doctor"""
        db = SessionLocal()
        try:
            result = get_available_slots(db, doctor_id)
            return json.dumps(result)
        finally:
            db.close()

    async def book_appointment_tool(self, user_id: int, doctor_id: int, slot_id: int) -> str:
        """Book an appointment for the patient"""
        db = SessionLocal()
        try:
            result = book_appointment(db, user_id, doctor_id, slot_id)
            return json.dumps(result)
        finally:
            db.close()

    async def cancel_appointment_tool(self, appointment_id: int) -> str:
        """Cancel an existing appointment"""
        db = SessionLocal()
        try:
            result = cancel_user_appointment(db, appointment_id)
            return json.dumps(result)
        finally:
            db.close()

    async def check_status_tool(self, appointment_id: int) -> str:
        """Check status of an existing appointment"""
        db = SessionLocal()
        try:
            result = check_appointment_status(db, appointment_id)
            return json.dumps(result)
        finally:
            db.close()

    async def reschedule_tool(self, appointment_id: int, new_slot_id: int) -> str:
        """Reschedule an existing appointment to a new slot"""
        db = SessionLocal()
        try:
            result = reschedule_appointment(db, appointment_id, new_slot_id)
            return json.dumps(result)
        finally:
            db.close()

    async def emergency_tool(self, situation: str) -> str:
        """Handle emergency situations immediately"""
        result = emergency_triage(situation)
        return json.dumps(result)

    async def location_tool(self, place: str) -> str:
        """Find internal hospital locations like pharmacy, ward, cafeteria"""
        result = get_internal_location(place)
        return json.dumps(result)

    async def hospital_info_tool(self) -> str:
        """Get hospital information like timing, address, emergency number"""
        result = get_hospital_info()
        return json.dumps(result)


def extract_user_id_from_room(room_name: str) -> int | None:
    """Extract user_id from room name — hospital_room_4 -> 4"""
    try:
        parts = room_name.split("_")
        return int(parts[-1])
    except Exception:
        return None


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    room_name = ctx.room.name

    # Get user_id — first try metadata, then extract from room name
    user_id = None
    if ctx.room.metadata:
        try:
            user_id = int(ctx.room.metadata)
        except Exception:
            pass

    if not user_id:
        user_id = extract_user_id_from_room(room_name)

    print(f"[AGENT] Room: {room_name} | User ID: {user_id}")

    # Get or create voice session in DB
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

    # Pass user_id to agent in system prompt
    dynamic_prompt = SYSTEM_PROMPT
    if user_id:
        dynamic_prompt += f"\n\n## Current User\n- User ID: {user_id}\n- Always use this exact user_id={user_id} when calling book_appointment_tool or cancel_appointment_tool."

    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(voice="alloy"),
    )

    # Store last user transcript
    last_user_transcript = {"text": ""}

    @session.on("user_input_transcribed")
    def on_user_transcribed(event) -> None:
        if hasattr(event, "is_final") and event.is_final:
            last_user_transcript["text"] = event.transcript
            print(f"[TRANSCRIPT] {event.transcript}")

    @session.on("conversation_item_added")
    def on_conversation_item(event) -> None:
        try:
            item = event.item
            if hasattr(item, "role") and item.role == "assistant":
                agent_response = ""
                if hasattr(item, "text_content"):
                    agent_response = item.text_content or ""

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
                        is_emergency=is_emergency,
                    )
                    print(f"[LOG SAVED] session={session_id} emergency={is_emergency}")
                finally:
                    db.close()

                last_user_transcript["text"] = ""
        except Exception as e:
            print(f"[LOG ERROR] {e}")

    await session.start(
        room=ctx.room,
        agent=HospitalAssistant(instructions=dynamic_prompt),
    )

    await session.say(
        "Hello! Welcome to City Hospital. I am Eve, your voice assistant. How can I help you today?",
        allow_interruptions=True,
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))