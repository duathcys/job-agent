from fastapi import FastAPI
from app.api.v1.router import router

app = FastAPI(
    title="Job Agent API",
    description="취업 준비 AI 에이전트",
    version="0.1.0",
)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}