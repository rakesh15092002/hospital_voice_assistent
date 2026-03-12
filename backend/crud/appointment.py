# crud/appointment.py

from sqlalchemy.orm import Session
from models.appointment import Appointment
from models.doctor_slot import DoctorSlot
from schemas.appointment import AppointmentCreate, AppointmentStatus


# --- Create --- book appointment
def create_appointment(db: Session, appointment: AppointmentCreate) -> Appointment | None:
    # first check slot available hai ya nahi
    slot = db.query(DoctorSlot).filter(DoctorSlot.id == appointment.slot_id).first()
    if not slot or slot.is_booked:
        return None  # slot already booked hai

    # appointment banao — status schema se aayega, hardcoded nahi
    db_appointment = Appointment(
        user_id=appointment.user_id,
        doctor_id=appointment.doctor_id,
        slot_id=appointment.slot_id,
        status=appointment.status,  # fix: pehle hardcoded AppointmentStatus.pending tha
    )
    db.add(db_appointment)

    # slot ko booked mark karo
    slot.is_booked = True

    db.commit()
    db.refresh(db_appointment)
    return db_appointment


# --- Get by ID ---
def get_appointment(db: Session, appointment_id: int) -> Appointment | None:
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


# --- Get All by User ---
def get_user_appointments(db: Session, user_id: int) -> list[Appointment]:
    return db.query(Appointment).filter(Appointment.user_id == user_id).all()


# --- Update Status ---
def update_appointment_status(db: Session, appointment_id: int, status: AppointmentStatus) -> Appointment | None:
    db_appointment = get_appointment(db, appointment_id)
    if not db_appointment:
        return None
    db_appointment.status = status
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


# --- Cancel --- appointment cancel karo aur slot free karo
def cancel_appointment(db: Session, appointment_id: int) -> bool:
    db_appointment = get_appointment(db, appointment_id)
    if not db_appointment:
        return False

    # slot wapas free karo
    slot = db.query(DoctorSlot).filter(DoctorSlot.id == db_appointment.slot_id).first()
    if slot:
        slot.is_booked = False

    db_appointment.status = AppointmentStatus.cancelled
    db.commit()
    return True