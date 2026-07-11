from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.db.models import User
from app.schemas.user import Token, UserResponse, UserCreate
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.id, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
        
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

from pydantic import BaseModel
from typing import Optional
import secrets
import hashlib
from app.db.models import ApiKey
from app.api.deps import get_admin_user

class ApiKeyCreate(BaseModel):
    name: str
    organization_id: str

@router.post("/api-keys", response_model=None, status_code=201) # response_model=None to avoid exposing ApiKeyResponse if not explicitly imported at top level
async def create_api_key(
    key_in: ApiKeyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    # Generate a cryptographically secure 32-byte string
    raw_key = secrets.token_urlsafe(32)
    # Hash it with SHA-256 before saving to the database
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    
    import uuid
    api_key_record = ApiKey(
        id=uuid.uuid4(),
        key_hash=key_hash,
        name=key_in.name,
        organization_id=uuid.UUID(key_in.organization_id)
    )
    
    db.add(api_key_record)
    await db.commit()
    await db.refresh(api_key_record)
    
    # Return the raw key ONLY ONCE. It is never retrievable again!
    return {
        "id": api_key_record.id,
        "name": api_key_record.name,
        "organization_id": api_key_record.organization_id,
        "raw_key": raw_key # The user MUST save this now!
    }
