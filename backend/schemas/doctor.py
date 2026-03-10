from pydantic import BaseModel


# --- Base --- common fields
class DoctorBase(BaseModel):
    name: str
    specialization: str
    consultation_fee: int
    symptoms_handled: str
    department_id: int


# --- Create --- request body
class DoctorCreate(DoctorBase):
    pass


# --- Update --- optional fields
class DoctorUpdate(BaseModel):
    name: str | None = None
    specialization: str | None = None
    consultation_fee: int | None = None
    symptoms_handled: str | None = None
    department_id: int | None = None


# --- Response --- what API returns
class DoctorResponse(DoctorBase):
    id: int

    model_config = {"from_attributes": True}


# --- Response with Department --- nested response
class DoctorWithDepartment(DoctorResponse):
    from schemas.department import DepartmentResponse
    department: DepartmentResponse | None = None

    model_config = {"from_attributes": True}