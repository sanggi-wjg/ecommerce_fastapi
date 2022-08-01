from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.database.models import UserEntity, AddressEntity, UserAddressEntity
from app.schema.user_address_schema import AddressCreate
from app.schema.user_schema import UserCreate


def find_user_by_id(db: Session, user_id: int) -> UserEntity:
    return db.query(UserEntity).filter(UserEntity.id == user_id).first()


def find_authenticate_user_by_email(db: Session, email: str) -> UserEntity:
    return db.query(UserEntity).filter(
        UserEntity.email == email,
        UserEntity.is_verified == True,
    ).first()


def find_user_address_by_user_id(db: Session, user_id: int) -> List[UserAddressEntity]:
    return db.query(UserAddressEntity).join(
        UserEntity.user_address
    ).filter(
        UserAddressEntity.user_id == user_id
    ).all()


def find_user_all_by_page(db: Session, offset: int, limit: int) -> List[UserEntity]:
    return db.query(UserEntity).outerjoin(
        UserAddressEntity
        # ).join(        AddressEntity, AddressEntity.id == UserAddressEntity.address_id
    ).offset(offset).limit(limit).all()


def create_new_user(db: Session, user_create: UserCreate) -> UserEntity:
    new_user = UserEntity(
        **user_create.dict(exclude={'password1', 'password2'}),
        password=user_create.hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user_verified(db: Session, user_entity: UserEntity) -> UserEntity:
    user_entity.is_verified = True

    db.commit()
    db.refresh(user_entity)
    return user_entity


def update_user_profile_path(db: Session, user_id: int, profile_image: str) -> UserEntity:
    find_user = find_user_by_id(db, user_id)
    if not find_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {
            "message": "error", "detail": "not exist user"
        })

    find_user.profile_image = profile_image

    db.commit()
    db.refresh(find_user)
    return find_user


def create_user_address(db: Session, user_id: int, address: AddressCreate) -> AddressEntity:
    try:
        new_address = AddressEntity(**address.dict())
        db.add(new_address)
        db.commit()
        db.refresh(new_address)

        new_user_address = UserAddressEntity(
            address_id=new_address.id,
            user_id=user_id
        )
        db.add(new_user_address)
        db.commit()
        db.refresh(new_user_address)
        return new_address

    except Exception:
        db.rollback()
