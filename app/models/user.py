from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    job = Column(String, nullable=False)           # 희망 직무 (백엔드)
    location = Column(String, nullable=False)       # 지역 (서울)
    career = Column(String, nullable=False)         # 경력 (신입)
    skills = Column(JSON, nullable=False)           # ["Java", "Spring", "MySQL"]
    interests = Column(JSON, nullable=True)         # ["네이버", "카카오"]
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())