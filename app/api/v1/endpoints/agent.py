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
    db: Session = Depends(get_db),
):
    def _run():
        from app.models.job import JobPosting
        from app.services.email_service import send_recommendation_email

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

        # 추천 공고 조회
        from app.db.session import SessionLocal
        db2 = SessionLocal()
        jobs = (
            db2.query(JobPosting)
            .filter(JobPosting.fit_score.isnot(None))
            .order_by(JobPosting.fit_score.desc())
            .limit(5)
            .all()
        )

        job_list = [
            {
                "company": job.company,
                "title": job.title,
                "summary": job.summary,
                "fit_score": job.fit_score,
                "url": job.url,
                "deadline": job.deadline,
            }
            for job in jobs
        ]
        db2.close()

        send_recommendation_email(current_user.email, job_list)

    background_tasks.add_task(_run)
    return {"message": "에이전트 실행을 시작했습니다. 완료 후 이메일로 결과를 보내드립니다!"}


@router.get("/recommendations")
def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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
    from app.scheduler import run_agent_for_all_users
    import threading
    threading.Thread(target=run_agent_for_all_users).start()
    return {"message": "스케줄러 즉시 실행 시작"}