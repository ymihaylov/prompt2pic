"""
Image generation API routes.
"""

from fastapi import APIRouter, HTTPException, Depends

from app.core.dependencies import (
    get_image_generation_orchestrator,
    get_request_id_service,
    get_job_status_service,
)
from app.models.image_generation import ImageGenerationRequest, ImageGenerationResponse
from app.services.image_generation_orchestrator import ImageGenerationOrchestrator
from app.services.request_id_service import RequestIdService
from app.services.job_status_service import JobStatusService

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
    request_id_service: RequestIdService = Depends(get_request_id_service),
):
    try:
        # Generate secure request ID using injected service
        request_id = request_id_service.generate()

        response = image_generation_orchestrator.generate_images(request, request_id)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create image generation job: {str(e)}"
        )


@router.get("/status/{request_id}")
async def get_job_status(
    request_id: str,
    status_service: JobStatusService = Depends(get_job_status_service),
):
    """Get real-time job status and progress."""
    try:
        status = status_service.get_job_dict(request_id)
        if "error" in status:
            raise HTTPException(status_code=404, detail=status["error"])
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")
