from app.celery_app import celery_app
from app.models.image_generation import ImageGenerationRequest
from app.core.interfaces import LLMProviderType, ImageProviderType
from app.services.image_generation_orchestrator import ImageGenerationOrchestrator
from app.services.prompt_template_service import PromptTemplateService
from app.core.factories import LLMProviderFactory, ImageProviderFactory
from app.services.file_manager_service import FileManagerService
from app.services.image_generator_service import ImageGeneratorService
from app.services.job_status_service import JobStatusService
from app.services.progress_calculator import ProgressCalculator
from app.services.image_processing_pipeline import ImageProcessingPipeline
from app.services.redis_service import RedisService

@celery_app.task
def generate_images_task(request_dict: dict, job_id: str):
    """Celery task to generate images"""
    try:
        # Convert string enum values back to enums
        request_dict["llm_model"] = LLMProviderType(request_dict["llm_model"])
        request_dict["image_model"] = ImageProviderType(request_dict["image_model"])
        
        # Convert dict back to request object
        request = ImageGenerationRequest(**request_dict)
        
        # Manually create orchestrator (no dependency injection in Celery)
        prompt_service = PromptTemplateService()
        llm_factory = LLMProviderFactory()
        image_factory = ImageProviderFactory()
        file_manager = FileManagerService()
        image_generator = ImageGeneratorService()
        from app.worker.config import REDIS_URL
        redis_service = RedisService(REDIS_URL)
        status_service = JobStatusService(redis_service)
        progress_calculator = ProgressCalculator()
        image_pipeline = ImageProcessingPipeline(image_generator, file_manager)
        
        orchestrator = ImageGenerationOrchestrator(
            prompt_service=prompt_service,
            llm_factory=llm_factory,
            image_factory=image_factory,
            file_manager=file_manager,
            image_generator=image_generator,
            status_service=status_service,
            progress_calculator=progress_calculator,
            image_pipeline=image_pipeline,
        )
        
        # Generate images
        orchestrator.generate_images(request, job_id)
        
        return {"status": "completed", "job_id": job_id}
    except Exception as e:
        print(f"Celery task failed for job {job_id}: {e}")
        return {"status": "failed", "job_id": job_id, "error": str(e)}
