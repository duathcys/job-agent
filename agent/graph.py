from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent.nodes.crawl_node import crawl_node
from agent.nodes.summarize_node import summarize_node
from agent.nodes.score_node import score_node
from agent.nodes.recommend_node import recommend_node


def should_continue(state: AgentState) -> str:
    """에러 발생 시 종료합니다."""
    if state.get("error"):
        print(f"❌ 에러 발생: {state['error']}")
        return "end"
    return "continue"


def build_agent() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("crawl", crawl_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("score", score_node)
    graph.add_node("recommend", recommend_node)

    graph.set_entry_point("crawl")

    graph.add_conditional_edges("crawl", should_continue, {
        "continue": "summarize",
        "end": END,
    })
    graph.add_conditional_edges("summarize", should_continue, {
        "continue": "score",
        "end": END,
    })
    graph.add_conditional_edges("score", should_continue, {
        "continue": "recommend",
        "end": END,
    })
    graph.add_edge("recommend", END)

    return graph.compile()


if __name__ == "__main__":
    from app.db.session import SessionLocal
    from app.models.user import User

    db = SessionLocal()
    user = db.query(User).filter(User.id == 1).first()
    db.close()

    agent = build_agent()
    result = agent.invoke({
        "user_id": user.id,
        "user_skills": user.skills,
        "raw_jobs": [],
        "saved_job_ids": [],
        "summarized_jobs": [],
        "scored_jobs": [],
        "final_recommendations": [],
        "error": None,
    }) 