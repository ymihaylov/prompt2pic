"""
Image generation API routes.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks

from app.core.dependencies import (
    get_image_generation_orchestrator,
    get_job_id_service,
)
from app.models.image_generation import ImageGenerationRequest, ImageGenerationResponse
from app.services.image_generation_orchestrator import ImageGenerationOrchestrator
from app.services.job_id_service import JobIdService
from app.worker.tasks import generate_images_task

# Create router instance
router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)


@router.post("/generate/async/background-tasks")
async def generate_images_async_background_tasks(
    request: ImageGenerationRequest,
    background_tasks: BackgroundTasks,
    image_generation_orchestrator: ImageGenerationOrchestrator = Depends(
        get_image_generation_orchestrator
    ),
    job_id_service: JobIdService = Depends(get_job_id_service),
):
    job_id = job_id_service.generate()
    background_tasks.add_task(
        image_generation_orchestrator.generate_images, request, job_id
    )

    return {"job_id": job_id, "status": "processing"}


@router.post("/generate/sync", response_model=ImageGenerationResponse)
async def generate_images_sync(
    request: ImageGenerationRequest,
    image_generation_orchestrator: ImageGenerationOrchestrator = Depends(
        get_image_generation_orchestrator
    ),
    job_id_service: JobIdService = Depends(get_job_id_service),
):
    try:
        # TODO: IS THIS THE BEST PLACE FOR THIS
        job_id = job_id_service.generate()
        print(job_id)

        response = image_generation_orchestrator.generate_images(request, job_id)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create image generation job: {str(e)}"
        )


@router.post("/generate/async/celery")
async def generate_images_async_celery(
    request: ImageGenerationRequest,
    job_id_service: JobIdService = Depends(get_job_id_service),
):
    """Start image generation with Celery and return job_id immediately"""
    try:
        job_id = job_id_service.generate()
        print(f"Starting Celery job: {job_id}")

        # Start Celery task - serialize enums to strings
        request_data = {
            "prompt": request.prompt,
            "gallery_count": request.gallery_count,
            "llm_model": request.llm_model.value,
            "image_model": request.image_model.value,
        }
        generate_images_task.delay(request_data, job_id)

        return {
            "job_id": job_id,
            "status": "started",
            "message": "Job started with Celery",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to start Celery job: {str(e)}"
        )
