from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

from app.core.config import settings
from agent.tools.search_jobs_tool import search_jobs
from agent.tools.fit_score_tool import calculate_fit_scores
from agent.tools.db_search_tool import get_recommendations, search_jobs_by_keyword

llm = ChatGroq(
    mmodel="llama-3.1-8b-instant",
    api_key=settings.groq_api_key,
    temperature=0,
)

tools = [
    search_jobs,
    calculate_fit_scores,
    get_recommendations,
    search_jobs_by_keyword,
]

agent = create_react_agent(llm, tools)


def run_react_agent(user_id: int, user_skills: list[str], message: str) -> str:
    """
    ReAct Agent를 실행합니다.
    """
    system_prompt = f"""당신은 취업 준비를 도와주는 AI 에이전트입니다.
사용자 정보:
- user_id: {user_id}
- 보유 기술: {', '.join(user_skills)}

사용자의 요청을 분석하고 적절한 Tool을 사용해서 답변해주세요.
한국어로 답변해주세요."""

    result = agent.invoke({
        "messages": [
            HumanMessage(content=f"{system_prompt}\n\n사용자 요청: {message}")
        ]
    })

    return result["messages"][-1].content