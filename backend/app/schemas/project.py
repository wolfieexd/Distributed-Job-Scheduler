from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    name: str

class ProjectCreate(ProjectBase):
    organization_id: UUID

class ProjectResponse(ProjectBase):
    id: UUID
    organization_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
