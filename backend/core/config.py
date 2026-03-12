# core/config.py

from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "Hospital Voice Assistant"
    DEBUG: bool = False  # ✅ Fix 3 - default False, .env se override karo

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
    EMAIL_USER: Optional[str] = None      # ✅ Fix 1 - None so we can check
    EMAIL_PASSWORD: Optional[str] = None  # ✅ Fix 1 - None so we can check

    # --- Hospital ---
    HOSPITAL_NAME: str = "City Hospital"
    HOSPITAL_EMERGENCY_PHONE: str = "108"
    HOSPITAL_OPENING_TIME: str = "08:00:00"
    HOSPITAL_ADDRESS: str = "123 Main Street"

    # ✅ Fix 2 - Pydantic v2 style
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()