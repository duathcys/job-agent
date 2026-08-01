from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from agent.graph import build_agent

router = APIRouter()


@router.post("/run")
def run_agent(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    """
    AI 에이전트를 실행합니다.
    크롤링 → 요약 → 적합도 계산 → 추천 순으로 동작합니다.
    """
    def _run():
        agent = build_agent()
        agent.invoke({
            "user_id": current_user.id,
            "user_skills": current_user.skills,
            "raw_jobs": [],
            "saved_job_ids": [],
            "summarized_jobs": [],
            "scored_jobs": [],
            "final_recommendations": [],
            "error": None,
        })

    background_tasks.add_task(_run)
    return {"message": "에이전트 실행을 시작했습니다."}


@router.get("/recommendations")
def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    현재 유저의 적합도 기준 상위 5개 공고를 반환합니다.
    """
    from app.models.job import JobPosting

    jobs = (
        db.query(JobPosting)
        .filter(JobPosting.fit_score.isnot(None))
        .order_by(JobPosting.fit_score.desc())
        .limit(5)
        .all()
    )

    return [
        {
            "id": job.id,
            "company": job.company,
            "title": job.title,
            "summary": job.summary,
            "fit_score": job.fit_score,
            "url": job.url,
            "deadline": job.deadline,
            "required_skills": job.required_skills,
        }
        for job in jobs
    ]

@router.post("/schedule/run-now")
def run_now(
    current_user: User = Depends(get_current_user),
):
    """
    스케줄러를 즉시 실행합니다. (테스트용)
    """
    from app.scheduler import run_agent_for_all_users
    from fastapi.concurrency import run_in_threadpool
    import asyncio

    asyncio.create_task(run_in_threadpool(run_agent_for_all_users))
    return {"message": "스케줄러 즉시 실행 시작"}