import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session
from typing import Optional

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.portfolio import Portfolio
from app.services.resume_service import extract_text_from_pdf, analyze_resume
from app.services.portfolio_service import (
    enhance_portfolio, generate_html, generate_pdf, image_to_base64
)

router = APIRouter()


@router.post("/generate")
async def generate_portfolio(
    output: str = "html",
    orientation: str = "portrait",
    form_data: Optional[str] = Form(None),
    files: list[UploadFile] = File(default=[]),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    포트폴리오를 생성합니다.
    files: PDF 이력서 + 프로젝트 이미지들
    form_data: JSON 형식의 폼 입력 데이터
    output: html 또는 pdf
    orientation: portrait(세로) 또는 landscape(가로)
    """
    import json as json_module

    base_data = {
        "name": "",
        "job": current_user.job,
        "email": current_user.email,
        "phone": "",
        "github": "",
        "intro": "",
        "skills": current_user.skills,
        "projects": [],
        "experiences": [],
        "education": {},
    }

    # 폼 데이터 적용
    if form_data:
        try:
            parsed = json_module.loads(form_data)
            base_data.update(parsed)
        except Exception:
            pass

    # 이미지 맵 {파일명: base64}
    image_map = {}

    # 파일 처리
    for file in files:
        file_bytes = await file.read()

        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_bytes)
            if text.strip():
                resume_data = await analyze_resume(text)
                if not base_data.get("name"):
                    base_data["skills"] = resume_data.get("skills", base_data["skills"])
                    base_data["job"] = resume_data.get("job", base_data["job"])
                    base_data["raw_resume"] = text

        elif file.content_type and file.content_type.startswith("image/"):
            image_map[file.filename] = image_to_base64(file_bytes, file.content_type)

    # 프로젝트 이미지 매핑
    for project in base_data.get("projects", []):
        img_key = project.get("image_filename")
        if img_key and img_key in image_map:
            project["image"] = image_map[img_key]

    enhanced = await enhance_portfolio(base_data)

    # 이미지는 enhance 후에도 유지
    for i, project in enumerate(enhanced.get("projects", [])):
        if i < len(base_data.get("projects", [])):
            orig = base_data["projects"][i]
            if orig.get("image"):
                project["image"] = orig["image"]

    if output == "pdf":
        try:
            pdf_bytes = generate_pdf(enhanced, orientation)
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=portfolio.pdf"},
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF 생성 실패: {str(e)}")

    html_content = generate_html(enhanced, orientation)

    # DB 저장
    share_token = str(uuid.uuid4())[:8]
    portfolio = Portfolio(
        user_id=current_user.id,
        title=f"{enhanced.get('name', '내')} 포트폴리오",
        data=enhanced,
        html=html_content,
        share_token=share_token,
    )
    db.add(portfolio)
    db.commit()

    return {
        "html": html_content,
        "share_token": share_token,
        "portfolio_id": portfolio.id,
    }


@router.get("/share/{token}")
def get_shared_portfolio(token: str, db: Session = Depends(get_db)):
    """공유 링크로 포트폴리오를 조회합니다."""
    portfolio = db.query(Portfolio).filter(Portfolio.share_token == token).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="포트폴리오를 찾을 수 없습니다.")
    return HTMLResponse(content=portfolio.html)


@router.get("/list")
def get_my_portfolios(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """내 포트폴리오 목록을 조회합니다."""
    portfolios = db.query(Portfolio).filter(
        Portfolio.user_id == current_user.id
    ).order_by(Portfolio.created_at.desc()).all()

    return [
        {
            "id": p.id,
            "title": p.title,
            "share_token": p.share_token,
            "created_at": str(p.created_at),
        }
        for p in portfolios
    ]