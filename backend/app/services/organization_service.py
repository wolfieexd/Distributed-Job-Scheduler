from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Organization
from app.schemas.organization import OrganizationCreate
import uuid

class OrganizationService:
    @staticmethod
    async def create_organization(db: AsyncSession, org_in: OrganizationCreate) -> Organization:
        db_org = Organization(name=org_in.name)
        db.add(db_org)
        await db.commit()
        await db.refresh(db_org)
        return db_org

    @staticmethod
    async def get_organizations(db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(Organization).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def get_organization(db: AsyncSession, org_id: uuid.UUID) -> Organization | None:
        result = await db.execute(select(Organization).where(Organization.id == org_id))
        return result.scalar_one_or_none()
