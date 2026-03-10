# schemas/department.py

from pydantic import BaseModel


# --- Base --- common fields
class DepartmentBase(BaseModel):
    name: str
    floor_num: str
    hospital_id: int


# --- Create --- request body
class DepartmentCreate(DepartmentBase):
    pass


# --- Update --- optional fields
class DepartmentUpdate(BaseModel):
    name: str | None = None
    floor_num: str | None = None
    hospital_id: int | None = None


# --- Response --- what API returns
class DepartmentResponse(DepartmentBase):
    id: int

    model_config = {"from_attributes": True}


# --- Response with Hospital --- nested response
class DepartmentWithHospital(DepartmentResponse):
    from schemas.hospital import HospitalResponse
    hospital: HospitalResponse | None = None

    model_config = {"from_attributes": True}