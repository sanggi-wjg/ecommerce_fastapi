from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.core.config import get_settings
from app.database.database import get_db
from app.dependency.auth_depend import get_current_user
from app.schema.auth_schema import Token
from app.schema.user_schema import User
from app.service import user_service
from app.utils.authentication import verify_token, verify_password, encode_token

router = APIRouter(
    prefix="",
    tags=["Authentication"],
    responses={404: {"detail": "not found"}}
)

settings = get_settings()
templates = Jinja2Templates(directory=settings.template_root)


@router.get("/verification", response_class=HTMLResponse)
async def verify_email(request: Request, token: str, db: Session = Depends(get_db)):
    user_by_token = await verify_token(token)
    find_user = user_service.find_user_by_id(db, user_by_token['user_id'])

    if find_user and not find_user.is_verified:
        user = user_service.update_user_verified(db, find_user)
        return templates.TemplateResponse("verification.html", {
            'request': request,
            'user': user,
        })
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired",
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/token", response_model=Token)
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    find_user = user_service.find_authenticate_user_by_email(db, form_data.username)
    if not find_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not verify_password(form_data.password, find_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return Token(
        access_token=await encode_token({"sub": find_user.email}),
        token_type="bearer"
    )


@router.get("/users/me", response_model=User)
async def get_users_me(current_user: User = Depends(get_current_user)):
    return current_user
