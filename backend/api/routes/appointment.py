# api/routes/appointment.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from crud.appointment import (
    create_appointment,
    get_appointment,
    get_user_appointments,
    cancel_appointment,
    update_appointment_status,
)
from schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentStatus,
)
from core.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/appointments", tags=["Appointments"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# --- Get Current User from Token ---
def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return int(payload.get("sub"))


# --- Book Appointment ---
@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def book_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    appointment.user_id = user_id
    result = create_appointment(db, appointment)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot already booked or not found"
        )
    return result


# --- Get My Appointments ---
@router.get("/me", response_model=list[AppointmentResponse])
def my_appointments(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return get_user_appointments(db, user_id)


# --- Get Appointment by ID ---
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment_by_id(
    appointment_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    appointment = get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    return appointment


# --- Cancel Appointment ---
@router.patch("/{appointment_id}/cancel", status_code=status.HTTP_200_OK)
def cancel_appointment_route(
    appointment_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    result = cancel_appointment(db, appointment_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    return {"message": "Appointment cancelled successfully"}