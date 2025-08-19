import logging

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks

from app.dependencies import (
    get_sync_image_generation_workflow,
    get_job_id_handler,
)
from app.models.dto.image_generation_request import (
    ImageGenerationRequest,
    ImageGenerationResponse,
)
from app.services.sync_images_generation_workflow import SyncImagesGenerationWorkflow
from app.utils.job_id_handler import JobIdHandler
from app.worker.tasks import generate_images_main_task

router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)


@router.post("/generate/async/celery")
async def generate_images_async_celery(
    request: ImageGenerationRequest,
    job_id_handler: JobIdHandler = Depends(get_job_id_handler),
):
    try:
        job_id = job_id_handler.generate()

        request_data = {
            "prompt": request.prompt,
            "gallery_count": request.gallery_count,
            "llm_model": request.llm_model.value,
            "image_model": request.image_model.value,
        }

        generate_images_main_task.delay(request_data, job_id)

        return {
            "job_id": job_id,
            "status": "started",
            "message": "Job started with Celery",
        }

    except Exception as e:
        logger.exception("Failed to start Celery job", extra={"error": str(e)})
        raise HTTPException(
            status_code=500, detail=f"Failed to start Celery job: {str(e)}"
        )


@router.post("/generate/async/background-tasks")
async def generate_images_async_background_tasks(
    request: ImageGenerationRequest,
    background_tasks: BackgroundTasks,
    sync_image_generation_orchestrator: SyncImagesGenerationWorkflow = Depends(
        get_sync_image_generation_workflow
    ),
    job_id_handler: JobIdHandler = Depends(get_job_id_handler),
):
    job_id = job_id_handler.generate()
    background_tasks.add_task(
        sync_image_generation_orchestrator.generate_images, request, job_id
    )

    return {
        "job_id": job_id,
        "status": "started",
        "message": "Job started with background task",
    }


@router.post("/generate/sync", response_model=ImageGenerationResponse)
async def generate_images_sync(
    request: ImageGenerationRequest,
    sync_image_generation_orchestrator: SyncImagesGenerationWorkflow = Depends(
        get_sync_image_generation_workflow
    ),
    job_id_handler: JobIdHandler = Depends(get_job_id_handler),
):
    """
    IMPORTANT: This endpoint generates images synchronously.
    This means images are processed sequentially, and the HTTP response is only returned after the whole job complete.
    This approach is not recommended for production environments.
    Use this endpoint exclusively for development, debugging and testing purposes.
    """
    try:
        job_id = job_id_handler.generate()
        response = sync_image_generation_orchestrator.generate_images(request, job_id)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create image generation job: {str(e)}"
        )
