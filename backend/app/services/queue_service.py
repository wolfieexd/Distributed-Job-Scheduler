from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.db.models import Queue
from app.schemas.queue import QueueCreate
import uuid

class QueueService:
    @staticmethod
    async def create_queue(db: AsyncSession, queue_in: QueueCreate) -> Queue:
        db_queue = Queue(
            project_id=queue_in.project_id,
            name=queue_in.name,
            concurrency_limit=queue_in.concurrency_limit,
            priority=queue_in.priority
        )
        db.add(db_queue)
        try:
            await db.commit()
            await db.refresh(db_queue)
            return db_queue
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Queue with this name already exists in the project")

    @staticmethod
    async def get_queues_by_project(db: AsyncSession, project_id: uuid.UUID, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(Queue).where(Queue.project_id == project_id).offset(skip).limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_queue(db: AsyncSession, queue_id: uuid.UUID) -> Queue | None:
        result = await db.execute(select(Queue).where(Queue.id == queue_id))
        return result.scalar_one_or_none()
