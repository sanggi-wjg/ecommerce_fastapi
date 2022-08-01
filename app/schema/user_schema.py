from pydantic import BaseModel, PositiveInt, EmailStr, validator

from app.utils.authentication import hash_password


class UserBase(BaseModel):
    id: PositiveInt


class User(BaseModel):
    email: EmailStr
    username: str
    is_verified: bool


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password1: str
    password2: str

    @validator("password2")
    def password_match(cls, v, values):
        if v != values.get('password1'):
            raise ValueError("passwords does not match")
        return v

    @property
    def hashed_password(self):
        return hash_password(self.password1)
