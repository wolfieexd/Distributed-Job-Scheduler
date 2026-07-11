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
import uuid
from app.core.logging import trace_id_var

@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    # Extract trace ID from header or generate a new one
    trace_id = request.headers.get("X-Trace-Id", str(uuid.uuid4()))
    
    # Bind to contextvar so structlog automatically picks it up
    token = trace_id_var.set(trace_id)
    
    response = await call_next(request)
    
    # Inject security headers and trace_id into response
    response.headers["X-Trace-Id"] = trace_id
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    # Reset contextvar to prevent bleeding across requests (though ASGI isolates them)
    trace_id_var.reset(token)
    
    return response

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "titan-api"}

from app.api.v1.router import api_router

app.include_router(api_router, prefix=settings.API_V1_STR)
