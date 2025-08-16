"""
Image generation API routes.
"""
from fastapi import APIRouter, HTTPException
from app.models.image_generation import ImageGenerationRequest, ImageGenerationResponse
from app.services.image_generation_service import ImageGenerationService

# Create router instance
router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)

# Initialize service
image_service = ImageGenerationService()


@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_images(request: ImageGenerationRequest):
    """
    Receive user prompt and gallery count to start image generation process.

    - **prompt**: Text description (max 300 characters)
    - **gallery_count**: Number of gallery images to generate (0-15)
    """
    try:
        response = image_service.create_generation_job(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create image generation job: {str(e)}")


@router.get("/job/{job_id}")
async def get_job_status(job_id: str):
    """
    Get the status of an image generation job.

    - **job_id**: Unique identifier for the generation job
    """
    try:
        status = image_service.get_job_status(job_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Job not found: {str(e)}")