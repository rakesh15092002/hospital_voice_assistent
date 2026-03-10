from __future__ import annotations
# models/doctor.py

from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    department_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("departments.id"), nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    specialization: Mapped[str | None] = mapped_column(String(255), nullable=True)
    consultation_fee: Mapped[int | None] = mapped_column(Integer, nullable=True)
    symptoms_handled: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    department: Mapped["Department | None"] = relationship("Department", back_populates="doctors")
    slots: Mapped[list["DoctorSlot"]] = relationship("DoctorSlot", back_populates="doctor")
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="doctor")

    def __repr__(self) -> str:
        return f"<Doctor(id={self.id}, name={self.name!r}, specialization={self.specialization!r})>"