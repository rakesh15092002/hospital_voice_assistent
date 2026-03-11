# schemas/appointment.py

from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


# --- Status Enum ---
class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


# --- Base ---
class AppointmentBase(BaseModel):
    user_id: int
    doctor_id: int
    slot_id: int
    status: AppointmentStatus = AppointmentStatus.pending


# --- Create ---
class AppointmentCreate(AppointmentBase):
    pass


# --- Update ---
class AppointmentUpdate(BaseModel):
    status: AppointmentStatus | None = None


# --- Response ---
class AppointmentResponse(AppointmentBase):
    id: int
    created_at: datetime | None

    model_config = {"from_attributes": True}