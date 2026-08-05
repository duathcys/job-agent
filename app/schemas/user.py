from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    job: str
    location: str
    career: str
    skills: list[str]
    interests: Optional[list[str]] = None


class UserUpdate(BaseModel):
    job: Optional[str] = None
    location: Optional[str] = None
    career: Optional[str] = None
    skills: Optional[list[str]] = None
    interests: Optional[list[str]] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    job: str
    location: str
    career: str
    skills: list[str]
    interests: Optional[list[str]] = None