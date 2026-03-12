# core/config.py

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "Hospital Voice Assistant"
    DEBUG: bool = True

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
    EMAIL_USER: str = ""
    EMAIL_PASSWORD: str = ""

    # --- Hospital (hardcoded) ---
    HOSPITAL_NAME: str = "City Hospital"
    HOSPITAL_EMERGENCY_PHONE: str = "108"
    HOSPITAL_OPENING_TIME: str = "08:00:00"
    HOSPITAL_ADDRESS: str = "123 Main Street"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()