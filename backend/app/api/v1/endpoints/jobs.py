from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
import uuid

from app.db.session import get_db
from app.db.redis import get_redis
from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import JobService

router = APIRouter()

@router.post("/queues/{queue_id}/jobs", response_model=JobResponse, status_code=201)
async def submit_job(
    queue_id: uuid.UUID,
    job_in: JobCreate,
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis)
):
    return await JobService.create_job(db, redis_client, queue_id, job_in)

@router.get("/jobs/{job_id}", response_model=JobResponse)
async def read_job(
    job_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    job = await JobService.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
