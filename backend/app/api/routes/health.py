"""
Health check endpoints.
"""

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel

from app.core.dependencies import get_redis_service
from app.services.redis_service import RedisService

router = APIRouter(
    tags=["health"],
)


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    message: str


class HelloResponse(BaseModel):
    message: str


@router.get("/", response_model=HelloResponse)
async def read_root():
    """Basic hello world endpoint."""
    return HelloResponse(message="Hello World")


@router.get("/health")
async def health_check(redis_service: RedisService = Depends(get_redis_service)):
    """Health check endpoint"""
    return {
        "redis": redis_service.health_check(),
        "status": "healthy" if redis_service.health_check() else "unhealthy",
    }


@router.get("/healthz", response_model=HealthResponse)
async def kubernetes_health_check():
    """Kubernetes-style health check endpoint."""
    return HealthResponse(status="ok", message="Ready")


@router.get("/readyz", response_model=HealthResponse)
async def kubernetes_readiness_check():
    """Kubernetes-style readiness check endpoint."""
    # TODO: Add actual readiness checks (database, GPU, etc.)
    return HealthResponse(status="ready", message="Service is ready to handle requests")
