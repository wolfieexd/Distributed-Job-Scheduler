from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from redis.asyncio import Redis
import uuid
import json
from datetime import timezone, datetime

from app.db.models import Job, Queue, JobEvent
from app.schemas.job import JobCreate
from app.core.logging import setup_logging

logger = setup_logging()

class JobService:
    @staticmethod
    async def create_job(db: AsyncSession, redis_client: Redis, queue_id: uuid.UUID, job_in: JobCreate) -> Job:
        logger.info("creating_job", queue_id=str(queue_id))
        # 1. Verify queue exists
        queue = await db.execute(select(Queue).where(Queue.id == queue_id))
        if not queue.scalar_one_or_none():
            logger.error("queue_not_found", queue_id=str(queue_id))
            raise HTTPException(status_code=404, detail="Queue not found")

        from app.core.logging import trace_id_var
        current_trace_id = trace_id_var.get()
        
        # 2. Dual Write: Save to Postgres FIRST (Source of truth)
        db_job = Job(
            queue_id=queue_id,
            payload=job_in.payload,
            max_retries=job_in.max_retries,
            scheduled_for=job_in.scheduled_for,
            status="queued",
            trace_id=current_trace_id
        )
        db.add(db_job)
        await db.flush()
        
        # Add Audit Event
        job_event = JobEvent(
            job_id=db_job.id, 
            previous_status=None,
            new_status="queued",
            message="Job initially enqueued"
        )
        db.add(job_event)
        
        await db.commit()
        await db.refresh(db_job)

        # 3. Dual Write: Push to Redis
        job_data = json.dumps({
            "job_id": str(db_job.id),
            "trace_id": current_trace_id
        })
        
        try:
            if db_job.scheduled_for:
                # Add to Scheduled Sorted Set (score is timestamp)
                score = db_job.scheduled_for.replace(tzinfo=timezone.utc).timestamp()
                await redis_client.zadd(f"titan:queue:{queue_id}:scheduled", {job_data: score})
            else:
                # Add to Immediate List (FIFO)
                await redis_client.rpush(f"titan:queue:{queue_id}:ready", job_data)
        except Exception as e:
            # If Redis fails, the Sweeper service will eventually see this 'queued' job in Postgres
            # and push it to Redis later. This guarantees we don't lose jobs.
            pass

        return db_job

    @staticmethod
    async def get_job(db: AsyncSession, job_id: uuid.UUID) -> Job | None:
        result = await db.execute(select(Job).where(Job.id == job_id))
        return result.scalar_one_or_none()
