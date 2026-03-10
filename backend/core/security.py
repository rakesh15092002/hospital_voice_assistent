import logging
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.config import settings

# 🚨 IMPORTANT: Passlib ke internal bcrypt version check ko silent karne ke liye
# Iske bina newer bcrypt versions par "ValueError: 72 bytes" error aata hai.
logging.getLogger("passlib").setLevel(logging.ERROR)

# Password hashing context setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Plain password ko secure hash mein convert karein"""
    # Note: Bcrypt 72 characters ki limit rakhta hai, passlib isse internally manage kar leta hai
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Login ke waqt password check karein"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """User ke liye JWT (Json Web Token) generate karein"""
    to_encode = data.copy()
    # Token expiration time set karein
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Token sign karein secret key aur algorithm ke saath
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict | None:
    """Encoded JWT token ko verify aur decode karein"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None