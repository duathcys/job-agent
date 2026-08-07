from langchain_core.tools import tool
from app.db.session import SessionLocal
from app.models.job import JobPosting


@tool
def get_recommendations(user_id: int, limit: int = 5) -> str:
    """
    DB에서 적합도 높은 공고를 조회합니다.
    user_id: 사용자 ID
    limit: 조회할 공고 수
    """
    try:
        db = SessionLocal()
        jobs = (
            db.query(JobPosting)
            .filter(JobPosting.fit_score.isnot(None))
            .order_by(JobPosting.fit_score.desc())
            .limit(limit)
            .all()
        )
        db.close()

        if not jobs:
            return "추천 공고가 없습니다. 먼저 공고를 검색해주세요."

        result = []
        for job in jobs:
            result.append(
                f"[{job.fit_score}%] {job.company} - {job.title}\n"
                f"  마감: {job.deadline or '미정'}\n"
                f"  링크: {job.url}"
            )
        return "\n\n".join(result)
    except Exception as e:
        return f"공고 조회 실패: {str(e)}"


@tool
def search_jobs_by_keyword(keyword: str) -> str:
    """
    키워드로 DB에서 공고를 검색합니다.
    keyword: 검색할 키워드 (예: Docker, AWS, 네이버)
    """
    try:
        db = SessionLocal()
        jobs = db.query(JobPosting).filter(
            JobPosting.title.ilike(f"%{keyword}%") |
            JobPosting.company.ilike(f"%{keyword}%") |
            JobPosting.description.ilike(f"%{keyword}%")
        ).limit(5).all()
        db.close()

        if not jobs:
            return f"'{keyword}' 관련 공고를 찾을 수 없습니다."

        result = []
        for job in jobs:
            result.append(
                f"{job.company} - {job.title}\n"
                f"  적합도: {job.fit_score or '미계산'}%\n"
                f"  링크: {job.url}"
            )
        return "\n\n".join(result)
    except Exception as e:
        return f"검색 실패: {str(e)}"