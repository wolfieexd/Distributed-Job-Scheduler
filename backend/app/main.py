from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Advanced Distributed Job Scheduling & Execution Platform API",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Strict CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://yourapp.com"], # Strict origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Security Headers Middleware
from fastapi import Request
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "titan-api"}

from app.api.v1.router import api_router

app.include_router(api_router, prefix=settings.API_V1_STR)
