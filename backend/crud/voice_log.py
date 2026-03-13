# crud/voice_log.py

from sqlalchemy.orm import Session
from models.voice_log import VoiceLog
from schemas.voice_log import VoiceLogCreate


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


def get_voice_log(db: Session, log_id: int) -> VoiceLog | None:
    return db.query(VoiceLog).filter(VoiceLog.id == log_id).first()


def get_session_logs(db: Session, session_id: int) -> list[VoiceLog]:
    return db.query(VoiceLog).filter(VoiceLog.session_id == session_id).all()


def get_emergency_logs(db: Session) -> list[VoiceLog]:
    # ✅ Fix 3 - is_(True) use karo
    return db.query(VoiceLog).filter(VoiceLog.is_emergency.is_(True)).all()