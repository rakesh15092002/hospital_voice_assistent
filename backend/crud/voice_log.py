# crud/voice_log.py

from sqlalchemy.orm import Session
from models.voice_log import VoiceLog
from schemas.voice_log import VoiceLogCreate


# --- Create --- save one conversation turn
def create_voice_log(db: Session, log: VoiceLogCreate) -> VoiceLog:
    db_log = VoiceLog(
        session_id=log.session_id,
        transcript=log.transcript,
        ai_response=log.ai_response,
        sentiment=log.sentiment,
        is_emergency=log.is_emergency,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


# --- Get by ID ---
def get_voice_log(db: Session, log_id: int) -> VoiceLog | None:
    return db.query(VoiceLog).filter(VoiceLog.id == log_id).first()


# --- Get All by Session ---
def get_session_logs(db: Session, session_id: int) -> list[VoiceLog]:
    return db.query(VoiceLog).filter(VoiceLog.session_id == session_id).all()


# --- Get Emergency Logs ---
def get_emergency_logs(db: Session) -> list[VoiceLog]:
    return db.query(VoiceLog).filter(VoiceLog.is_emergency == True).all()