from app.models.job import JobPosting
from app.models.user import User


def filter_jobs_for_user(jobs: list[JobPosting], user: User, limit: int = 15) -> list[JobPosting]:
    """
    사용자 정보를 기반으로 공고를 필터링합니다.
    AI 없이 빠르게 처리합니다.
    """
    scored = []

    user_skills = [s.lower() for s in (user.skills or [])]
    user_interests = [i.lower() for i in (user.interests or [])]
    user_job = (user.job or "").lower()
    user_career = (user.career or "").lower()

    for job in jobs:
        score = 0
        title = (job.title or "").lower()
        company = (job.company or "").lower()
        required = (job.required_skills or "").lower() if isinstance(job.required_skills, str) else ""
        preferred = (job.preferred_skills or "").lower() if isinstance(job.preferred_skills, str) else ""
        career = (job.career or "").lower()

        # 1. 직무 키워드 매칭 (가장 중요)
        job_keywords = _get_job_keywords(user_job)
        job_match = sum(1 for kw in job_keywords if kw in title)
        score += job_match * 30

        # 2. 관심 기업 매칭
        if any(interest in company for interest in user_interests):
            score += 50

        # 3. 기술스택 매칭
        skill_match = sum(1 for skill in user_skills if skill in required or skill in preferred)
        score += skill_match * 10

        # 4. 경력 조건
        if "신입" in user_career:
            if "신입" in title or "주니어" in title or "junior" in title:
                score += 20
            if career and int(career) > 3 if career.isdigit() else False:
                score -= 30  # 경력 3년 이상이면 감점

        # 5. 직무가 아예 안 맞으면 제외
        if job_match == 0 and score < 10:
            continue

        scored.append((score, job))

    # 점수 높은 순으로 정렬
    scored.sort(key=lambda x: x[0], reverse=True)
    return [job for _, job in scored[:limit]]


def _get_job_keywords(job: str) -> list[str]:
    JOB_KEYWORDS = {
        "백엔드": ["백엔드", "backend", "back-end", "서버", "server"],
        "프론트엔드": ["프론트엔드", "frontend", "front-end"],
        "풀스택": ["풀스택", "fullstack", "full-stack"],
        "데이터": ["데이터", "data engineer", "데이터 엔지니어"],
        "devops": ["devops", "인프라", "sre"],
        "ios": ["ios", "swift"],
        "android": ["android", "안드로이드"],
    }
    for key, keywords in JOB_KEYWORDS.items():
        if key in job or job in key:
            return keywords
    return [job.lower(), job]