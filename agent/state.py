from typing import TypedDict, Optional


class AgentState(TypedDict):
    """
    Agent가 각 노드를 거치며 공유하는 상태값입니다.
    """
    user_id: int
    user_skills: list[str]
    raw_jobs: list[dict]          # 크롤링한 원본 공고
    saved_job_ids: list[int]      # DB에 저장된 공고 ID
    summarized_jobs: list[dict]   # AI 요약된 공고
    scored_jobs: list[dict]       # 적합도 계산된 공고
    final_recommendations: list[dict]  # 최종 추천 목록
    error: Optional[str]