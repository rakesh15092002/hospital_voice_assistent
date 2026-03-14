from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.voice_session import VoiceSession
from models.voice_log import VoiceLog
from core.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/voice", tags=["Voice"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload.get("sub"))

# Get all voice sessions for current user
@router.get("/sessions")
def get_my_sessions(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    sessions = db.query(VoiceSession).filter(
        VoiceSession.user_id == user_id
    ).order_by(VoiceSession.started_at.desc()).all()

    return [
        {
            "id": s.id,
            "livekit_sid": s.livekit_sid,
            "started_at": s.started_at,
            "ended_at": s.ended_at,
        }
        for s in sessions
    ]

# Get all logs for a specific session
@router.get("/sessions/{session_id}/logs")
def get_session_logs(
    session_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    # Verify session belongs to user
    session = db.query(VoiceSession).filter(
        VoiceSession.id == session_id,
        VoiceSession.user_id == user_id,
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    logs = db.query(VoiceLog).filter(
        VoiceLog.session_id == session_id
    ).order_by(VoiceLog.created_at.asc()).all()

    return [
        {
            "id": l.id,
            "transcript": l.transcript,
            "ai_response": l.ai_response,
            "sentiment": l.sentiment,
            "is_emergency": l.is_emergency,
            "created_at": l.created_at,
        }
        for l in logs
    ]