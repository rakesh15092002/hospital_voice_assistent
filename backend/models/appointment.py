from __future__ import annotations

from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    doctor_id: Mapped[int | None] = mapped_column(Integer, nullable=True)  # ForeignKey hata diya
    slot_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("doctors_slots.id"), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=func.now(), nullable=True)

    # Relationships
    user: Mapped["User | None"] = relationship("User", back_populates="appointments")
    slot: Mapped["DoctorSlot | None"] = relationship("DoctorSlot", back_populates="appointment")

    def __repr__(self) -> str:
        return f"<Appointment(id={self.id}, user_id={self.user_id}, doctor_id={self.doctor_id}, status={self.status!r})>"