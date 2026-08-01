from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.db.session import get_db
from app.repositories import user_repo
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    user = user_repo.get_user_by_email(db, request.email)
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    token = create_access_token(user.id)
    return TokenResponse(access_token=token)