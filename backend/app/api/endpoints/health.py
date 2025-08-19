import logging

import httpx
from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel

from app.core.settings import settings
from app.dependencies import get_redis_service
from app.infrastructure.storage.redis_service import RedisService

router = APIRouter(
    tags=["health"],
)


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    message: str


logger = logging.getLogger(__name__)


@router.get("/health")
async def health_check(redis_service: RedisService = Depends(get_redis_service)):
    """Health check endpoint"""
    redis_ok = redis_service.health_check()

    ollama_ok = False
    try:
        with httpx.Client(timeout=2.0) as client:
            # Simple ping via tags endpoint (lightweight). Alternative: /api/tags or /api/version
            r = client.get(f"{settings.ollama_llm_base_url}/api/tags")
            r.raise_for_status()
            ollama_ok = True
    except Exception:
        logger.info(
            "Ollama health check failed",
            extra={"base_url": settings.ollama_llm_base_url},
        )
        ollama_ok = False

    overall = redis_ok and ollama_ok

    return {
        "redis": redis_ok,
        "ollama": ollama_ok,
        "status": "healthy" if overall else "unhealthy",
    }
