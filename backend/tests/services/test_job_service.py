import pytest
from uuid import uuid4
import json
from sqlalchemy.future import select

from app.services.job_service import JobService
from app.schemas.job import JobCreate
from app.db.models import Job, JobEvent

@pytest.mark.asyncio
async def test_job_dual_write_success(db_session, redis_client, test_queue):
    """
    Advanced Test: Verifies the Dual-Write mechanism.
    When a job is created, it should:
    1. Be inserted into Postgres with status 'queued'
    2. Have an audit trail JobEvent created
    3. Be pushed onto the Redis list 'titan:queue:{queue_id}:ready'
    """
    job_payload = {"task": "process_video", "video_id": 12345}
    job_in = JobCreate(payload=job_payload, max_retries=3)
    
    # Execute JobService
    db_job = await JobService.create_job(db_session, redis_client, test_queue.id, job_in)
    
    # 1. Verify Postgres State
    assert db_job.id is not None
    assert db_job.status == "queued"
    assert db_job.queue_id == test_queue.id
    
    # 2. Verify Audit Trail (JobEvent)
    result = await db_session.execute(select(JobEvent).where(JobEvent.job_id == db_job.id))
    events = result.scalars().all()
    assert len(events) == 1
    assert events[0].new_status == "queued"
    
    # 3. Verify Redis State (Dual-Write)
    redis_key = f"titan:queue:{test_queue.id}:ready"
    queue_len = await redis_client.llen(redis_key)
    assert queue_len == 1
    
    redis_data_str = await redis_client.lpop(redis_key)
    redis_data = json.loads(redis_data_str)
    assert redis_data["job_id"] == str(db_job.id)

@pytest.mark.asyncio
async def test_job_service_queue_not_found(db_session, redis_client):
    """
    Ensure creating a job on a non-existent queue raises 404
    """
    job_in = JobCreate(payload={}, max_retries=3)
    from fastapi import HTTPException
    
    with pytest.raises(HTTPException) as excinfo:
        await JobService.create_job(db_session, redis_client, uuid4(), job_in)
        
    assert excinfo.value.status_code == 404
