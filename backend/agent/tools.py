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
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        return {"found": False, "message": "Appointment not found."}
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
    old_appointment = get_appointment(db, appointment_id)
    if not old_appointment:
        return {"success": False, "message": "Appointment not found."}
    new_slot = db.query(DoctorSlot).filter(
        DoctorSlot.id == new_slot_id,
        DoctorSlot.is_booked == False
    ).first()
    if not new_slot:
        return {"success": False, "message": "New slot is not available."}
    old_slot = db.query(DoctorSlot).filter(DoctorSlot.id == old_appointment.slot_id).first()
    if old_slot:
        old_slot.is_booked = False
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
    from core.config import settings
    emergency_keywords = [
        "chest pain", "heart attack", "can't breathe", "unconscious",
        "severe bleeding", "stroke", "accident", "ambulance", "dying",
        "not breathing", "collapsed", "overdose", "poisoning", "burns"
    ]
    situation_lower = situation.lower()
    is_emergency = any(keyword in situation_lower for keyword in emergency_keywords)

    if is_emergency:
        return {
            "is_emergency": True,
            "message": (
                f"EMERGENCY DETECTED! Please call {settings.HOSPITAL_DIRECT_EMERGENCY} immediately "
                f"or go to Emergency Ward on Ground Floor, right side entrance. Do not wait! "
                f"National Emergency: {settings.HOSPITAL_EMERGENCY_PHONE}"
            ),
            "emergency_phone": settings.HOSPITAL_DIRECT_EMERGENCY,
            "national_emergency": settings.HOSPITAL_EMERGENCY_PHONE,
            "emergency_location": "Ground Floor - Emergency Ward, Right Side Entrance",
            "ambulance_bay": "Ground Floor, Right Side Exit",
        }
    return {"is_emergency": False, "message": "No emergency detected."}


# --- Tool 8: Get Internal Location ---
def get_internal_location(place: str) -> dict:
    from core.config import settings
    locations = {
        "pharmacy":          "Ground Floor, near main exit",
        "lab":               "Ground Floor, left wing",
        "laboratory":        "Ground Floor, left wing",
        "x-ray":             "Ground Floor, left wing, next to Lab",
        "radiology":         "Ground Floor, left wing, next to Lab",
        "blood bank":        "3rd Floor",
        "operation theatre": "3rd Floor",
        "ot":                "3rd Floor",
        "icu":               "2nd Floor, restricted area",
        "emergency":         "Ground Floor, right side entrance",
        "ambulance":         "Ground Floor, right side exit",
        "cafeteria":         "1st Floor, left wing",
        "canteen":           "1st Floor, left wing",
        "parking":           "Basement and open area outside",
        "atm":               "Ground Floor, near reception",
        "wheelchair":        "Available at Reception, Ground Floor",
        "lift":              "Near Reception, Ground Floor",
        "elevator":          "Near Reception, Ground Floor",
        "washroom":          "Every floor, near elevator",
        "toilet":            "Every floor, near elevator",
        "reception":         "Ground Floor, main entrance",
        "cardiology":        "2nd Floor, Room 201-202",
        "neurology":         "3rd Floor, Room 301-302",
        "orthopedic":        "2nd Floor, Room 210-211",
        "ent":               "1st Floor, Room 105-106",
        "dermatology":       "1st Floor, Room 110",
        "eye":               "1st Floor, Room 115",
        "ophthalmology":     "1st Floor, Room 115",
        "gynecology":        "3rd Floor, Room 310",
        "gynae":             "3rd Floor, Room 310",
        "pediatric":         "1st Floor, Room 120-121",
        "children":          "1st Floor, Room 120-121",
        "gastro":            "2nd Floor, Room 215-216",
        "general medicine":  "Ground Floor, Room 05-06",
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
        "message": f"Location not found. Please ask at the Reception on Ground Floor or call {settings.HOSPITAL_PHONE}."
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
        "tagline": settings.HOSPITAL_TAGLINE,
        "address": settings.HOSPITAL_ADDRESS,
        "phone": settings.HOSPITAL_PHONE,
        "emergency_phone": settings.HOSPITAL_EMERGENCY_PHONE,
        "direct_emergency": settings.HOSPITAL_DIRECT_EMERGENCY,
        "email": settings.HOSPITAL_EMAIL,
        "opening_time": settings.HOSPITAL_OPENING_TIME,
        "closing_time": settings.HOSPITAL_CLOSING_TIME,
        "emergency_hours": settings.HOSPITAL_EMERGENCY_HOURS,
        "departments": settings.HOSPITAL_DEPARTMENTS,
        "floors": settings.HOSPITAL_FLOORS,
    }