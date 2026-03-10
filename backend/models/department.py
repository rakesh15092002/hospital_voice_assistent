from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    hospital_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("hospital.id"), nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    floor_num: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Relationships
    hospital: Mapped["Hospital | None"] = relationship("Hospital", back_populates="departments")
    doctors: Mapped[list["Doctor"]] = relationship("Doctor", back_populates="department")

    def __repr__(self) -> str:
        return f"<Department(id={self.id}, name={self.name!r}, floor={self.floor_num!r})>"