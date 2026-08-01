import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.job import JobPosting


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.wanted.co.kr/",
}

JOB_GROUP_ID = 518  # 백엔드


def fetch_job_list(limit: int = 20) -> list[dict]:
    """
    원티드 채용공고 목록을 가져옵니다.
    """
    url = "https://www.wanted.co.kr/api/v4/jobs"
    params = {
        "job_group_id": JOB_GROUP_ID,
        "country": "kr",
        "job_sort": "job.latest_order",
        "years": -1,
        "locations": "seoul",
        "limit": limit,
        "offset": 0,
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json().get("data", [])


def fetch_job_detail(job_id: int) -> dict:
    """
    채용공고 상세 정보를 가져옵니다.
    """
    url = f"https://www.wanted.co.kr/api/v4/jobs/{job_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json().get("job", {})


def parse_job(raw: dict, detail: dict) -> dict:
    """
    원티드 공고 데이터를 DB 저장 형식으로 변환합니다.
    """
    return {
        "company": raw.get("company", {}).get("name", ""),
        "title": raw.get("position", ""),
        "description": detail.get("detail", {}).get("main_tasks", ""),
        "required_skills": detail.get("detail", {}).get("requirements", ""),
        "preferred_skills": detail.get("detail", {}).get("preferred_points", ""),
        "location": raw.get("address", {}).get("location", ""),
        "career": "",
        "deadline": str(raw.get("due_time", "")) if raw.get("due_time") else None,
        "url": f"https://www.wanted.co.kr/wd/{raw.get('id')}",
        "source": "원티드",
    }


def save_jobs_to_db(limit: int = 20):
    """
    원티드 공고를 가져와서 DB에 저장합니다.
    """
    db = SessionLocal()
    try:
        jobs = fetch_job_list(limit=limit)
        saved = 0

        for raw in jobs:
            existing = db.query(JobPosting).filter(
                JobPosting.url == f"https://www.wanted.co.kr/wd/{raw['id']}"
            ).first()
            if existing:
                print(f"이미 존재: {raw['id']}")
                continue

            detail = fetch_job_detail(raw["id"])
            parsed = parse_job(raw, detail)

            job = JobPosting(**parsed)
            db.add(job)
            saved += 1
            print(f"저장완료: [{raw['id']}] {parsed['company']} - {parsed['title']}")

        db.commit()
        print(f"\n총 {saved}개 공고 저장 완료!")

    except Exception as e:
        db.rollback()
        print(f"에러: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    save_jobs_to_db(limit=10)