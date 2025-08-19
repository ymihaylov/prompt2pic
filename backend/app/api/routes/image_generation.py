"""
Image generation API routes.
"""

from fastapi import APIRouter, HTTPException

from app.core.prompt_config import ProviderConfig
from app.models.image_generation import ImageGenerationRequest, ImageGenerationResponse
from app.services.workflow_manager import WorkflowManager

# Create router instance
router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)

# Initialize service with simulation mode for development
config = ProviderConfig()
workflow_manager = WorkflowManager(config)


@router.post("/generate/sync", response_model=ImageGenerationResponse)
async def generate_images(request: ImageGenerationRequest):
    try:
        response = workflow_manager.create_generation_job(request)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create image generation job: {str(e)}"
        )


@router.get("/job/{job_id}")
async def get_job_status(job_id: str):
    """
    Get the status of an image generation job.

    - **job_id**: Unique identifier for the generation job
    """
    try:
        status = workflow_manager.get_job_status(job_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Job not found: {str(e)}")
