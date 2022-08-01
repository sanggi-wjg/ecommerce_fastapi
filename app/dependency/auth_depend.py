from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.database import get_db
from app.database.models import UserEntity
from app.exception.exceptions import BadCredential
from app.schema.auth_schema import TokenData
from app.schema.user_schema import User
from app.service import user_service

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def verify_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserEntity:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.access_token_algorithm])
        username = payload.get('sub')
        if username is None:
            raise BadCredential("Invalid email")

        token_data = TokenData(user_email=username)
    except JWTError:
        raise BadCredential()

    find_user = user_service.find_authenticate_user_by_email(db, token_data.user_email)
    if not find_user:
        raise BadCredential()
    return find_user


async def get_current_user(user: UserEntity = Depends(verify_current_user)) -> User:
    if not user.is_verified:
        raise BadCredential("Invalid token")

    return User(
        email=user.email,
        username=user.username,
        is_verified=user.is_verified,
    )
