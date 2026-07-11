import sys
import os
import asyncio
import uuid
import json

# Append backend path to import shared models
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.future import select

from app.db.models import Job, WorkerNode
from worker.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def process_job(job_id: str, worker_id: uuid.UUID):
    print(f"[{settings.WORKER_HOSTNAME}] Processing job {job_id}")
    async with AsyncSessionLocal() as db:
        # Mark as processing in Postgres
        result = await db.execute(select(Job).where(Job.id == uuid.UUID(job_id)))
        job = result.scalar_one_or_none()
        
        if not job:
            return
            
        job.status = "processing"
        job.worker_id = worker_id
        await db.commit()
        
        try:
            # Simulate heavy work
            await asyncio.sleep(2)
            
            # Mark as completed
            job.status = "completed"
            job.result = {"status": "success", "message": "Simulated heavy computation"}
        except Exception as e:
            job.retry_count += 1
            if job.retry_count >= job.max_retries:
                job.status = "failed"
                job.error = str(e)
            else:
                job.status = "queued"
                # Requeue logic would go here
        finally:
            await db.commit()

async def worker_loop(queue_id: str, worker_id: uuid.UUID):
    print(f"[{settings.WORKER_HOSTNAME}] Worker started. Listening to queue: {queue_id}")
    
    queue_key = f"titan:queue:{queue_id}:ready"
    
    while True:
        try:
            # BLPOP blocks until a job is available
            result = await redis_client.blpop(queue_key, timeout=10)
            if result:
                _, job_data_str = result
                job_data = json.loads(job_data_str)
                job_id = job_data["job_id"]
                
                # Process the job
                await process_job(job_id, worker_id)
            
        except Exception as e:
            print(f"Worker polling error: {e}")
            await asyncio.sleep(1)

async def main():
    if not settings.QUEUE_ID:
        print("Error: QUEUE_ID environment variable must be set for the worker to know what to poll.")
        return

    # Register worker
    worker_id = uuid.uuid4()
    async with AsyncSessionLocal() as db:
        worker = WorkerNode(id=worker_id, hostname=settings.WORKER_HOSTNAME, status="active")
        db.add(worker)
        await db.commit()
    
    try:
        # In a real app we'd also run a heartbeat asyncio task concurrently here
        await worker_loop(settings.QUEUE_ID, worker_id)
    finally:
        # Mark worker as offline on graceful exit
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(WorkerNode).where(WorkerNode.id == worker_id))
            worker = result.scalar_one_or_none()
            if worker:
                worker.status = "offline"
                await db.commit()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker shutting down...")
