from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.job import JobPostingCreate, JobPostingResponse
from app.services import job_service
from app.services.ai_service import summarize_job, calculate_fit_score
from app.schemas.user import UserResponse
from app.services.user_service import get_user

router = APIRouter()


@router.post("/", response_model=JobPostingResponse)
def create_job(
    job_data: JobPostingCreate,
    db: Session = Depends(get_db),
):
    return job_service.create_job(db, job_data)


@router.get("/", response_model=list[JobPostingResponse])
def get_jobs(
    db: Session = Depends(get_db),
):
    return job_service.get_all_jobs(db)


@router.get("/{job_id}", response_model=JobPostingResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    return job_service.get_job(db, job_id)


@router.post("/{job_id}/summarize")
async def summarize(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = job_service.get_job(db, job_id)
    result = await summarize_job(job.description or job.title)
    return result


@router.post("/{job_id}/fit-score")
async def fit_score(
    job_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    job = job_service.get_job(db, job_id)
    user = get_user(db, user_id)
    result = await calculate_fit_score(
        user_skills=user.skills,
        job_required_skills=job.required_skills or [],
        job_preferred_skills=job.preferred_skills or [],
    )
    return result