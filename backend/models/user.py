from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=func.now(), nullable=True)

    # Relationships
    voice_sessions: Mapped[list["VoiceSession"]] = relationship("VoiceSession", back_populates="user")
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name!r}, email={self.email!r})>"