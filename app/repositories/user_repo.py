from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user_data: UserCreate) -> User:
    user = User(
        email=user_data.email,
        password=user_data.password,
        job=user_data.job,
        location=user_data.location,
        career=user_data.career,
        skills=user_data.skills,
        interests=user_data.interests,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user: User, user_data: UserUpdate) -> User:
    if user_data.job is not None:
        user.job = user_data.job
    if user_data.location is not None:
        user.location = user_data.location
    if user_data.career is not None:
        user.career = user_data.career
    if user_data.skills is not None:
        user.skills = user_data.skills
    if user_data.interests is not None:
        user.interests = user_data.interests
    db.commit()
    db.refresh(user)
    return user