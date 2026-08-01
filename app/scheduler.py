from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.db.session import SessionLocal
from app.models.user import User


def run_agent_for_all_users():
    from agent.graph import build_agent
    from app.models.job import JobPosting
    from app.services.email_service import send_recommendation_email

    print("⏰ 스케줄러 실행 시작...")
    db = SessionLocal()

    try:
        users = db.query(User).all()
        print(f"👥 총 {len(users)}명의 유저에 대해 에이전트 실행")

        for user in users:
            print(f"\n🔄 [{user.email}] 에이전트 실행 중...")
            agent = build_agent()
            agent.invoke({
                "user_id": user.id,
                "user_skills": user.skills,
                "raw_jobs": [],
                "saved_job_ids": [],
                "summarized_jobs": [],
                "scored_jobs": [],
                "final_recommendations": [],
                "error": None,
            })

            # 추천 공고 조회
            jobs = (
                db.query(JobPosting)
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

            # 이메일 발송
            send_recommendation_email(user.email, job_list)
            print(f"✅ [{user.email}] 완료")

    except Exception as e:
        print(f"❌ 스케줄러 에러: {e}")
    finally:
        db.close()

    print("\n⏰ 스케줄러 실행 완료!")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_agent_for_all_users,
        trigger=CronTrigger(hour=9, minute=0),
        id="daily_agent",
        name="매일 채용공고 수집 및 추천",
        replace_existing=True,
    )
    scheduler.start()
    print("✅ 스케줄러 시작 (매일 오전 9시 실행)")
    return scheduler