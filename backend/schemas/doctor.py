# schemas/doctor.py

from __future__ import annotations
from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.department import DepartmentResponse


# --- Base ---
class DoctorBase(BaseModel):
    name: str
    specialization: str
    consultation_fee: int
    symptoms_handled: str
    department_id: int


# --- Create ---
class DoctorCreate(DoctorBase):
    pass


# --- Update ---
class DoctorUpdate(BaseModel):
    name: str | None = None
    specialization: str | None = None
    consultation_fee: int | None = None
    symptoms_handled: str | None = None
    department_id: int | None = None


# --- Response ---
class DoctorResponse(DoctorBase):
    id: int

    model_config = {"from_attributes": True}