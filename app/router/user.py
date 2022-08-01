import os.path
import secrets
from typing import List

from PIL import Image
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from app.core.config import get_settings
from app.database.database import get_db
from app.dependency.auth_depend import get_current_user
from app.dependency.query_depend import PageQueryParameter, page_parameter
from app.schema.user_address_schema import UserAddress, AddressCreate
from app.schema.user_schema import User, UserCreate, UserDetail
from app.service import user_service
from app.utils.email import EmailSchema, send_verify_mail

router = APIRouter(
    prefix="/api/v1",
    tags=["User"],
    responses={404: {"detail": "not found"}}
)

settings = get_settings()
templates = Jinja2Templates(directory=settings.template_root)


@router.get("/users", response_model=List[UserDetail], status_code=status.HTTP_200_OK)
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


@router.get("/users/{user_id}/address", response_model=List[UserAddress])
async def get_user_address(user_id: int, db: Session = Depends(get_db)):
    return user_service.find_user_address_by_user_id(db, user_id)


@router.post("/users/{user_id}/address")
async def create_user_address(user_id: int, address: AddressCreate, db: Session = Depends(get_db)):
    return user_service.create_user_address(db, user_id, address)


@router.post("/users/profile/file", response_class=JSONResponse)
async def upload_profile_file(file: UploadFile = File(...),
                              current_user: User = Depends(get_current_user),
                              db: Session = Depends(get_db)):
    filename = file.filename
    extension = filename.split(".")[1]

    if extension.lower() not in ("jpg", "png"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {
            "message": "error",
            "detail": "not allowed file extension"
        })

    filepath = os.path.join(settings.user_profile_root, f"{secrets.token_hex(10)}.{extension}")
    file_content = await file.read()

    with open(filepath, "wb") as f:
        f.write(file_content)

    img = Image.open(filepath)
    img = img.resize(size=(200, 200))
    img.save(filepath)

    find_user = user_service.update_user_profile_path(db, current_user.id, filepath)
    if find_user.profile_image == filepath:
        return JSONResponse({"message": "success"})
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {
            "message": "error",
            "detail": "fail to apply profile image"
        })
