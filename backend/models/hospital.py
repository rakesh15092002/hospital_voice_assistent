from __future__ import annotations

from sqlalchemy import Integer, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Hospital(Base):
    __tablename__ = "hospital"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    emergency_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    opening_time: Mapped[str | None] = mapped_column(Time, nullable=True)

    # Relationships
    departments: Mapped[list["Department"]] = relationship("Department", back_populates="hospital")

    def __repr__(self) -> str:
        return f"<Hospital(id={self.id}, name={self.name!r})>"