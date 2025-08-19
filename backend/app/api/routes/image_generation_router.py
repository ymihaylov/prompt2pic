"""
Image generation API routes.
"""

from fastapi import APIRouter, HTTPException, Depends

from app.core.dependencies import get_workflow_manager
from app.models.image_generation import ImageGenerationRequest, ImageGenerationResponse
from app.services.workflow_manager import WorkflowManager

# Create router instance
router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)


@router.post("/generate/sync", response_model=ImageGenerationResponse)
async def generate_images_sync(
    request: ImageGenerationRequest,
    workflow_manager: WorkflowManager = Depends(get_workflow_manager),
):
    try:
        response = workflow_manager.generate_images(request)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create image generation job: {str(e)}"
        )


@router.get("/job/{job_id}")
async def get_job_status(
    job_id: str, workflow_manager: WorkflowManager = Depends(get_workflow_manager)
):
    """
    Get the status of an image generation job.

    - **job_id**: Unique identifier for the generation job
    """
    try:
        status = workflow_manager.get_job_status(job_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Job not found: {str(e)}")
