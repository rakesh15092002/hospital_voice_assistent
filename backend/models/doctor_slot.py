from __future__ import annotations

from datetime import datetime
from sqlalchemy import Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class DoctorSlot(Base):
    __tablename__ = "doctors_slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    doctor_id: Mapped[int | None] = mapped_column(Integer, nullable=True)  # ForeignKey hata diya
    start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_booked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    appointment: Mapped["Appointment | None"] = relationship("Appointment", back_populates="slot")

    def __repr__(self) -> str:
        return f"<DoctorSlot(id={self.id}, doctor_id={self.doctor_id}, is_booked={self.is_booked})>"