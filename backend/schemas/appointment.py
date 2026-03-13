# schemas/appointment.py

from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional


# --- Status Enum ---
class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


# --- Base ---
class AppointmentBase(BaseModel):
    doctor_id: int
    slot_id: int
    status: AppointmentStatus = AppointmentStatus.pending


# --- Create ---
# user_id optional hai — route mein JWT token se automatically set hoga
class AppointmentCreate(AppointmentBase):
    user_id: Optional[int] = None


# --- Update ---
class AppointmentUpdate(BaseModel):
    status: AppointmentStatus | None = None


# --- Response ---
class AppointmentResponse(AppointmentBase):
    id: int
    user_id: int | None
    created_at: datetime | None

    model_config = {"from_attributes": True}