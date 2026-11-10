import httpx

from hireflow.workers.ingestion import run_ingestion
from arq.connections import RedisSettings
from hireflow.core.config import settings



async def startup(ctx: dict) -> None:
    ctx["http_client"] = httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
        limits=httpx.Limits(
            max_connections=20,
            max_keepalive_connections=10,
        ),
    )


async def shutdown(ctx: dict) -> None:
    await ctx["http_client"].aclose()


class WorkerSettings:
    functions = [run_ingestion]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)

    on_startup = startup
    on_shutdown = shutdown

    max_jobs = 5
    job_timeout = 3600
    max_tries = 3

    