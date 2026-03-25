from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from redis import Redis

from app.db.session import SessionLocal
from app.core.config import settings
from app.core.security import decode_token
from app.models.user import User
from app.schemas.token import TokenPayload


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), request: Request = None
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = None
    # Try to get token from cookie first
    if request and "access_token" in request.cookies:
        token = request.cookies["access_token"]
    
    # If still no token, raise exception
    if not token:
        raise credentials_exception

    try:
        payload = decode_token(token)
        if payload is None:
            raise credentials_exception
        user_id = payload.sub
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

def get_redis_client() -> Redis:
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
