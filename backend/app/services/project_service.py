from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Project
from app.schemas.project import ProjectCreate
import uuid

class ProjectService:
    @staticmethod
    async def create_project(db: AsyncSession, proj_in: ProjectCreate) -> Project:
        db_proj = Project(organization_id=proj_in.organization_id, name=proj_in.name)
        db.add(db_proj)
        await db.commit()
        await db.refresh(db_proj)
        return db_proj

    @staticmethod
    async def get_projects_by_org(db: AsyncSession, org_id: uuid.UUID, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(Project).where(Project.organization_id == org_id).offset(skip).limit(limit)
        )
        return result.scalars().all()
