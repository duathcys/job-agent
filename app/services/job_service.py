from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories import job_repo
from app.schemas.job import JobPostingCreate
from app.models.job import JobPosting


def create_job(db: Session, job_data: JobPostingCreate) -> JobPosting:
    return job_repo.create_job(db, job_data)


def get_all_jobs(db: Session) -> list[JobPosting]:
    return job_repo.get_all_jobs(db)


def get_job(db: Session, job_id: int) -> JobPosting:
    job = job_repo.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="공고를 찾을 수 없습니다.")
    return job