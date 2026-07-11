import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi.testclient import TestClient
from httpx import AsyncClient
import fakeredis.aioredis
from uuid import uuid4

from app.main import app
from app.db.models import Base, Organization, Project, Queue
from app.db.session import get_db
from app.db.redis import get_redis

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function")
async def db_session():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
        
    # Drop tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def redis_client():
    client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    yield client
    await client.flushall()

@pytest_asyncio.fixture(scope="function")
async def client(db_session, redis_client):
    async def override_get_db():
        yield db_session
        
    async def override_get_redis():
        yield redis_client

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
        
    app.dependency_overrides.clear()

@pytest_asyncio.fixture(scope="function")
async def test_queue(db_session):
    # Setup base entities needed for job tests
    org = Organization(id=uuid4(), name="Test Org")
    db_session.add(org)
    
    project = Project(id=uuid4(), organization_id=org.id, name="Test Project")
    db_session.add(project)
    
    queue = Queue(id=uuid4(), project_id=project.id, name="test-queue", priority="default", concurrency_limit=10)
    db_session.add(queue)
    
    await db_session.commit()
    return queue
