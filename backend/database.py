# database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get DATABASE_URL from .env, fallback to SQLite if not found
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hospital_chatbot.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite + FastAPI
    echo=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """FastAPI dependency — yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables. Call once on startup."""
    Base.metadata.create_all(bind=engine)