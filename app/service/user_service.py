from typing import List

from sqlalchemy.orm import Session

from app.database.models import UserEntity
from app.schema.user_schema import UserCreate


def find_user_by_id(db: Session, user_id: int) -> UserEntity:
    return db.query(UserEntity).filter(UserEntity.id == user_id).first()


def find_authenticate_user_by_email(db: Session, email: str) -> UserEntity:
    return db.query(UserEntity).filter(
        UserEntity.email == email,
        UserEntity.is_verified is True,
    ).first()


def find_user_all_by_page(db: Session, offset: int, limit: int) -> List[UserEntity]:
    return db.query(UserEntity).offset(offset).limit(limit).all()


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
