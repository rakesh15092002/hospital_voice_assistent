from __future__ import annotations

from sqlalchemy import Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class VoiceLog(Base):
    __tablename__ = "voice_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    session_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("voice_sessions.id"), nullable=True)
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_response: Mapped[str | None] = mapped_column(Text, nullable=True)
    sentiment: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_emergency: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    session: Mapped["VoiceSession | None"] = relationship("VoiceSession", back_populates="voice_logs")

    def __repr__(self) -> str:
        return f"<VoiceLog(id={self.id}, session_id={self.session_id}, is_emergency={self.is_emergency})>"