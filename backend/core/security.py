# core/security.py

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.config import settings


# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Plain password ko hash karo"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Login pe password verify karo"""
    return pwd_context.verify(plain_password, hashed_password)


# --- JWT Token ---
def create_access_token(data: dict) -> str:
    """JWT token banao"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """JWT token decode karo, invalid hoga toh None return karo"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None