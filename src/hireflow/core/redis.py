from arq.connections import RedisSettings, create_pool
from hireflow.core.config import settings

def get_redis_settings() -> RedisSettings:
    return RedisSettings.from_dsn(settings.REDIS_URL)

async def create_redis_pool():
    redis_settings = get_redis_settings()
    return await create_pool(redis_settings)
