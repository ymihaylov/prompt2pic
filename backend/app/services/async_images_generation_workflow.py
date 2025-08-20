from app.infrastructure.providers.image.image_provider_factory import (
    ImageProviderFactory,
)
from app.infrastructure.providers.image.image_provider_type import ImageProviderType
from app.infrastructure.storage.file_storage import FileStorage
from app.models.domain.image_task import ImageTask
from app.models.dto.image_generation_request import ImageGenerationRequest
from app.repositories.image_repository import ImageRepository
from app.services.images.image_processing_service import ImageProcessingService
from app.services.images.image_task_pipeline import ImageTaskPipeline
from app.services.jobs.job_lifecycle_service import JobLifecycleService
from app.services.llm.llm_processing_service import LLMProcessingService


class AsyncImagesGenerationWorkflow:
    def __init__(
        self,
        llm_processing_service: LLMProcessingService,
        image_processing_service: ImageProcessingService,
        job_lifecycle_service: JobLifecycleService,
        file_storage: FileStorage,
        image_repository: ImageRepository,
        image_factory: ImageProviderFactory,
        image_pipeline: ImageTaskPipeline,
    ):
        self.llm_processing_service = llm_processing_service
        self.image_processing_service = image_processing_service
        self.job_lifecycle_service = job_lifecycle_service
        self.file_storage = file_storage
        self.image_repository = image_repository
        self.image_factory = image_factory
        self.image_pipeline = image_pipeline

    def start_job(self, request: ImageGenerationRequest, job_id: str) -> dict:
        # 1. Initialize
        self.job_lifecycle_service.initialize_job(job_id, request)

        # 2. Generate enhanced prompts
        llm_response = self.llm_processing_service.generate_enhanced_prompts(request)
        self.job_lifecycle_service.complete_prompt_generation(job_id, llm_response)

        # 3. Process images in parallel (Celery chord)
        chord_task_id = self.image_processing_service.process_all_images_parallel(
            llm_response, request.image_model, job_id
        )

        return {
            "status": "images_processing",
            "job_id": job_id,
            "chord_task_id": chord_task_id,
        }

    def process_single_image(
        self, task: ImageTask, image_provider_type: ImageProviderType, job_id: str
    ) -> dict:
        # Update status to generating
        self.image_repository.update_image_generating(job_id, task.image_type)

        # Process image generation
        image_provider = self.image_factory.create(image_provider_type)
        result = self.image_pipeline.process_image_task(task, image_provider, job_id)

        # Update status to completed
        self.image_repository.update_image_completed(
            job_id, result.image_type, result.url, result.local_path
        )

        return result.to_dict()

    def finalize_job(self, job_id: str) -> dict:
        # Create final archive
        self.job_lifecycle_service.start_archiving(job_id)
        zip_path = self.file_storage.create_zip_from_directory(job_id)

        # Complete the job
        self.job_lifecycle_service.complete_job(job_id, zip_path)

        return {"status": "completed", "job_id": job_id, "zip_path": zip_path}
