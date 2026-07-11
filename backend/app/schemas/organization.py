from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
