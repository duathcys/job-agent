from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
import json

from app.core.config import settings
from agent.tools.fit_score_tool import extract_skills_from_job, compare_skills, generate_fit_comment

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=settings.groq_api_key,
    temperature=0,
)

tools = [extract_skills_from_job, compare_skills, generate_fit_comment]
agent = create_react_agent(llm, tools)


def calculate_fit_score_agent(
    user_skills: list[str],
    job_title: str,
    job_required: str,
    job_preferred: str,
) -> dict:
    """
    Agent를 사용해서 적합도를 계산합니다.
    """
    user_skills_str = ",".join(user_skills)
    job_text = f"직무: {job_title}\n필수: {job_required}\n우대: {job_preferred}"

    result = agent.invoke({
        "messages": [
            HumanMessage(content=f"""
다음 순서로 적합도를 계산해줘:

1. extract_skills_from_job으로 공고에서 기술 추출
2. compare_skills로 사용자 스킬과 비교
   - user_skills_str: "{user_skills_str}"
3. generate_fit_comment로 한 줄 평가 생성

공고 정보:
{job_text[:500]}

최종적으로 JSON 형식으로 결과를 알려줘:
{{
    "fit_score": 점수,
    "matched_skills": [],
    "missing_skills": [],
    "comment": "한 줄 평가"
}}
""")
        ]
    })

    # 마지막 메시지에서 JSON 추출
    last_message = result["messages"][-1].content
    try:
        # JSON 블록 찾기
        import re
        json_match = re.search(r'\{.*\}', last_message, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception:
        pass

    return {
        "fit_score": 0,
        "matched_skills": [],
        "missing_skills": [],
        "comment": "분석 실패",
    }