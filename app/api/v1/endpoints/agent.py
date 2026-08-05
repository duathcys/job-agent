import asyncio
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User

router = APIRouter()


@router.get("/run-stream")
async def run_agent_stream(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    AI 에이전트를 실행하고 진행상황을 실시간으로 전송합니다.
    """
    user_id = current_user.id
    user_skills = current_user.skills
    user_email = current_user.email

    async def event_stream():
        try:
            from app.models.job import JobPosting
            from app.services.email_service import send_recommendation_email
            from app.db.session import SessionLocal
            from crawler.wanted import fetch_job_list, fetch_job_detail, parse_job
            from app.services.ai_service import summarize_job, calculate_fit_score

            yield "data: {\"step\": 1, \"message\": \"🔍 채용공고 수집 중...\"}\n\n"
            await asyncio.sleep(0)

            db2 = SessionLocal()
            raw_jobs = fetch_job_list(limit=10)
            saved_ids = []

            for raw in raw_jobs:
                existing = db2.query(JobPosting).filter(
                    JobPosting.url == f"https://www.wanted.co.kr/wd/{raw['id']}"
                ).first()
                if existing:
                    saved_ids.append(existing.id)
                    continue
                detail = fetch_job_detail(raw["id"])
                parsed = parse_job(raw, detail)
                job = JobPosting(**parsed)
                db2.add(job)
                db2.flush()
                saved_ids.append(job.id)

            db2.commit()

            yield f"data: {{\"step\": 1, \"message\": \"✅ {len(saved_ids)}개 공고 수집 완료\"}}\n\n"
            await asyncio.sleep(0)

            yield "data: {\"step\": 2, \"message\": \"📝 공고 요약 중...\"}\n\n"
            await asyncio.sleep(0)

            for job_id in saved_ids:
                job = db2.query(JobPosting).filter(JobPosting.id == job_id).first()
                if not job:
                    continue
                summary = await summarize_job(job.description or job.title)
                job.summary = summary.get("one_line_summary", "")

            db2.commit()

            yield "data: {\"step\": 2, \"message\": \"✅ 공고 요약 완료\"}\n\n"
            await asyncio.sleep(0)

            yield "data: {\"step\": 3, \"message\": \"🎯 적합도 계산 중...\"}\n\n"
            await asyncio.sleep(0)

            for job_id in saved_ids:
                job = db2.query(JobPosting).filter(JobPosting.id == job_id).first()
                if not job:
                    continue
                result = await calculate_fit_score(
                    user_skills=user_skills,
                    job_required_skills=job.required_skills or [],
                    job_preferred_skills=job.preferred_skills or [],
                )
                job.fit_score = result.get("fit_score", 0)

            db2.commit()

            yield "data: {\"step\": 3, \"message\": \"✅ 적합도 계산 완료\"}\n\n"
            await asyncio.sleep(0)

            yield "data: {\"step\": 4, \"message\": \"📧 이메일 발송 중...\"}\n\n"
            await asyncio.sleep(0)

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

            send_recommendation_email(user_email, job_list)

            yield "data: {\"step\": 4, \"message\": \"✅ 이메일 발송 완료!\", \"done\": true}\n\n"

        except Exception as e:
            import traceback
            traceback.print_exc()
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


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