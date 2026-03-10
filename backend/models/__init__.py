# models/__init__.py

from .base import Base
from .user import User
from .hospital import Hospital          # Hospital table
from .department import Department      # Department table
from .doctor import Doctor              # Doctor table
from .doctor_slot import DoctorSlot     # Doctor available slots
from .appointment import Appointment    # Appointment booking
from .voice_session import VoiceSession # LiveKit voice session
from .voice_log import VoiceLog         # Transcript & AI response logs

__all__ = [
    "Base",
    "User",
    "Hospital",
    "Department",
    "Doctor",
    "DoctorSlot",
    "Appointment",
    "VoiceSession",
    "VoiceLog",
]