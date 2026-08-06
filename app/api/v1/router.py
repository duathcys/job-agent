from fastapi import APIRouter
from app.api.v1.endpoints import users, jobs, auth, agent, resume, portfolio

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
router.include_router(agent.router, prefix="/agent", tags=["agent"])
router.include_router(resume.router, prefix="/resume", tags=["resume"])
router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])