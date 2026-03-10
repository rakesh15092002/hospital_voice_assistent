# schemas/hospital.py

from pydantic import BaseModel
from datetime import time


# --- Base --- common fields
class HospitalBase(BaseModel):
    name: str
    address: str
    phone: str
    emergency_phone: str
    opening_time: time


# --- Create --- request body
class HospitalCreate(HospitalBase):
    pass


# --- Update --- optional fields
class HospitalUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    phone: str | None = None
    emergency_phone: str | None = None
    opening_time: time | None = None


# --- Response --- what API returns
class HospitalResponse(HospitalBase):
    id: int

    model_config = {"from_attributes": True}