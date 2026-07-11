from pydantic import BaseModel, ConfigDict, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any
import sys

class JobBase(BaseModel):
    payload: Dict[str, Any] = Field(default_factory=dict)
    max_retries: int = Field(3, ge=0)
    scheduled_for: Optional[datetime] = None

    @field_validator('payload')
    @classmethod
    def validate_payload_size(cls, v):
        # Prevent payloads larger than ~10KB to avoid memory exhaustion DoS
        import json
        if len(json.dumps(v)) > 10240:
            raise ValueError("Payload size exceeds maximum allowed limit (10KB)")
        return v

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
