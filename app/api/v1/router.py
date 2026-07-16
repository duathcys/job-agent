from fastapi import APIRouter
from app.api.v1.endpoints import users, jobs

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])