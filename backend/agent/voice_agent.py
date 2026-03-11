import json
import sys
import os
from dotenv import load_dotenv

# .env load karo
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
from crud.voice_session import get_session_by_livekit_sid


class HospitalAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=SYSTEM_PROMPT)

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


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(voice="alloy"),
    )

    await session.start(
        room=ctx.room,
        agent=HospitalAssistant(),
    )

    await session.say(
        "Hello! Welcome to City Hospital. I am Eve, your voice assistant. How can I help you today?",
        allow_interruptions=True,
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))