from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func

from app.db.session import Base


class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    required_skills = Column(Text, nullable=True)    # 텍스트로 변경
    preferred_skills = Column(Text, nullable=True)   # 텍스트로 변경
    location = Column(String, nullable=True)
    career = Column(String, nullable=True)
    deadline = Column(String, nullable=True)
    url = Column(String, nullable=True)
    source = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    fit_score = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())