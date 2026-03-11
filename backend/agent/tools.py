import json
import os
from sqlalchemy.orm import Session
from crud.appointment import create_appointment, cancel_appointment, get_user_appointments
from crud.voice_log import create_voice_log
from schemas.appointment import AppointmentCreate, AppointmentStatus
from schemas.voice_log import VoiceLogCreate, SentimentType
from models.doctor_slot import DoctorSlot


# --- Load Hardcoded Doctors ---
def load_doctors() -> list[dict]:
    """Load doctors from JSON file"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, "data", "doctors.json")
    with open(json_path, "r") as f:
        return json.load(f)


# --- Tool 1: Find Doctor by Symptoms ---
def find_doctor(symptoms: str) -> dict:
    """
    Find a matching doctor based on patient symptoms
    The voice bot will call this first
    """
    doctors = load_doctors()
    symptoms_lower = symptoms.lower()

    matched = []
    for doctor in doctors:
        doctor_symptoms = doctor.get("symptoms", [])
        for s in doctor_symptoms:
            if s.lower() in symptoms_lower:
                matched.append(doctor)
                break

    if not matched:
        return {
            "found": False,
            "message": "No doctor found for these symptoms. Please visit our general physician."
        }

    return {
        "found": True,
        "doctors": matched
    }


# --- Tool 2: Get Available Slots ---
def get_available_slots(db: Session, doctor_id: int) -> dict:
    """
    Find available slots for the doctor
    Only return slots where is_booked=False
    """
    slots = db.query(DoctorSlot).filter(
        DoctorSlot.doctor_id == doctor_id,
        DoctorSlot.is_booked == False
    ).all()

    if not slots:
        return {
            "found": False,
            "message": "No available slots for this doctor."
        }

    return {
        "found": True,
        "slots": [
            {
                "slot_id": slot.id,
                "start_time": str(slot.start_time),
                "end_time": str(slot.end_time),
            }
            for slot in slots
        ]
    }


# --- Tool 3: Book Appointment ---
def book_appointment(db: Session, user_id: int, doctor_id: int, slot_id: int) -> dict:
    """
    Book an appointment
    If the slot is available, book it; otherwise return an error
    """
    appointment = create_appointment(db, AppointmentCreate(
        user_id=user_id,
        doctor_id=doctor_id,
        slot_id=slot_id,
        status=AppointmentStatus.confirmed,
    ))

    if not appointment:
        return {
            "success": False,
            "message": "Slot already booked. Please choose another slot."
        }

    return {
        "success": True,
        "appointment_id": appointment.id,
        "message": f"Appointment confirmed! Your appointment ID is {appointment.id}."
    }


# --- Tool 4: Cancel Appointment ---
def cancel_user_appointment(db: Session, appointment_id: int) -> dict:
    """Cancel an appointment"""
    result = cancel_appointment(db, appointment_id)
    if not result:
        return {
            "success": False,
            "message": "Appointment not found."
        }
    return {
        "success": True,
        "message": "Appointment cancelled successfully."
    }


# --- Tool 5: Save Voice Log ---
def save_voice_log(
    db: Session,
    session_id: int,
    transcript: str,
    ai_response: str,
    sentiment: str = "neutral",
    is_emergency: bool = False
) -> None:
    """Save each conversation turn"""
    create_voice_log(db, VoiceLogCreate(
        session_id=session_id,
        transcript=transcript,
        ai_response=ai_response,
        sentiment=SentimentType(sentiment),
        is_emergency=is_emergency,
    ))


# --- Tool 6: Get Hospital Info ---
def get_hospital_info() -> dict:
    """Return basic hospital information"""
    from core.config import settings
    return {
        "name": settings.HOSPITAL_NAME,
        "emergency_phone": settings.HOSPITAL_EMERGENCY_PHONE,
        "opening_time": settings.HOSPITAL_OPENING_TIME,
        "address": settings.HOSPITAL_ADDRESS,
    }