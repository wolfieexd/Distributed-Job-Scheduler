from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any

class JobBase(BaseModel):
    payload: Dict[str, Any] = Field(default_factory=dict)
    max_retries: int = Field(3, ge=0)
    scheduled_for: Optional[datetime] = None

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: UUID
    queue_id: UUID
    worker_id: Optional[UUID] = None
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    retry_count: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
