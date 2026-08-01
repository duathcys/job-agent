from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.router import router
from app.db.session import create_tables
from app.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시
    create_tables()
    scheduler = start_scheduler()
    yield
    # 서버 종료 시
    scheduler.shutdown()


app = FastAPI(
    title="Job Agent API",
    description="취업 준비 AI 에이전트",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}