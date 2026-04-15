from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
import jwt
from typing import Optional
from passlib.context import CryptContext
from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        return False

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    else:
        expires = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": data.get("sub"), "exp": expires}
    token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        if "sub" not in payload:
            return None

        return payload
    except InvalidTokenError:
        return None

