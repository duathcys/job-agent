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
    """
    사용자 기술스택과 공고 기술스택을 비교해 적합도를 반환합니다.
    Agent 기반으로 정확도 향상.
    """
    from agent.fit_score_agent import calculate_fit_score_agent

    required_text = job_required_skills if isinstance(job_required_skills, str) else " ".join(job_required_skills or [])
    preferred_text = job_preferred_skills if isinstance(job_preferred_skills, str) else " ".join(job_preferred_skills or [])

    try:
        result = calculate_fit_score_agent(
            user_skills=user_skills,
            job_title=job_title,
            job_required=required_text,
            job_preferred=preferred_text,
        )
        return result
    except Exception as e:
        print(f"Agent 적합도 계산 오류: {e}")
        # fallback
        matched = list(set([s.lower() for s in user_skills]) &
                      set([s.lower() for s in (job_required_skills if isinstance(job_required_skills, list) else [])]))
        return {
            "fit_score": len(matched) * 10,
            "matched_skills": matched,
            "missing_skills": [],
            "comment": "기본 매칭으로 계산됨",
        }