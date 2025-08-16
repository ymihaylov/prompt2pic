# Routers package

"""
API routes package initialization.
"""
from fastapi import APIRouter
from .health import router as health_router
from .image_generation import router as images_router

# Create main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(health_router)
api_router.include_router(images_router)

# Export for easy import
__all__ = ["api_router"]