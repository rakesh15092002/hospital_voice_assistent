# crud/voice_session.py

from datetime import datetime, timezone  # ✅ Fix 4 - timezone import
from sqlalchemy.orm import Session
from models.voice_session import VoiceSession
from schemas.voice_session import VoiceSessionCreate, VoiceSessionUpdate


def create_voice_session(db: Session, session: VoiceSessionCreate) -> VoiceSession:
    db_session = VoiceSession(
        user_id=session.user_id,
        livekit_sid=session.livekit_sid,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_voice_session(db: Session, session_id: int) -> VoiceSession | None:
    return db.query(VoiceSession).filter(VoiceSession.id == session_id).first()


def get_session_by_livekit_sid(db: Session, livekit_sid: str) -> VoiceSession | None:
    return db.query(VoiceSession).filter(VoiceSession.livekit_sid == livekit_sid).first()


def get_user_voice_sessions(db: Session, user_id: int) -> list[VoiceSession]:
    return db.query(VoiceSession).filter(VoiceSession.user_id == user_id).all()


def end_voice_session(db: Session, livekit_sid: str) -> VoiceSession | None:
    db_session = get_session_by_livekit_sid(db, livekit_sid)
    if not db_session:
        return None
    # ✅ Fix 4 - timezone aware datetime
    db_session.ended_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_session)
    return db_session