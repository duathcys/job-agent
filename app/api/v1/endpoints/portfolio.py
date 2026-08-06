from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.resume_service import extract_text_from_pdf, analyze_resume
from app.services.portfolio_service import enhance_portfolio, generate_html, generate_pdf

router = APIRouter()


@router.post("/generate")
async def generate_portfolio(
    output: str = "html",
    file: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    포트폴리오를 생성합니다.
    file: PDF 이력서 (선택)
    output: html 또는 pdf
    """
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

    if file and file.filename.endswith(".pdf"):
        file_bytes = await file.read()
        text = extract_text_from_pdf(file_bytes)
        if text.strip():
            resume_data = await analyze_resume(text)
            base_data.update({
                "skills": resume_data.get("skills", current_user.skills),
                "job": resume_data.get("job", current_user.job),
            })
            base_data["raw_resume"] = text

    enhanced = await enhance_portfolio(base_data)

    if output == "pdf":
        try:
            pdf_bytes = generate_pdf(enhanced)
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=portfolio.pdf"},
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF 생성 실패: {str(e)}")

    html_content = generate_html(enhanced)
    return HTMLResponse(content=html_content)