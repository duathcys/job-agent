from sqlalchemy import Column, Integer, String, JSON, DateTime, Float
from sqlalchemy.sql import func

from app.db.session import Base


class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)         # 회사명
    title = Column(String, nullable=False)           # 공고 제목
    description = Column(String, nullable=True)      # 공고 원문
    required_skills = Column(JSON, nullable=True)    # ["Java", "Spring"]
    preferred_skills = Column(JSON, nullable=True)   # ["Docker", "AWS"]
    location = Column(String, nullable=True)         # 지역
    career = Column(String, nullable=True)           # 신입/경력
    deadline = Column(String, nullable=True)         # 마감일
    url = Column(String, nullable=True)              # 공고 URL
    source = Column(String, nullable=True)           # 출처 (원티드, 사람인)
    summary = Column(String, nullable=True)          # AI 요약
    fit_score = Column(Float, nullable=True)         # 적합도 점수
    created_at = Column(DateTime, server_default=func.now())