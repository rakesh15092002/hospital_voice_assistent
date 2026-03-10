# schemas/voice_log.py

from pydantic import BaseModel
from enum import Enum


# --- Sentiment Enum --- only these 3 values allowed
class SentimentType(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"


# --- Base --- common fields
class VoiceLogBase(BaseModel):
    session_id: int
    transcript: str
    ai_response: str
    sentiment: SentimentType = SentimentType.neutral
    is_emergency: bool = False


# --- Create --- request body
class VoiceLogCreate(VoiceLogBase):
    pass


# --- Update --- optional fields
class VoiceLogUpdate(BaseModel):
    transcript: str | None = None
    ai_response: str | None = None
    sentiment: SentimentType | None = None
    is_emergency: bool | None = None


# --- Response --- what API returns
class VoiceLogResponse(VoiceLogBase):
    id: int

    model_config = {"from_attributes": True}


# --- Emergency Logs --- only emergency logs
class VoiceLogEmergency(VoiceLogResponse):
    is_emergency: bool = True

    model_config = {"from_attributes": True}