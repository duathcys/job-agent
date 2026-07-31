import json
from groq import Groq

from app.core.config import settings

client = Groq(api_key=settings.groq_api_key)


async def summarize_job(description: str) -> dict:
    """
    채용공고 원문을 받아 구조화된 요약을 반환합니다.
    """
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
    return json.loads(response.choices[0].message.content)


async def calculate_fit_score(
    user_skills: list[str],
    job_required_skills: list[str],
    job_preferred_skills: list[str],
) -> dict:
    """
    사용자 기술스택과 공고 기술스택을 비교해 적합도를 반환합니다.
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""
사용자의 기술스택과 채용공고의 요구 기술을 비교해서 적합도를 분석해줘.

사용자 기술스택: {user_skills}
필수 기술: {job_required_skills}
우대 기술: {job_preferred_skills}

출력 형식 (JSON만 출력, 다른 말 하지 말 것):
{{
    "fit_score": 85,
    "matched_skills": ["Java", "Spring"],
    "missing_skills": ["Docker"],
    "comment": "한 줄 평가"
}}
""",
            }
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)