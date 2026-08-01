import asyncio
from agent.state import AgentState
from app.services.ai_service import calculate_fit_score
from app.db.session import SessionLocal
from app.models.job import JobPosting


def score_node(state: AgentState) -> AgentState:
    """
    사용자 스킬과 공고를 비교해 적합도를 계산합니다.
    """
    print("🎯 [3/4] 적합도 계산 중...")
    try:
        db = SessionLocal()
        scored = []

        for item in state["summarized_jobs"]:
            job = db.query(JobPosting).filter(JobPosting.id == item["job_id"]).first()
            if not job:
                continue

            result = asyncio.run(calculate_fit_score(
                user_skills=state["user_skills"],
                job_required_skills=job.required_skills or [],
                job_preferred_skills=job.preferred_skills or [],
            ))

            job.fit_score = result.get("fit_score", 0)
            scored.append({
                "job_id": item["job_id"],
                "company": job.company,
                "title": job.title,
                "summary": item["summary"],
                "fit_score": result.get("fit_score", 0),
                "matched_skills": result.get("matched_skills", []),
                "missing_skills": result.get("missing_skills", []),
                "comment": result.get("comment", ""),
                "url": job.url,
                "deadline": job.deadline,
            })

        db.commit()
        db.close()

        print(f"✅ {len(scored)}개 공고 적합도 계산 완료")
        return {**state, "scored_jobs": scored}

    except Exception as e:
        db.rollback()
        db.close()
        return {**state, "error": str(e)}