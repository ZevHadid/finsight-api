from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
import hashlib

from app.core.config import settings
from app.schemas.token import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")
    hashed = hashlib.sha256(password_bytes).hexdigest()
    return pwd_context.verify(hashed, hashed_password)

def get_password_hash(password: str) -> str:
    password_bytes = password.encode("utf-8")
    hashed = hashlib.sha256(password_bytes).hexdigest()
    return pwd_context.hash(hashed)

def create_access_token(subject: int, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access"
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: int, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.now(datetime.timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh"
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[TokenPayload]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return TokenPayload(**payload)
    except JWTError as e:
        print(f"JWT decode error: {e}")
        return None
