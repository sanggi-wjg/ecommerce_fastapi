from typing import List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import BaseModel, EmailStr

from app.core.config import get_settings
from app.database.models import UserEntity
from app.utils.authentication import encode_token

settings = get_settings()


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME="Test",
    MAIL_FROM=settings.mail_from,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


# def get_email():
#     email = FastMail(conf)
#     yield email

async def create_verify_template(token: str):
    return f"""
        <!DOCTYPE html>
        <html lang="ko-kr">
            <head>
            </head>
            <body>
                <div style="display:flex; align-items:center; justify-content=center;">
                    <h3>Account Verification</h3>
                    <p>Click on the button below to verify your account</p>
                    <a href="http://localhost:9002/verfication?token={token}">Verify your email</a>
                </div>
            </body>
        </html>
    """


async def send_verify_mail(email: EmailSchema, user: UserEntity):
    token = await encode_token({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })

    message = MessageSchema(
        recipients=email.dict().get("email"),
        subject="Verification Email",
        body=await create_verify_template(token),
        subtype="html"
    )
    mail = FastMail(conf)
    await mail.send_message(message)
