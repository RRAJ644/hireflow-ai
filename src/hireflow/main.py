from contextlib import asynccontextmanager

from fastapi import FastAPI

from hireflow.core.config import settings
from hireflow.core.redis import create_redis_pool
from hireflow.db.session import engine
from hireflow.api.v1.health import router as health_router
from hireflow.api.v1.ingestion import router as ingestion_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting HireFlow API...")

    app.state.redis = await create_redis_pool()

    yield

    print("Shutting down HireFlow API...")
    await app.state.redis.aclose()
    await engine.dispose()

app= FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(ingestion_router, prefix="/api/v1")


