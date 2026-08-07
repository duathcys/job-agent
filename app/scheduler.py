from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.db.session import SessionLocal
from app.models.user import User


def collect_all_jobs():
    """
    전체 공고를 수집해서 DB에 저장합니다. (사용자 무관)
    """
    from crawler.wanted import fetch_all_jobs, fetch_job_detail, parse_job
    from app.models.job import JobPosting

    print("전체 공고 수집 시작...")
    db = SessionLocal()
    try:
        all_jobs = fetch_all_jobs(max_pages=5)  # 약 500개
        saved = 0

        for raw in all_jobs:
            existing = db.query(JobPosting).filter(
                JobPosting.url == f"https://www.wanted.co.kr/wd/{raw['id']}"
            ).first()
            if existing:
                continue

            try:
                detail = fetch_job_detail(raw["id"])
                parsed = parse_job(raw, detail)
                job = JobPosting(**parsed)
                db.add(job)
                saved += 1
            except Exception as e:
                print(f"공고 저장 오류 {raw['id']}: {e}")
                continue

        db.commit()
        print(f"전체 공고 수집 완료: {saved}개 신규 저장")

    except Exception as e:
        db.rollback()
        print(f"전체 공고 수집 오류: {e}")
    finally:
        db.close()


def analyze_jobs_for_users():
    """
    사용자별로 필터링 후 AI 분석합니다.
    """
    import asyncio
    from app.models.job import JobPosting
    from app.services.filter_service import filter_jobs_for_user
    from app.services.ai_service import summarize_job, calculate_fit_score
    from app.services.email_service import send_recommendation_email

    print("사용자별 분석 시작...")
    db = SessionLocal()
    try:
        users = db.query(User).all()
        all_jobs = db.query(JobPosting).all()

        for user in users:
            print(f"[{user.email}] 분석 중...")

            # 1. 사용자별 필터링 (AI 없이)
            filtered = filter_jobs_for_user(all_jobs, user, limit=15)
            print(f"  필터링 결과: {len(filtered)}개")

            # 2. 필터링된 것만 AI 분석
            for job in filtered:
                try:
                    # 요약
                    if not job.summary:
                        summary = asyncio.run(summarize_job(job.description or job.title))
                        job.summary = summary.get("one_line_summary", "")

                    # 적합도
                    result = asyncio.run(calculate_fit_score(
                        user_skills=user.skills or [],
                        job_required_skills=[job.required_skills] if isinstance(job.required_skills, str) else (job.required_skills or []),
                        job_preferred_skills=[job.preferred_skills] if isinstance(job.preferred_skills, str) else (job.preferred_skills or []),
                    ))
                    job.fit_score = result.get("fit_score", 0)

                except Exception as e:
                    print(f"  공고 분석 오류: {e}")
                    continue

            db.commit()

            # 3. 상위 10개 이메일 발송
            top_jobs = sorted(filtered, key=lambda j: j.fit_score or 0, reverse=True)[:10]
            job_list = [
                {
                    "company": j.company,
                    "title": j.title,
                    "summary": j.summary,
                    "fit_score": j.fit_score,
                    "url": j.url,
                    "deadline": j.deadline,
                }
                for j in top_jobs
            ]
            send_recommendation_email(user.email, job_list)
            print(f"  [{user.email}] 완료")

    except Exception as e:
        db.rollback()
        print(f"사용자별 분석 오류: {e}")
    finally:
        db.close()


def run_agent_for_all_users():
    """전체 파이프라인 실행"""
    collect_all_jobs()
    analyze_jobs_for_users()


def start_scheduler():
    scheduler = BackgroundScheduler()

    # 매일 새벽 3시 공고 수집
    scheduler.add_job(
        collect_all_jobs,
        trigger=CronTrigger(hour=3, minute=0),
        id="collect_jobs",
        name="전체 공고 수집",
        replace_existing=True,
    )

    # 매일 오전 8시 사용자별 분석 + 이메일
    scheduler.add_job(
        analyze_jobs_for_users,
        trigger=CronTrigger(hour=8, minute=0),
        id="analyze_jobs",
        name="사용자별 분석 및 이메일",
        replace_existing=True,
    )

    scheduler.start()
    print("스케줄러 시작 (새벽 3시 수집, 오전 8시 분석)")
    return scheduler