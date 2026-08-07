from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False, default="내 포트폴리오")
    data = Column(JSON, nullable=False)       # 포트폴리오 전체 데이터
    html = Column(String, nullable=True)      # 생성된 HTML
    share_token = Column(String, nullable=True, unique=True)  # 공유 링크용
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())