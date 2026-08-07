from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional


class ProjectInput(BaseModel):
    name: str
    description: str = ""
    skills: list[str] = []
    github: str = ""
    deploy_url: str = ""
    period: str = ""


class ExperienceInput(BaseModel):
    company: str
    role: str
    period: str
    description: str = ""


class EducationInput(BaseModel):
    school: str
    major: str
    graduation: str


class PortfolioInput(BaseModel):
    name: str = ""
    job: str = ""
    email: str = ""
    phone: str = ""
    github: str = ""
    intro: str = ""
    skills: list[str] = []
    projects: list[ProjectInput] = []
    experiences: list[ExperienceInput] = []
    education: Optional[EducationInput] = None


class PortfolioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    share_token: Optional[str] = None
    created_at: str