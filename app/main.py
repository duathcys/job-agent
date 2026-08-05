from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router
from app.db.session import create_tables
from app.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()


app = FastAPI(
    title="Job Agent API",
    description="취업 준비 AI 에이전트",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}