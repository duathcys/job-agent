import asyncio
from agent.state import AgentState
from app.services.ai_service import summarize_job
from app.db.session import SessionLocal
from app.models.job import JobPosting


def summarize_node(state: AgentState) -> AgentState:
    """
    수집된 공고를 AI로 요약합니다.
    """
    print("[2/4] 공고 요약 중...")
    try:
        db = SessionLocal()
        summarized = []

        for job_id in state["saved_job_ids"]:
            job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
            if not job:
                continue

            summary = asyncio.run(summarize_job(job.description or job.title))

            job.summary = summary.get("one_line_summary", "")
            summarized.append({
                "job_id": job_id,
                "company": job.company,
                "title": job.title,
                "summary": summary,
            })

        db.commit()
        db.close()

        print(f"✅ {len(summarized)}개 공고 요약 완료")
        return {**state, "summarized_jobs": summarized}

    except Exception as e:
        db.rollback()
        db.close()
        return {**state, "error": str(e)}