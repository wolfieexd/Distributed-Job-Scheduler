import redis.asyncio as redis
from app.core.config import settings

# Global redis client pool
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_redis():
    try:
        yield redis_client
    finally:
        pass # The connection pool handles closing connections
