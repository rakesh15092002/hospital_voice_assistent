# schemas/doctor_slot.py

from pydantic import BaseModel
from datetime import datetime


# --- Base --- common fields
class DoctorSlotBase(BaseModel):
    doctor_id: int
    start_time: datetime
    end_time: datetime
    is_booked: bool = False


# --- Create --- request body
class DoctorSlotCreate(DoctorSlotBase):
    pass


# --- Update --- optional fields
class DoctorSlotUpdate(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None
    is_booked: bool | None = None


# --- Response --- what API returns
class DoctorSlotResponse(DoctorSlotBase):
    id: int

    model_config = {"from_attributes": True}


# --- Available Slots --- only unbooked slots
class DoctorSlotAvailable(DoctorSlotResponse):
    is_booked: bool = False

    model_config = {"from_attributes": True}