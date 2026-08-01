from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.security import hash_password
from app.repositories import user_repo
from app.schemas.user import UserCreate
from app.models.user import User


def create_user(db: Session, user_data: UserCreate) -> User:
    existing = user_repo.get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    user_data.password = hash_password(user_data.password)
    return user_repo.create_user(db, user_data)


def get_user(db: Session, user_id: int) -> User:
    user = user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    return user