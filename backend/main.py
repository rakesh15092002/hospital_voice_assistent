# main.py

from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables, SessionLocal
from api.routes import auth, appointment, livekit
from core.config import settings
from models.doctor import Doctor
from models.doctor_slot import DoctorSlot
from agent.tools import load_doctors


def seed_doctors():
    """Load doctors from JSON into database"""
    doctors_data = load_doctors()
    db = SessionLocal()
    try:
        for d in doctors_data:
            # Skip if already exists
            existing = db.query(Doctor).filter(Doctor.id == d["id"]).first()
            if not existing:
                doctor = Doctor(
                    id=d["id"],
                    name=d["name"],
                    specialization=d["specialization"],
                    department=d.get("department"),
                    department_id=d.get("department_id"),
                    floor=d.get("floor"),
                    fee=d.get("fee"),
                )
                db.add(doctor)
        db.commit()
        print("✅ Doctors seeded")
    except Exception as e:
        print(f"❌ Doctor seed error: {e}")
        db.rollback()
    finally:
        db.close()


def seed_slots():
    """Create time slots for all doctors for next 7 days"""
    db = SessionLocal()
    try:
        # Skip if slots already exist
        existing = db.query(DoctorSlot).first()
        if existing:
            print("✅ Slots already exist")
            return

        doctors = db.query(Doctor).all()

        # Morning and evening time slots
        slot_times = [
            (9, 0),   # 9:00 AM
            (10, 0),  # 10:00 AM
            (11, 0),  # 11:00 AM
            (14, 0),  # 2:00 PM
            (15, 0),  # 3:00 PM
            (16, 0),  # 4:00 PM
        ]

        for doctor in doctors:
            for day in range(1, 8):  # Next 7 days
                date = datetime.now().replace(
                    hour=0, minute=0,
                    second=0, microsecond=0
                ) + timedelta(days=day)

                for hour, minute in slot_times:
                    start = date.replace(hour=hour, minute=minute)
                    end = start + timedelta(minutes=30)

                    slot = DoctorSlot(
                        doctor_id=doctor.id,
                        start_time=start,
                        end_time=end,
                        is_booked=False,
                    )
                    db.add(slot)

        db.commit()
        print("✅ Slots seeded — 420 slots created")

    except Exception as e:
        print(f"❌ Slot seed error: {e}")
        db.rollback()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    create_tables()
    print("✅ Tables created")
    seed_doctors()  # Step 1 - doctors pehle
    seed_slots()    # Step 2 - phir slots
    print("✅ App ready!")
    yield
    # On shutdown


# --- Create App ---
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ---
app.include_router(auth.router)
app.include_router(appointment.router)
app.include_router(livekit.router)


# --- Health Check ---
@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} is running!"}


# --- Run ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)