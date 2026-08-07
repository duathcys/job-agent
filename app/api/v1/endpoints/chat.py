from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/")
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """
    AI Agent와 채팅합니다.
    """
    from agent.react_agent import run_react_agent

    response = run_react_agent(
        user_id=current_user.id,
        user_skills=current_user.skills,
        message=request.message,
    )
    return {"response": response}