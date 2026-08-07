from langchain_core.tools import tool
from crawler.wanted import fetch_job_list, fetch_job_detail, parse_job
from app.db.session import SessionLocal
from app.models.job import JobPosting


@tool
def search_jobs(job: str = "백엔드", limit: int = 10) -> str:
    """
    원티드에서 채용공고를 검색하고 DB에 저장합니다.
    job: 희망 직무 (예: 백엔드, 프론트엔드)
    limit: 가져올 공고 수
    """
    try:
        db = SessionLocal()
        raw_jobs = fetch_job_list(limit=limit, job=job)
        saved = 0

        for raw in raw_jobs:
            existing = db.query(JobPosting).filter(
                JobPosting.url == f"https://www.wanted.co.kr/wd/{raw['id']}"
            ).first()
            if existing:
                continue

            detail = fetch_job_detail(raw["id"])
            parsed = parse_job(raw, detail)
            job_obj = JobPosting(**parsed)
            db.add(job_obj)
            saved += 1

        db.commit()
        db.close()
        return f"{job} 직무 공고 {len(raw_jobs)}개 검색, {saved}개 신규 저장 완료"
    except Exception as e:
        return f"공고 검색 실패: {str(e)}"