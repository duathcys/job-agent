from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.resume_service import extract_text_from_pdf, analyze_resume
from app.repositories import user_repo
from app.schemas.user import UserUpdate

router = APIRouter()


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    apply: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    PDF 이력서를 업로드하고 AI로 분석합니다.
    apply=True 이면 분석 결과를 프로필에 자동 반영합니다.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="PDF 파일만 업로드 가능합니다.")

    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="파일 크기는 10MB 이하여야 합니다.")

    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)

    if not text.strip():
        raise HTTPException(status_code=400, detail="PDF에서 텍스트를 추출할 수 없습니다.")

    result = await analyze_resume(text)

    if apply:
        user_repo.update_user(db, current_user, UserUpdate(
            skills=result.get("skills", []),
            career=result.get("career", current_user.career),
            job=result.get("job", current_user.job),
        ))

    return {
        "message": "이력서 분석 완료",
        "result": result,
        "applied": apply,
    }