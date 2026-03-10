# schemas/voice_session.py

from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.voice_log import VoiceLogResponse


# --- Base ---
class VoiceSessionBase(BaseModel):
    user_id: int
    livekit_sid: str


# --- Create ---
class VoiceSessionCreate(VoiceSessionBase):
    pass


# --- Update ---
class VoiceSessionUpdate(BaseModel):
    ended_at: datetime | None = None


# --- Response ---
class VoiceSessionResponse(VoiceSessionBase):
    id: int
    started_at: datetime | None
    ended_at: datetime | None

    model_config = {"from_attributes": True}