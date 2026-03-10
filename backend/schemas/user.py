from pydantic import BaseModel, EmailStr
from datetime import datetime


# --- Base --- common fields
class UserBase(BaseModel):
    name: str
    email: EmailStr


# --- Create --- signup request body
class UserCreate(UserBase):
    password: str


# --- Update --- optional fields for profile update
class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


# --- Response --- what API returns (no password)
class UserResponse(UserBase):
    id: int
    created_at: datetime | None

    model_config = {"from_attributes": True}