# schemas/voice_session.py

from pydantic import BaseModel
from datetime import datetime


# --- Base --- common fields
class VoiceSessionBase(BaseModel):
    user_id: int
    livekit_sid: str


# --- Create --- request body
class VoiceSessionCreate(VoiceSessionBase):
    pass


# --- Update --- only ended_at update hoga
class VoiceSessionUpdate(BaseModel):
    ended_at: datetime | None = None


# --- Response --- what API returns
class VoiceSessionResponse(VoiceSessionBase):
    id: int
    started_at: datetime | None
    ended_at: datetime | None

    model_config = {"from_attributes": True}


# --- Response with Logs --- nested response
class VoiceSessionWithLogs(VoiceSessionResponse):
    from schemas.voice_log import VoiceLogResponse
    voice_logs: list[VoiceLogResponse] = []

    model_config = {"from_attributes": True}