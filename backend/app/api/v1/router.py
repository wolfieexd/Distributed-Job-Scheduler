from fastapi import APIRouter

from app.api.v1.endpoints import organizations, projects, queues

api_router = APIRouter()

api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(queues.router, prefix="/queues", tags=["Queues"])
