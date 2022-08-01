from datetime import datetime
from typing import List

from pydantic import BaseModel, PositiveInt, EmailStr, validator

from app.schema.user_address_schema import UserAddress
from app.utils.authentication import hash_password


class UserBase(BaseModel):
    id: PositiveInt


class User(UserBase):
    email: EmailStr
    username: str
    is_verified: bool

    class Config:
        orm_mode = True


class UserDetail(UserBase):
    email: EmailStr
    username: str
    is_verified: bool
    profile_image: str
    datetime_created: datetime
    datetime_updated: datetime
    user_address: List[UserAddress]

    class Config:
        orm_mode = True


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
