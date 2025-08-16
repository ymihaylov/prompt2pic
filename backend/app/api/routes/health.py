"""
Health check endpoints.
"""
from fastapi import APIRouter
from pydantic import BaseModel

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

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="Service is running"
    )


@router.get("/healthz", response_model=HealthResponse)
async def kubernetes_health_check():
    """Kubernetes-style health check endpoint."""
    return HealthResponse(
        status="ok",
        message="Ready"
    )


@router.get("/readyz", response_model=HealthResponse)
async def kubernetes_readiness_check():
    """Kubernetes-style readiness check endpoint."""
    # TODO: Add actual readiness checks (database, GPU, etc.)
    return HealthResponse(
        status="ready",
        message="Service is ready to handle requests"
    )
