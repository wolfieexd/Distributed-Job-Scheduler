from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class QueueBase(BaseModel):
    name: str = Field(..., max_length=255)
    concurrency_limit: Optional[int] = Field(None, ge=1)
    priority: int = Field(1, ge=1, le=10)

class QueueCreate(QueueBase):
    project_id: UUID

class QueueResponse(QueueBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
