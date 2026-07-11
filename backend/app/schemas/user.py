from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class UserBase(BaseModel):
    email: str
    role: str = "developer"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class ApiKeyResponse(BaseModel):
    id: UUID
    raw_key: str
    name: str
    organization_id: UUID
    model_config = ConfigDict(from_attributes=True)
