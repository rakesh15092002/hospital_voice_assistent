# schemas/appointment.py

from pydantic import BaseModel
from datetime import datetime
from enum import Enum


# --- Status Enum --- only these 3 values allowed
class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


# --- Base --- common fields
class AppointmentBase(BaseModel):
    user_id: int
    doctor_id: int
    slot_id: int
    status: AppointmentStatus = AppointmentStatus.pending


# --- Create --- request body
class AppointmentCreate(AppointmentBase):
    pass


# --- Update --- optional fields
class AppointmentUpdate(BaseModel):
    status: AppointmentStatus | None = None


# --- Response --- what API returns
class AppointmentResponse(AppointmentBase):
    id: int
    created_at: datetime | None

    model_config = {"from_attributes": True}


# --- Response with Details --- nested full response
class AppointmentWithDetails(AppointmentResponse):
    from schemas.user import UserResponse
    from schemas.doctor import DoctorResponse
    from schemas.doctor_slot import DoctorSlotResponse

    user: UserResponse | None = None
    doctor: DoctorResponse | None = None
    slot: DoctorSlotResponse | None = None

    model_config = {"from_attributes": True}