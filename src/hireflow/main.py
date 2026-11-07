from contextlib import asynccontextmanager
from fastapi import FastAPI
from hireflow.core.config import settings
from hireflow.db.session import engine
from hireflow.api.v1.health import router as health_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting HireFlow API...")

    yield

    print("Shutting down HireFlow API...")
    await engine.dispose()

app= FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)

app.include_router(health_router, prefix="/api/v1")


