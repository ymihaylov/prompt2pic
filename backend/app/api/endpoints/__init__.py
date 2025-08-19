# Routers package

"""
API endpoints package initialization.
"""
from fastapi import APIRouter

from .health import router as health_router
from .home import router as home_router
from .images import router as images_router
from .jobs import router as jobs_router

# Create main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(images_router)
api_router.include_router(jobs_router)
api_router.include_router(health_router)
api_router.include_router(home_router)

# Export for easy import
__all__ = ["api_router"]
