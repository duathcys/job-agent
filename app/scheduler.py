from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.db.session import SessionLocal
from app.models.user import User


def run_agent_for_all_users():
    """
    모든 유저에 대해 AI 에이전트를 실행합니다.
    """
    from agent.graph import build_agent

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
            print(f"✅ [{user.email}] 완료")

    except Exception as e:
        print(f"❌ 스케줄러 에러: {e}")
    finally:
        db.close()

    print("\n⏰ 스케줄러 실행 완료!")


def start_scheduler():
    """
    스케줄러를 시작합니다.
    매일 오전 9시에 실행됩니다.
    """
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        run_agent_for_all_users,
        trigger=CronTrigger(hour=9, minute=0),  # 매일 오전 9시
        id="daily_agent",
        name="매일 채용공고 수집 및 추천",
        replace_existing=True,
    )

    scheduler.start()
    print("✅ 스케줄러 시작 (매일 오전 9시 실행)")
    return scheduler