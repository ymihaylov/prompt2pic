import logging

from app.celery_app import celery_app
from app.infrastructure.providers.image.image_provider_type import ImageProviderType
from app.infrastructure.providers.llm.llm_provider_type import LLMProviderType
from app.models.domain.image_task import ImageTask
from app.models.dto.image_generation_request import ImageGenerationRequest
from app.worker.service_container import service_container

logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def generate_images_main_task(self, request_dict: dict, job_id: str):
    """Main task: Setup + coordination, images in parallel"""

    try:
        request = _reconstruct_request(request_dict)

        sc = service_container()

        return sc.async_workflow.start_job(request, job_id)
    except Exception as e:
        logger.exception("generate_images_main_task failed", extra={"job_id": job_id})
        _handle_task_failure(job_id, e)
        return {"status": "failed", "job_id": job_id, "error": str(e)}


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 2},
)
def generate_single_image_task(
    self, task_dict: dict, image_provider_type: str, job_id: str
):
    """Generate single image task"""

    try:
        sc = service_container()
        task = _reconstruct_image_task(task_dict)
        image_provider_type = ImageProviderType(image_provider_type)

        result = sc.async_workflow.process_single_image(
            task, image_provider_type, job_id
        )

        return result

    except Exception as e:
        sc = service_container()
        try:
            image_type = _reconstruct_image_task(task_dict).image_type
        except Exception:
            image_type = task_dict.get("image_type", "unknown")

        sc.image_repository.update_image_failed(job_id, image_type, str(e))

        logger.exception(
            "Image task failed",
            extra={"job_id": job_id, "image_type": image_type, "error": str(e)},
        )
        raise


@celery_app.task(bind=True)
def finalize_generation_task(self, image_results, job_id: str):
    """Finalization task - runs after all images complete"""

    try:
        sc = service_container()

        return sc.async_workflow.finalize_job(job_id)

    except Exception as e:
        _handle_task_failure(job_id, e)
        return {"status": "failed", "job_id": job_id, "error": str(e)}


def _reconstruct_request(request_dict: dict) -> ImageGenerationRequest:
    request_dict["llm_model"] = LLMProviderType(request_dict["llm_model"])
    request_dict["image_model"] = ImageProviderType(request_dict["image_model"])

    return ImageGenerationRequest(**request_dict)


def _reconstruct_image_task(task_dict: dict) -> ImageTask:
    return ImageTask.from_dict(task_dict)


def _handle_task_failure(job_id: str, error: Exception):
    try:
        sc = service_container()
        sc.job_lifecycle_tracker.fail_job(job_id, error)
    except Exception as e:
        logger.exception("Job failed", extra={"job_id": job_id, "error": str(e)})
