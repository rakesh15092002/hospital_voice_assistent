import json
import os
from sqlalchemy.orm import Session
from crud.appointment import create_appointment, cancel_appointment, get_user_appointments, get_appointment
from crud.voice_log import create_voice_log
from schemas.appointment import AppointmentCreate, AppointmentStatus
from schemas.voice_log import VoiceLogCreate, SentimentType
from models.doctor_slot import DoctorSlot


# --- Load Hardcoded Doctors ---
def load_doctors() -> list[dict]:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, "data", "doctors.json")
    with open(json_path, "r") as f:
        return json.load(f)


# --- Tool 1: Find Doctor by Symptoms ---
def find_doctor(symptoms: str) -> dict:
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
    return {"found": True, "doctors": matched}


# --- Tool 2: Get Available Slots ---
def get_available_slots(db: Session, doctor_id: int) -> dict:
    slots = db.query(DoctorSlot).filter(
        DoctorSlot.doctor_id == doctor_id,
        DoctorSlot.is_booked == False
    ).all()
    if not slots:
        return {"found": False, "message": "No available slots for this doctor."}
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
    appointment = create_appointment(db, AppointmentCreate(
        user_id=user_id,
        doctor_id=doctor_id,
        slot_id=slot_id,
        status=AppointmentStatus.confirmed,
    ))
    if not appointment:
        return {"success": False, "message": "Slot already booked. Please choose another slot."}
    return {
        "success": True,
        "appointment_id": appointment.id,
        "message": f"Appointment confirmed! Your appointment ID is {appointment.id}."
    }


# --- Tool 4: Cancel Appointment ---
def cancel_user_appointment(db: Session, appointment_id: int) -> dict:
    result = cancel_appointment(db, appointment_id)
    if not result:
        return {"success": False, "message": "Appointment not found."}
    return {"success": True, "message": "Appointment cancelled successfully."}


# --- Tool 5: Check Appointment Status ---
def check_appointment_status(db: Session, appointment_id: int) -> dict:
    """Check the status of an existing appointment"""
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        return {"found": False, "message": "Appointment not found."}

    # get slot info
    slot = db.query(DoctorSlot).filter(DoctorSlot.id == appointment.slot_id).first()

    return {
        "found": True,
        "appointment_id": appointment.id,
        "doctor_id": appointment.doctor_id,
        "status": appointment.status,
        "slot_time": str(slot.start_time) if slot else "Unknown",
        "created_at": str(appointment.created_at),
    }


# --- Tool 6: Reschedule Appointment ---
def reschedule_appointment(db: Session, appointment_id: int, new_slot_id: int) -> dict:
    """Cancel old slot and book new slot"""
    old_appointment = get_appointment(db, appointment_id)
    if not old_appointment:
        return {"success": False, "message": "Appointment not found."}

    # check new slot available hai
    new_slot = db.query(DoctorSlot).filter(
        DoctorSlot.id == new_slot_id,
        DoctorSlot.is_booked == False
    ).first()
    if not new_slot:
        return {"success": False, "message": "New slot is not available."}

    # free old slot
    old_slot = db.query(DoctorSlot).filter(DoctorSlot.id == old_appointment.slot_id).first()
    if old_slot:
        old_slot.is_booked = False

    # book new slot
    old_appointment.slot_id = new_slot_id
    old_appointment.status = AppointmentStatus.confirmed
    new_slot.is_booked = True

    db.commit()
    return {
        "success": True,
        "message": f"Appointment rescheduled to {new_slot.start_time} successfully."
    }


# --- Tool 7: Emergency Triage ---
def emergency_triage(situation: str) -> dict:
    """
    Stop all flows and handle emergency immediately
    Triggered by keywords like chest pain, accident, unconscious
    """
    from core.config import settings
    emergency_keywords = [
        "chest pain", "heart attack", "can't breathe", "unconscious",
        "severe bleeding", "stroke", "accident", "ambulance", "dying"
    ]
    situation_lower = situation.lower()
    is_emergency = any(keyword in situation_lower for keyword in emergency_keywords)

    if is_emergency:
        return {
            "is_emergency": True,
            "message": f"EMERGENCY DETECTED! Please call {settings.HOSPITAL_EMERGENCY_PHONE} immediately or go to Emergency Ward on Ground Floor. Do not wait!",
            "emergency_phone": settings.HOSPITAL_EMERGENCY_PHONE,
            "emergency_location": "Ground Floor - Emergency Ward",
        }
    return {"is_emergency": False, "message": "No emergency detected."}


# --- Tool 8: Get Internal Location ---
def get_internal_location(place: str) -> dict:
    """Find internal hospital locations like pharmacy, ward, etc."""
    locations = {
        "pharmacy": "Ground Floor, near main entrance",
        "emergency": "Ground Floor, right wing",
        "cardiology": "3rd Floor",
        "orthopedics": "2nd Floor",
        "ent": "2nd Floor",
        "neurology": "4th Floor",
        "general medicine": "1st Floor",
        "reception": "Ground Floor, main entrance",
        "cafeteria": "1st Floor, left wing",
        "parking": "Basement",
        "lift": "Near reception, Ground Floor",
    }

    place_lower = place.lower()
    for key, location in locations.items():
        if key in place_lower:
            return {
                "found": True,
                "place": key,
                "location": location,
                "message": f"{key.title()} is located at {location}."
            }

    return {
        "found": False,
        "message": "Location not found. Please ask at the reception on Ground Floor."
    }


# --- Tool 9: Save Voice Log ---
def save_voice_log(
    db: Session,
    session_id: int,
    transcript: str,
    ai_response: str,
    sentiment: str = "neutral",
    is_emergency: bool = False
) -> None:
    create_voice_log(db, VoiceLogCreate(
        session_id=session_id,
        transcript=transcript,
        ai_response=ai_response,
        sentiment=SentimentType(sentiment),
        is_emergency=is_emergency,
    ))


# --- Tool 10: Get Hospital Info ---
def get_hospital_info() -> dict:
    from core.config import settings
    return {
        "name": settings.HOSPITAL_NAME,
        "emergency_phone": settings.HOSPITAL_EMERGENCY_PHONE,
        "opening_time": settings.HOSPITAL_OPENING_TIME,
        "address": settings.HOSPITAL_ADDRESS,
    }