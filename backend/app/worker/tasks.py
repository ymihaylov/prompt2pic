"""
Celery tasks for image generation
"""
import logging
from typing import Dict, Any

from app.celery_app import celery_app
from app.models.image_generation import ImageGenerationRequest
from app.core.interfaces import LLMProviderType, ImageProviderType
from app.worker.service_factory import WorkerServiceFactory
from app.worker.exceptions import TaskValidationError, ImageGenerationTaskError

logger = logging.getLogger(__name__)


@celery_app.task(
    name="image_generation.generate_images",
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 3, 'countdown': 60},
    retry_backoff=True,
    retry_jitter=True
)
def generate_images_task(self, request_dict: Dict[str, Any], job_id: str) -> Dict[str, Any]:
    """
    Generate images based on user request
    
    Args:
        self: Celery task instance (bound)
        request_dict: Serialized image generation request
        job_id: Unique job identifier
        
    Returns:
        Dict containing task result status and job_id
        
    Raises:
        TaskValidationError: If input validation fails
        ImageGenerationTaskError: If image generation fails
    """
    logger.info(f"Starting image generation task for job {job_id}")
    
    try:
        # Validate and convert request
        request = _validate_and_convert_request(request_dict)
        logger.info(f"Request validated for job {job_id}: {request.prompt[:50]}...")
        
        # Get orchestrator
        orchestrator = WorkerServiceFactory.create_image_generation_orchestrator()
        
        # Generate images
        logger.info(f"Starting image generation for job {job_id}")
        orchestrator.generate_images(request, job_id)
        
        logger.info(f"Image generation completed successfully for job {job_id}")
        return {
            "status": "completed",
            "job_id": job_id,
            "task_id": self.request.id
        }
        
    except TaskValidationError as e:
        logger.error(f"Validation failed for job {job_id}: {e}")
        return {
            "status": "failed",
            "job_id": job_id,
            "error": f"Validation error: {str(e)}",
            "error_type": "validation"
        }
        
    except Exception as e:
        logger.error(f"Image generation failed for job {job_id}: {e}")
        # Re-raise for Celery retry mechanism
        raise ImageGenerationTaskError(f"Image generation failed: {str(e)}")


def _validate_and_convert_request(request_dict: Dict[str, Any]) -> ImageGenerationRequest:
    """
    Validate and convert request dictionary to ImageGenerationRequest
    
    Args:
        request_dict: Raw request dictionary
        
    Returns:
        ImageGenerationRequest: Validated request object
        
    Raises:
        TaskValidationError: If validation fails
    """
    try:
        # Convert string enum values back to enums
        if "llm_model" in request_dict:
            request_dict["llm_model"] = LLMProviderType(request_dict["llm_model"])
        if "image_model" in request_dict:
            request_dict["image_model"] = ImageProviderType(request_dict["image_model"])
        
        # Convert dict back to request object
        request = ImageGenerationRequest(**request_dict)
        return request
        
    except (ValueError, TypeError) as e:
        raise TaskValidationError(f"Invalid request format: {str(e)}")
