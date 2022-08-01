from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import get_settings
from app.exception.exceptions import BadCredential

settings = get_settings()
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    return crypt.hash(plain_password)


async def encode_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({
        'exp': datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    })
    return jwt.encode(
        to_encode,
        settings.secret_key,
        settings.access_token_algorithm
    )


async def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, settings.access_token_algorithm)
        user_id = payload.get("id")
        username = payload.get("username")
        email = payload.get("email")
    except JWTError:
        raise BadCredential("Invalid token")

    return {
        "user_id": user_id,
        "username": username,
        "email": email
    }
