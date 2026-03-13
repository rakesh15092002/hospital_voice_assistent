# api/routes/livekit.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from livekit.api import AccessToken, VideoGrants
from database import get_db
from crud.voice_session import create_voice_session, end_voice_session, get_session_by_livekit_sid
from schemas.voice_session import VoiceSessionCreate
from core.config import settings
from core.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/livekit", tags=["LiveKit"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return int(payload.get("sub"))


@router.post("/token")
def generate_livekit_token(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    try:
        room_name = f"hospital_room_{user_id}"

        # ✅ Fix 4 - keyword arguments use karo
        token = (
            AccessToken(
                api_key=settings.LIVEKIT_API_KEY,
                api_secret=settings.LIVEKIT_API_SECRET
            )
            .with_identity(str(user_id))
            .with_name(f"user_{user_id}")
            .with_grants(VideoGrants(room_join=True, room=room_name))
        )

        jwt_token = token.to_jwt()

        existing_session = get_session_by_livekit_sid(db, room_name)
        if existing_session:
            session = existing_session
        else:
            session = create_voice_session(db, VoiceSessionCreate(
                user_id=user_id,
                livekit_sid=room_name,
            ))

        return {
            "token": jwt_token,
            "room": room_name,
            "livekit_url": settings.LIVEKIT_URL,
            "session_id": session.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token generation failed: {str(e)}"
        )


@router.post("/webhook")
async def livekit_webhook(payload: dict):
    try:
        event = payload.get("event")
        room = payload.get("room", {})
        livekit_sid = room.get("name")

        if event == "room_finished" and livekit_sid:
            from database import SessionLocal
            db = SessionLocal()
            # ✅ Fix 5 - finally block add kiya
            try:
                end_voice_session(db, livekit_sid)
            finally:
                db.close()

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Webhook failed: {str(e)}"
        )