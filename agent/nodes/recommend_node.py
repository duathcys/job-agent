from agent.state import AgentState


def recommend_node(state: AgentState) -> AgentState:
    """
    적합도 기준으로 상위 5개 공고를 추천합니다.
    """
    print("🏆 [4/4] 최종 추천 생성 중...")

    scored = state["scored_jobs"]
    top5 = sorted(scored, key=lambda x: x["fit_score"], reverse=True)[:5]

    print(f"\n{'='*50}")
    print("🎉 최종 추천 공고")
    print(f"{'='*50}")
    for i, job in enumerate(top5, 1):
        print(f"\n#{i} [{job['fit_score']}%] {job['company']} - {job['title']}")
        print(f"   ✅ 보유: {job['matched_skills']}")
        print(f"   ❌ 부족: {job['missing_skills']}")
        print(f"   💬 {job['comment']}")
        print(f"   🔗 {job['url']}")

    return {**state, "final_recommendations": top5}