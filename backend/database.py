# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base
from core.config import settings


# ✅ Fix 1 - SQLite and PostgreSQL support
def get_engine():
    if settings.DATABASE_URL.startswith("sqlite"):
        return create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False},  
            echo=settings.DEBUG, 
        )
    else:
        return create_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,  
        )


engine = get_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """FastAPI dependency — yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables on startup."""
    Base.metadata.create_all(bind=engine)