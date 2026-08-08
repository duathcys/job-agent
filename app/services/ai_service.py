import json
from groq import Groq

from app.core.config import settings

client = Groq(api_key=settings.groq_api_key)


async def summarize_job(description: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""
다음 채용공고를 아래 JSON 형식으로 요약해줘.

채용공고:
{description}

출력 형식 (JSON만 출력, 다른 말 하지 말 것):
{{
    "company": "회사명",
    "title": "직무명",
    "main_tasks": ["주요업무1", "주요업무2"],
    "required_skills": ["필수기술1", "필수기술2"],
    "preferred_skills": ["우대기술1", "우대기술2"],
    "deadline": "마감일",
    "one_line_summary": "한 줄 요약"
}}
""",
            }
        ],
        response_format={"type": "json_object"},
    )
    result = json.loads(response.choices[0].message.content)
    # list로 오는 경우 처리
    if isinstance(result, list):
        result = result[0] if result else {}
    return result


async def calculate_fit_score(
    user_skills: list[str],
    job_required_skills: list,
    job_preferred_skills: list,
    job_title: str = "",
) -> dict:
    required_text = job_required_skills if isinstance(job_required_skills, str) else " ".join(job_required_skills or [])
    preferred_text = job_preferred_skills if isinstance(job_preferred_skills, str) else " ".join(job_preferred_skills or [])

    # 1단계: 공고에서 기술스택 추출
    try:
        extract_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "기술스택만 추출해서 JSON으로 반환. 다른 말 금지.",
                },
                {
                    "role": "user",
                    "content": f"""
공고에서 기술스택만 추출해줘.
프로그래밍 언어, 프레임워크, DB, 인프라, 툴만 포함.

필수:
{required_text[:500]}

우대:
{preferred_text[:300]}

출력 (JSON만):
{{
    "required": ["Java", "Spring"],
    "preferred": ["Docker", "AWS"]
}}
""",
                }
            ],
            response_format={"type": "json_object"},
        )
        extracted = json.loads(extract_response.choices[0].message.content)
        required_skills = [s.lower() for s in extracted.get("required", [])]
        preferred_skills = [s.lower() for s in extracted.get("preferred", [])]
    except Exception:
        required_skills = []
        preferred_skills = []

    # 2단계: 코드로 매칭 계산
    user_skills_lower = [s.lower() for s in user_skills]

    matched_required = [
        s for s in required_skills
        if any(u in s or s in u for u in user_skills_lower)
    ]
    missing_required = [s for s in required_skills if s not in matched_required]
    matched_preferred = [
        s for s in preferred_skills
        if any(u in s or s in u for u in user_skills_lower)
    ]
    missing_preferred = [s for s in preferred_skills if s not in matched_preferred]

    # 점수 계산
    required_score = (len(matched_required) / len(required_skills) * 70) if required_skills else 35
    preferred_score = (len(matched_preferred) / len(preferred_skills) * 30) if preferred_skills else 15
    fit_score = round(required_score + preferred_score)

    # 3단계: 코멘트 생성
    try:
        comment_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": f"""
취업 지원 관점에서 1문장으로 평가해줘.

적합도: {fit_score}%
직무: {job_title}
보유 기술: {', '.join(matched_required) or '없음'}
부족한 기술: {', '.join(missing_required) or '없음'}

한국어 1문장만 출력.
""",
                }
            ],
        )
        comment = comment_response.choices[0].message.content.strip()
    except Exception:
        comment = f"필수 기술 {len(required_skills)}개 중 {len(matched_required)}개 보유"

    return {
        "fit_score": fit_score,
        "matched_skills": matched_required,
        "missing_skills": missing_required + missing_preferred,
        "comment": comment,
    }