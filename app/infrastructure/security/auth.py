from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
	return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
	return pwd_context.verify(password, hashed)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
	if expires_delta is None:
		expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	expire = datetime.now(timezone.utc) + expires_delta
	to_encode = {"sub": subject, "exp": expire}
	return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str | None:
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
		return payload.get("sub")
	except JWTError:
		return None
