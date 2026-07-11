from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.db.session import get_db
from app.schemas.queue import QueueCreate, QueueResponse
from app.services.queue_service import QueueService

router = APIRouter()

@router.post("/", response_model=QueueResponse, status_code=201)
async def create_queue(
    queue_in: QueueCreate,
    db: AsyncSession = Depends(get_db)
):
    return await QueueService.create_queue(db, queue_in)

@router.get("/project/{project_id}", response_model=List[QueueResponse])
async def read_queues_by_project(
    project_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await QueueService.get_queues_by_project(db, project_id, skip=skip, limit=limit)

@router.get("/{queue_id}", response_model=QueueResponse)
async def read_queue(
    queue_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    queue = await QueueService.get_queue(db, queue_id)
    if not queue:
        raise HTTPException(status_code=404, detail="Queue not found")
    return queue
