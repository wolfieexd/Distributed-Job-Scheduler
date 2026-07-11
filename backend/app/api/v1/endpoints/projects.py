from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.db.session import get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project_service import ProjectService
from app.services.organization_service import OrganizationService
from app.api.deps import get_admin_user

router = APIRouter(dependencies=[Depends(get_admin_user)])

@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    # Verify organization exists
    org = await OrganizationService.get_organization(db, project_in.organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
        
    return await ProjectService.create_project(db, project_in)

@router.get("/organization/{org_id}", response_model=List[ProjectResponse])
async def read_projects_by_org(
    org_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await ProjectService.get_projects_by_org(db, org_id, skip=skip, limit=limit)
