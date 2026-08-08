from langchain_core.tools import tool
from app.db.session import SessionLocal
from app.models.job import JobPosting
from app.models.user import User


@tool
def calculate_fit_scores(user_id: int) -> str:
    """
    DB에 저장된 공고들의 적합도를 계산합니다.
    user_id: 사용자 ID
    """
    import asyncio
    from app.services.ai_service import calculate_fit_score

    try:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return "사용자를 찾을 수 없습니다."

        jobs = db.query(JobPosting).filter(
            JobPosting.fit_score.is_(None)
        ).limit(10).all()

        for job in jobs:
            result = asyncio.run(calculate_fit_score(
                user_skills=user.skills,
                job_required_skills=job.required_skills or [],
                job_preferred_skills=job.preferred_skills or [],
                job_title=job.title or "",
            ))
            job.fit_score = result.get("fit_score", 0)

        db.commit()
        db.close()
        return f"{len(jobs)}개 공고 적합도 계산 완료"
    except Exception as e:
        return f"적합도 계산 실패: {str(e)}"