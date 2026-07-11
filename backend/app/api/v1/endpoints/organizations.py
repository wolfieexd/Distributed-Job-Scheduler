from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.db.session import get_db
from app.schemas.organization import OrganizationCreate, OrganizationResponse
from app.services.organization_service import OrganizationService

router = APIRouter()

@router.post("/", response_model=OrganizationResponse, status_code=201)
async def create_organization(
    org_in: OrganizationCreate,
    db: AsyncSession = Depends(get_db)
):
    return await OrganizationService.create_organization(db, org_in)

@router.get("/", response_model=List[OrganizationResponse])
async def read_organizations(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await OrganizationService.get_organizations(db, skip=skip, limit=limit)

@router.get("/{org_id}", response_model=OrganizationResponse)
async def read_organization(
    org_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    org = await OrganizationService.get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org
