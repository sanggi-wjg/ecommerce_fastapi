from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from app.core.config import get_settings
from app.database.database import get_db
from app.dependency.query_depend import PageQueryParameter, page_parameter
from app.schema.user_schema import User, UserCreate
from app.service import user_service
from app.utils.email import EmailSchema, send_verify_mail

router = APIRouter(
    prefix="/api/v1",
    tags=["User"],
    responses={404: {"detail": "not found"}}
)

settings = get_settings()
templates = Jinja2Templates(directory=settings.template_root)


@router.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_users(page_param: PageQueryParameter = Depends(page_parameter), db: Session = Depends(get_db)):
    return user_service.find_user_all_by_page(db, page_param.offset, page_param.limit)


@router.post("/users", response_class=JSONResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_user(user_create: UserCreate, background_task: BackgroundTasks, db: Session = Depends(get_db)):
    new_user = user_service.create_new_user(db, user_create)
    background_task.add_task(send_verify_mail, EmailSchema(email=[new_user.email]), new_user)
    return {
        "message": "ok",
        "detail": f"Hello {new_user.email}. Please check your email and click the link to verify your registration."
    }
