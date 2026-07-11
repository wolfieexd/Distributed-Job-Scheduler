from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from redis.asyncio import Redis

from app.db.session import get_db
from app.db.redis import get_redis
from app.core.logging import setup_logging

logger = setup_logging()
router = APIRouter()

@router.get("/")
async def health_check(
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis)
):
    status = {"api": "ok", "db": "unknown", "redis": "unknown"}
    
    # Check Postgres
    try:
        await db.execute(text("SELECT 1"))
        status["db"] = "ok"
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        status["db"] = "failed"
        
    # Check Redis
    try:
        await redis_client.ping()
        status["redis"] = "ok"
    except Exception as e:
        logger.error("Redis health check failed", error=str(e))
        status["redis"] = "failed"
        
    if status["db"] == "failed" or status["redis"] == "failed":
        logger.error("Health probe failed", status=status)
        raise HTTPException(status_code=503, detail=status)
        
    logger.info("Health check passed", status=status)
    return status
