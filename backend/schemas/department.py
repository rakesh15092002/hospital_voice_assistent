# schemas/department.py

from __future__ import annotations
from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.hospital import HospitalResponse


# --- Base ---
class DepartmentBase(BaseModel):
    name: str
    floor_num: str
    hospital_id: int


# --- Create ---
class DepartmentCreate(DepartmentBase):
    pass


# --- Update ---
class DepartmentUpdate(BaseModel):
    name: str | None = None
    floor_num: str | None = None
    hospital_id: int | None = None


# --- Response ---
class DepartmentResponse(DepartmentBase):
    id: int

    model_config = {"from_attributes": True}