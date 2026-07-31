from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.job import JobPostingCreate, JobPostingResponse
from app.services import job_service

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