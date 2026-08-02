from pydantic import BaseModel, ConfigDict
from typing import Optional


class JobPostingCreate(BaseModel):
    company: str
    title: str
    description: Optional[str] = None
    required_skills: Optional[list[str]] = None
    preferred_skills: Optional[list[str]] = None
    location: Optional[str] = None
    career: Optional[str] = None
    deadline: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = None


class JobPostingResponse(BaseModel):
    id: int
    company: str
    title: str
    required_skills: Optional[list[str]] = None
    preferred_skills: Optional[list[str]] = None
    location: Optional[str] = None
    career: Optional[str] = None
    deadline: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = None
    summary: Optional[str] = None
    fit_score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)