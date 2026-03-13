# models/doctor.py

from __future__ import annotations
from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base  # ✅ Sirf ye rakho


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    specialization: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str | None] = mapped_column(String(255), nullable=True)
    department_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    floor: Mapped[str | None] = mapped_column(String(100), nullable=True)
    fee: Mapped[float | None] = mapped_column(Float, nullable=True)
    available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    slots: Mapped[list["DoctorSlot"]] = relationship("DoctorSlot", back_populates="doctor")

    def __repr__(self) -> str:
        return f"<Doctor(id={self.id}, name={self.name!r})>"