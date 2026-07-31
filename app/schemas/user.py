from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    job: str
    location: str
    career: str
    skills: list[str]
    interests: Optional[list[str]] = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    job: str
    location: str
    career: str
    skills: list[str]
    interests: Optional[list[str]] = None

    class Config:
        from_attributes = True