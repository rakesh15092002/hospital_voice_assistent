# core/config.py

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "Hospital Voice Assistant"
    DEBUG: bool = False

    # --- Database ---
    DATABASE_URL: str = "sqlite:///./hospital_chatbot.db"

    # --- JWT ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- LiveKit ---
    LIVEKIT_API_KEY: str
    LIVEKIT_API_SECRET: str
    LIVEKIT_URL: str

    # --- OpenAI ---
    OPENAI_API_KEY: str

    # --- Email ---
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USER: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None

    # =============================
    # Hospital Information
    # =============================
    HOSPITAL_NAME: str = "City Care Hospital"
    HOSPITAL_TAGLINE: str = "Your Health, Our Priority"
    HOSPITAL_ADDRESS: str = "Plot No. 45, Sector 12, Noida, Uttar Pradesh - 201301"
    HOSPITAL_PHONE: str = "+91-120-4567890"
    HOSPITAL_EMERGENCY_PHONE: str = "108"
    HOSPITAL_DIRECT_EMERGENCY: str = "+91-120-4567999"
    HOSPITAL_EMAIL: str = "info@citycarehospital.com"
    HOSPITAL_WEBSITE: str = "www.citycarehospital.com"
    HOSPITAL_OPENING_TIME: str = "8:00 AM"
    HOSPITAL_CLOSING_TIME: str = "8:00 PM"
    HOSPITAL_EMERGENCY_HOURS: str = "24/7"
    HOSPITAL_ESTABLISHED: str = "2005"

    # =============================
    # Hospital Layout
    # =============================
    HOSPITAL_FLOORS: str = (
        "Ground Floor : Main Reception, Emergency Ward, "
        "General Medicine OPD (Room 05, 06), Pharmacy, Lab, X-Ray, Ambulance Bay | "
        "1st Floor    : ENT OPD (Room 105, 106), Dermatology (Room 110), "
        "Ophthalmology (Room 115), Pediatrics (Room 120, 121), Cafeteria | "
        "2nd Floor    : Cardiology (Room 201, 202), Orthopedics (Room 210, 211), "
        "Gastroenterology (Room 215, 216), ICU Wing | "
        "3rd Floor    : Neurology (Room 301, 302), Gynecology (Room 310), "
        "Operation Theatre, Blood Bank"
    )

    # =============================
    # Departments
    # =============================
    HOSPITAL_DEPARTMENTS: str = (
        "1. Cardiology - 2nd Floor | "
        "2. Neurology - 3rd Floor | "
        "3. Orthopedics - 2nd Floor | "
        "4. ENT - 1st Floor | "
        "5. Dermatology - 1st Floor | "
        "6. Ophthalmology - 1st Floor | "
        "7. Gynecology - 3rd Floor | "
        "8. Pediatrics - 1st Floor | "
        "9. Gastroenterology - 2nd Floor | "
        "10. General Medicine - Ground Floor | "
        "11. ICU - 2nd Floor | "
        "12. Emergency - Ground Floor (24/7)"
    )

    # =============================
    # Important Locations
    # =============================
    HOSPITAL_LOCATIONS: str = (
        "Pharmacy: Ground Floor near main exit | "
        "Laboratory: Ground Floor left wing | "
        "X-Ray/Radiology: Ground Floor left wing next to Lab | "
        "Blood Bank: 3rd Floor | "
        "Operation Theatre: 3rd Floor | "
        "ICU: 2nd Floor restricted area | "
        "Emergency Ward: Ground Floor right side entrance | "
        "Ambulance Bay: Ground Floor right side exit | "
        "Cafeteria: 1st Floor left wing | "
        "Parking: Basement and open area outside | "
        "ATM: Ground Floor near reception | "
        "Wheelchair: Available at Reception Ground Floor | "
        "Lift/Elevator: Near Reception Ground Floor | "
        "Washrooms: Every floor near elevator"
    )

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()