from langchain_core.tools import tool
from groq import Groq
import json

from app.core.config import settings

client = Groq(api_key=settings.groq_api_key)


@tool
def extract_skills_from_job(job_text: str) -> str:
    """
    채용공고 텍스트에서 기술스택을 추출합니다.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "기술스택만 추출해서 JSON으로 반환. 다른 말 하지 말 것.",
                },
                {
                    "role": "user",
                    "content": f"""
다음 채용공고에서 기술스택만 추출해줘.
언어, 프레임워크, DB, 인프라, 툴 등만 포함.
자격요건, 경력, 학력 등은 제외.

공고 내용:
{job_text[:1000]}

출력 형식 (JSON만):
{{
    "required": ["Java", "Spring", "MySQL"],
    "preferred": ["Docker", "AWS"]
}}
""",
                }
            ],
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"required": [], "preferred": []})


@tool
def compare_skills(user_skills_str: str, job_skills_str: str) -> str:
    """
    사용자 스킬과 공고 스킬을 비교해서 점수를 계산합니다.
    user_skills_str: 쉼표로 구분된 사용자 기술 (예: "Java,Spring,MySQL")
    job_skills_str: JSON 형식의 공고 기술
    """
    try:
        user_skills = [s.strip().lower() for s in user_skills_str.split(",")]
        job_data = json.loads(job_skills_str)
        required = [s.lower() for s in job_data.get("required", [])]
        preferred = [s.lower() for s in job_data.get("preferred", [])]

        # 필수 기술 매칭
        matched_required = [s for s in required if any(u in s or s in u for u in user_skills)]
        missing_required = [s for s in required if s not in [m for m in matched_required]]

        # 우대 기술 매칭
        matched_preferred = [s for s in preferred if any(u in s or s in u for u in user_skills)]
        missing_preferred = [s for s in preferred if s not in [m for m in matched_preferred]]

        # 점수 계산
        if required:
            required_score = len(matched_required) / len(required) * 70
        else:
            required_score = 35

        if preferred:
            preferred_score = len(matched_preferred) / len(preferred) * 30
        else:
            preferred_score = 15

        total_score = round(required_score + preferred_score)

        result = {
            "fit_score": total_score,
            "matched_required": matched_required,
            "missing_required": missing_required,
            "matched_preferred": matched_preferred,
            "missing_preferred": missing_preferred,
        }
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"fit_score": 0, "error": str(e)})


@tool
def generate_fit_comment(score: int, matched_str: str, missing_str: str) -> str:
    """
    적합도 점수와 매칭 결과를 바탕으로 한 줄 평가를 생성합니다.
    score: 적합도 점수
    matched_str: 보유 기술 (쉼표 구분)
    missing_str: 부족한 기술 (쉼표 구분)
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": f"""
다음 정보를 바탕으로 취업 지원 관점에서 한 줄 평가를 해줘.
너무 길지 않게 1-2문장으로.

적합도: {score}%
보유 기술: {matched_str or "없음"}
부족한 기술: {missing_str or "없음"}

한국어로 답변해줘.
""",
                }
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"적합도 {score}% - 분석 중 오류 발생"