"""
Image generation API routes.
"""

import secrets
import uuid

from fastapi import APIRouter, HTTPException, Depends

from app.core.dependencies import get_image_generation_orchestrator
from app.models.image_generation import ImageGenerationRequest, ImageGenerationResponse
from app.services.image_generation_orchestrator import ImageGenerationOrchestrator

# Create router instance
router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)


@router.post("/generate/sync", response_model=ImageGenerationResponse)
async def generate_images_sync(
    request: ImageGenerationRequest,
    image_generation_orchestrator: ImageGenerationOrchestrator = Depends(
        get_image_generation_orchestrator
    ),
):
    try:
        # Generate cryptographically secure request ID
        request_id = secrets.token_urlsafe(12)  # 16 chars, secure & URL-safe

        response = image_generation_orchestrator.generate_images(request, request_id)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create image generation job: {str(e)}"
        )


@router.get("/job/{job_id}")
async def get_job_status(
    job_id: str,
    image_generation_orchestrator: ImageGenerationOrchestrator = Depends(
        get_image_generation_orchestrator
    ),
):
    try:
        status = image_generation_orchestrator.get_job_status(job_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Job not found: {str(e)}")
