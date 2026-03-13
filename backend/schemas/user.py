from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime | None
    model_config = {"from_attributes": True}


# Login request - only email and password needed
class UserLogin(BaseModel):
    email: EmailStr
    password: str