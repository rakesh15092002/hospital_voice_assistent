from __future__ import annotations
# models/voice_session.py

from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class VoiceSession(Base):
    __tablename__ = "voice_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    livekit_sid: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, default=func.now(), nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    user: Mapped["User | None"] = relationship("User", back_populates="voice_sessions")
    voice_logs: Mapped[list["VoiceLog"]] = relationship("VoiceLog", back_populates="session")

    def __repr__(self) -> str:
        return f"<VoiceSession(id={self.id}, livekit_sid={self.livekit_sid!r}, user_id={self.user_id})>"