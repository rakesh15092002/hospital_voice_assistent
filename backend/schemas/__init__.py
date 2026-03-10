# schemas/__init__.py

from .user import UserBase, UserCreate, UserUpdate, UserResponse
from .hospital import HospitalBase, HospitalCreate, HospitalUpdate, HospitalResponse
from .department import DepartmentBase, DepartmentCreate, DepartmentUpdate, DepartmentResponse, DepartmentWithHospital
from .doctor import DoctorBase, DoctorCreate, DoctorUpdate, DoctorResponse, DoctorWithDepartment
from .doctor_slot import DoctorSlotBase, DoctorSlotCreate, DoctorSlotUpdate, DoctorSlotResponse, DoctorSlotAvailable
from .appointment import AppointmentStatus, AppointmentBase, AppointmentCreate, AppointmentUpdate, AppointmentResponse, AppointmentWithDetails
from .voice_session import VoiceSessionBase, VoiceSessionCreate, VoiceSessionUpdate, VoiceSessionResponse, VoiceSessionWithLogs
from .voice_log import SentimentType, VoiceLogBase, VoiceLogCreate, VoiceLogUpdate, VoiceLogResponse, VoiceLogEmergency

__all__ = [
    # User
    "UserBase", "UserCreate", "UserUpdate", "UserResponse",
    # Hospital
    "HospitalBase", "HospitalCreate", "HospitalUpdate", "HospitalResponse",
    # Department
    "DepartmentBase", "DepartmentCreate", "DepartmentUpdate", "DepartmentResponse", "DepartmentWithHospital",
    # Doctor
    "DoctorBase", "DoctorCreate", "DoctorUpdate", "DoctorResponse", "DoctorWithDepartment",
    # DoctorSlot
    "DoctorSlotBase", "DoctorSlotCreate", "DoctorSlotUpdate", "DoctorSlotResponse", "DoctorSlotAvailable",
    # Appointment
    "AppointmentStatus", "AppointmentBase", "AppointmentCreate", "AppointmentUpdate", "AppointmentResponse", "AppointmentWithDetails",
    # VoiceSession
    "VoiceSessionBase", "VoiceSessionCreate", "VoiceSessionUpdate", "VoiceSessionResponse", "VoiceSessionWithLogs",
    # VoiceLog
    "SentimentType", "VoiceLogBase", "VoiceLogCreate", "VoiceLogUpdate", "VoiceLogResponse", "VoiceLogEmergency",
]