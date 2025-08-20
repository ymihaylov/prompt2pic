from app.infrastructure.storage.file_storage import FileStorage
from app.models.dto.image_generation_request import (
    ImageGenerationRequest,
    ImageGenerationResponse,
)
from app.services.images.image_processing_service import (
    ImageProcessingService,
)
from app.services.jobs.job_lifecycle_service import JobLifecycleService
from app.services.llm.llm_processing_service import (
    LLMProcessingService,
)


class SyncImagesGenerationWorkflow:
    def __init__(
        self,
        llm_processing_service: LLMProcessingService,
        image_processing_service: ImageProcessingService,
        job_lifecycle_service: JobLifecycleService,
        file_storage: FileStorage,
    ):
        self.llm_processing_service = llm_processing_service
        self.image_processing_service = image_processing_service
        self.job_lifecycle_service = job_lifecycle_service
        self.file_storage = file_storage

    def generate_images(
        self, request: ImageGenerationRequest, job_id: str
    ) -> ImageGenerationResponse:
        try:
            # 1. Initialize
            self.job_lifecycle_service.initialize_job(job_id, request)

            # 2. Generate enhanced prompts
            llm_response = self.llm_processing_service.generate_enhanced_prompts(
                request
            )
            self.job_lifecycle_service.complete_prompt_generation(job_id, llm_response)

            # 3. Process all images
            self.image_processing_service.process_all_images_sequential(
                llm_response, request.image_model, job_id
            )

            # 4. Create final archive
            self.job_lifecycle_service.start_archiving(job_id)
            zip_path = self.file_storage.create_zip_from_directory(job_id)

            # 5. Complete job
            job_dict = self.job_lifecycle_service.complete_job(job_id, zip_path)

            return self._create_response(job_dict)

        except Exception as e:
            self._handle_failure(job_id, e)
            raise

    def _create_response(self, job_dict) -> ImageGenerationResponse:
        """Create final response"""
        return ImageGenerationResponse(job_status=job_dict)

    def _handle_failure(self, job_id: str, error: Exception):
        """Handle job failure"""
        self.job_lifecycle_service.fail_job(job_id, error)
