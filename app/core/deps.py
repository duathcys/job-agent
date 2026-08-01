from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.repositories import user_repo

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """토큰에서 현재 로그인한 유저를 반환합니다."""
    token = credentials.credentials
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    user = user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    return user