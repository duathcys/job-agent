import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agent.state import AgentState
from crawler.wanted import fetch_job_list, fetch_job_detail, parse_job, save_jobs_to_db
from app.db.session import SessionLocal
from app.models.job import JobPosting


def crawl_node(state: AgentState) -> AgentState:
    """
    원티드에서 채용공고를 수집하고 DB에 저장합니다.
    """
    print("🔍 [1/4] 채용공고 수집 중...")
    try:
        db = SessionLocal()
        raw_jobs = fetch_job_list(limit=10)
        saved_ids = []

        for raw in raw_jobs:
            existing = db.query(JobPosting).filter(
                JobPosting.url == f"https://www.wanted.co.kr/wd/{raw['id']}"
            ).first()

            if existing:
                saved_ids.append(existing.id)
                continue

            detail = fetch_job_detail(raw["id"])
            parsed = parse_job(raw, detail)
            job = JobPosting(**parsed)
            db.add(job)
            db.flush()
            saved_ids.append(job.id)

        db.commit()
        db.close()

        print(f"✅ {len(saved_ids)}개 공고 수집 완료")
        return {**state, "raw_jobs": raw_jobs, "saved_job_ids": saved_ids}

    except Exception as e:
        db.rollback()
        db.close()
        return {**state, "error": str(e)}