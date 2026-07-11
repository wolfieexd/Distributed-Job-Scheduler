import os
from pydantic_settings import BaseSettings

class WorkerSettings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://admin:password123@localhost:5432/titan_db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    WORKER_HOSTNAME: str = os.getenv("HOSTNAME", "local-worker")
    QUEUE_ID: str = os.getenv("QUEUE_ID", "")  # Which queue this worker listens to

settings = WorkerSettings()
