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
    user_email = current_user.email
    user_skills = current_user.skills
    user_id = current_user.id

    def _run():
        try:
            from app.models.job import JobPosting
            from app.services.email_service import send_recommendation_email
            from app.db.session import SessionLocal

            agent = build_agent()
            agent.invoke({
                "user_id": user_id,
                "user_skills": user_skills,
                "raw_jobs": [],
                "saved_job_ids": [],
                "summarized_jobs": [],
                "scored_jobs": [],
                "final_recommendations": [],
                "error": None,
            })

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

            print(f"📧 이메일 발송 시도: {user_email}")
            send_recommendation_email(user_email, job_list)

        except Exception as e:
            print(f"❌ _run 에러: {e}")
            import traceback
            traceback.print_exc()

    background_tasks.add_task(_run)
    return {"message": "에이전트 실행을 시작했습니다. 완료 후 이메일로 결과를 보내드립니다!"}