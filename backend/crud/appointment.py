# crud/appointment.py

import json
import os
from sqlalchemy.orm import Session
from models.appointment import Appointment
from models.doctor_slot import DoctorSlot
from models.user import User
from schemas.appointment import AppointmentCreate, AppointmentStatus
from core.email import send_appointment_email


# ✅ Fix - agent.tools se import mat karo, yahan hi likho
def load_doctors() -> list[dict]:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "doctors.json")
    with open(json_path, "r") as f:
        return json.load(f)


def create_appointment(db: Session, appointment: AppointmentCreate) -> Appointment | None:
    slot = db.query(DoctorSlot).filter(DoctorSlot.id == appointment.slot_id).first()
    if not slot or slot.is_booked:
        return None

    db_appointment = Appointment(
        user_id=appointment.user_id,
        doctor_id=appointment.doctor_id,
        slot_id=appointment.slot_id,
        status=appointment.status,
    )
    db.add(db_appointment)
    slot.is_booked = True
    db.commit()
    db.refresh(db_appointment)

    # Send confirmation email
    try:
        user = db.query(User).filter(User.id == appointment.user_id).first()
        doctors = load_doctors()
        doctor = next((d for d in doctors if d["id"] == appointment.doctor_id), None)

        if user and user.email and doctor:
            send_appointment_email(
                to_email=user.email,
                patient_name=user.name or "Patient",
                doctor_name=doctor["name"],
                doctor_specialization=doctor["specialization"],
                slot_start=str(slot.start_time),
                slot_end=str(slot.end_time),
                appointment_id=db_appointment.id,
            )
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

    return db_appointment


def get_appointment(db: Session, appointment_id: int) -> Appointment | None:
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def get_user_appointments(db: Session, user_id: int) -> list[Appointment]:
    return db.query(Appointment).filter(Appointment.user_id == user_id).all()


def update_appointment_status(db: Session, appointment_id: int, status: AppointmentStatus) -> Appointment | None:
    db_appointment = get_appointment(db, appointment_id)
    if not db_appointment:
        return None
    db_appointment.status = status
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def cancel_appointment(db: Session, appointment_id: int) -> bool:
    db_appointment = get_appointment(db, appointment_id)
    if not db_appointment:
        return False

    slot = db.query(DoctorSlot).filter(DoctorSlot.id == db_appointment.slot_id).first()
    if slot:
        slot.is_booked = False

    db_appointment.status = AppointmentStatus.cancelled
    db.commit()
    return True