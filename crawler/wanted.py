import requests
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.wanted.co.kr/",
}

JOB_KEYWORDS = {
    "백엔드": ["백엔드", "back-end", "backend", "서버", "server", "java", "spring", "python", "node", "django", "fastapi", "kotlin", "golang", "php", "scala"],
    "프론트엔드": ["프론트엔드", "front-end", "frontend", "react", "vue", "angular", "javascript", "typescript"],
    "풀스택": ["풀스택", "full-stack", "fullstack"],
    "데이터": ["데이터", "data", "ml", "ai", "머신러닝", "딥러닝"],
    "devops": ["devops", "infra", "인프라", "sre", "kubernetes", "docker"],
    "ios": ["ios", "swift"],
    "android": ["android", "안드로이드"],
}


def get_keywords_for_job(job: str) -> list[str]:
    job_lower = job.lower()
    for key, keywords in JOB_KEYWORDS.items():
        if key in job_lower or job_lower in key:
            return keywords
    return [job_lower]


def is_matching_job(position: str, keywords: list[str]) -> bool:
    position_lower = position.lower()
    return any(keyword in position_lower for keyword in keywords)


def fetch_all_jobs(max_pages: int = 5) -> list[dict]:
    """
    원티드 전체 공고를 페이지네이션으로 수집합니다.
    사용자 무관하게 전체 수집.
    max_pages: 가져올 페이지 수 (1페이지 = 100개)
    """
    url = "https://www.wanted.co.kr/api/v4/jobs"
    all_jobs = []

    for page in range(max_pages):
        offset = page * 100
        params = {
            "country": "kr",
            "job_sort": "job.latest_order",
            "years": -1,
            "locations": "all",
            "limit": 100,
            "offset": offset,
        }
        try:
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            batch = response.json().get("data", [])

            if not batch:
                break

            all_jobs.extend(batch)
            print(f"페이지 {page + 1}: {len(batch)}개 수집 (누적 {len(all_jobs)}개)")
            time.sleep(0.5)

        except Exception as e:
            print(f"페이지 {page + 1} 수집 오류: {e}")
            break

    return all_jobs


def fetch_job_list(limit: int = 100, job: str = "백엔드") -> list[dict]:
    """
    사용자 직무에 맞는 공고를 필터링해서 반환합니다.
    """
    all_jobs = fetch_all_jobs(max_pages=3)
    keywords = get_keywords_for_job(job)
    filtered = [j for j in all_jobs if is_matching_job(j.get("position", ""), keywords)]
    print(f"전체 {len(all_jobs)}개 중 {len(filtered)}개 필터링")
    return filtered[:limit]


def fetch_job_detail(job_id: int) -> dict:
    url = f"https://www.wanted.co.kr/api/v4/jobs/{job_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json().get("job", {})


def parse_job(raw: dict, detail: dict) -> dict:
    return {
        "company": raw.get("company", {}).get("name", ""),
        "title": raw.get("position", ""),
        "description": detail.get("detail", {}).get("main_tasks", ""),
        "required_skills": detail.get("detail", {}).get("requirements", ""),
        "preferred_skills": detail.get("detail", {}).get("preferred_points", ""),
        "location": raw.get("address", {}).get("location", ""),
        "career": str(raw.get("annual_from", "")) if raw.get("annual_from") is not None else "",
        "deadline": str(raw.get("due_time", "")) if raw.get("due_time") else None,
        "url": f"https://www.wanted.co.kr/wd/{raw.get('id')}",
        "source": "원티드",
    }