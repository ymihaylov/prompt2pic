"""
Image generation API routes.
"""

from fastapi import APIRouter, HTTPException, Depends

from app.core.dependencies import get_image_generation_orchestrator, get_request_id_service
from app.models.image_generation import ImageGenerationRequest, ImageGenerationResponse
from app.services.image_generation_orchestrator import ImageGenerationOrchestrator
from app.services.request_id_service import RequestIdService

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
        request_id = request_id_service.generate_with_prefix("img")

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
