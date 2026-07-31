from sqlalchemy.orm import Session

from app.models.job import JobPosting
from app.schemas.job import JobPostingCreate


def create_job(db: Session, job_data: JobPostingCreate) -> JobPosting:
    job = JobPosting(
        company=job_data.company,
        title=job_data.title,
        description=job_data.description,
        required_skills=job_data.required_skills,
        preferred_skills=job_data.preferred_skills,
        location=job_data.location,
        career=job_data.career,
        deadline=job_data.deadline,
        url=job_data.url,
        source=job_data.source,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_all_jobs(db: Session) -> list[JobPosting]:
    return db.query(JobPosting).all()


def get_job_by_id(db: Session, job_id: int) -> JobPosting | None:
    return db.query(JobPosting).filter(JobPosting.id == job_id).first()