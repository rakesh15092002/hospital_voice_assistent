# agent/voice_agent.py

import json
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from agent.prompts import SYSTEM_PROMPT
from agent.tools import (
    find_doctor,
    get_available_slots,
    book_appointment,
    cancel_user_appointment,
    get_hospital_info,
    save_voice_log,
)
from database import SessionLocal
from crud.voice_session import get_session_by_livekit_sid


# --- Define AI Tools for OpenAI ---
class HospitalAssistantTools(llm.FunctionContext):

    @llm.ai_callable(description="Find a doctor based on patient symptoms")
    async def find_doctor_tool(self, symptoms: str) -> str:
        result = find_doctor(symptoms)
        return json.dumps(result)

    @llm.ai_callable(description="Get available appointment slots for a doctor")
    async def get_slots_tool(self, doctor_id: int) -> str:
        db = SessionLocal()
        try:
            result = get_available_slots(db, doctor_id)
            return json.dumps(result)
        finally:
            db.close()

    @llm.ai_callable(description="Book an appointment for the patient")
    async def book_appointment_tool(
        self,
        user_id: int,
        doctor_id: int,
        slot_id: int
    ) -> str:
        db = SessionLocal()
        try:
            result = book_appointment(db, user_id, doctor_id, slot_id)
            return json.dumps(result)
        finally:
            db.close()

    @llm.ai_callable(description="Cancel an existing appointment")
    async def cancel_appointment_tool(self, appointment_id: int) -> str:
        db = SessionLocal()
        try:
            result = cancel_user_appointment(db, appointment_id)
            return json.dumps(result)
        finally:
            db.close()

    @llm.ai_callable(description="Get hospital information like emergency number and timing")
    async def hospital_info_tool(self) -> str:
        result = get_hospital_info()
        return json.dumps(result)


# --- Main Agent Entry Point ---
async def entrypoint(ctx: JobContext):
    """LiveKit calls this when a user joins the room"""

    # connect to livekit room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # get user_id from room metadata
    user_id = int(ctx.room.metadata) if ctx.room.metadata else None

    # get session from DB
    db = SessionLocal()
    session = get_session_by_livekit_sid(db, ctx.room.name)
    session_id = session.id if session else None
    db.close()

    # setup voice assistant
    assistant = VoiceAssistant(
        vad=silero.VAD.load(),                        # Voice Activity Detection
        stt=openai.STT(),                             # Speech to Text
        llm=openai.LLM(model="gpt-4o-realtime-preview"),  # AI Brain
        tts=openai.TTS(voice="alloy"),                # Text to Speech
        fnc_ctx=HospitalAssistantTools(),             # Tools
        chat_ctx=llm.ChatContext().append(
            role="system",
            text=SYSTEM_PROMPT,
        ),
    )

    # start assistant in room
    assistant.start(ctx.room)

    # greet the user
    await assistant.say(
        "Hello! Welcome to City Hospital. I am Eve, your voice assistant. How can I help you today?",
        allow_interruptions=True,
    )

    # save each conversation turn
    @assistant.on("user_speech_committed")
    def on_user_speech(user_msg: llm.ChatMessage):
        pass  # transcript captured

    @assistant.on("agent_speech_committed")
    def on_agent_speech(agent_msg: llm.ChatMessage):
        if session_id and user_id:
            db = SessionLocal()
            try:
                # check for emergency keywords
                transcript = str(user_id)
                is_emergency = any(word in transcript.lower() for word in [
                    "chest pain", "can't breathe", "unconscious",
                    "severe bleeding", "stroke", "heart attack"
                ])
                save_voice_log(
                    db=db,
                    session_id=session_id,
                    transcript=transcript,
                    ai_response=agent_msg.content,
                    is_emergency=is_emergency,
                )
            finally:
                db.close()


# --- Run Agent ---
if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))