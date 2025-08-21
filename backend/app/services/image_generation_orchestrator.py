from typing import Dict, Any

from app.core.factories import LLMProviderFactory, ImageProviderFactory
from app.core.interfaces import ImageProvider
from app.models.image_generation import ImageGenerationRequest, ImageGenerationResponse
from app.services.file_manager_service import FileManagerService
from app.services.image_generator_service import ImageGeneratorService
from app.services.image_processing_pipeline import ImageTask, ImageProcessingPipeline
from app.services.job_status_service import JobStatusService, JobStatus
from app.services.progress_calculator import ProgressCalculator
from app.services.prompt_template_service import PromptTemplateService


class ImageGenerationOrchestrator:
    def __init__(
        self,
        prompt_service: PromptTemplateService,
        llm_factory: LLMProviderFactory,
        image_factory: ImageProviderFactory,
        file_manager: FileManagerService,
        image_generator: ImageGeneratorService,
        status_service: JobStatusService,
        progress_calculator: ProgressCalculator,
        image_pipeline: ImageProcessingPipeline,
    ):
        self.prompt_service = prompt_service
        self.llm_factory = llm_factory
        self.image_factory = image_factory
        self.file_manager = file_manager
        self.image_generator = image_generator
        self.status_service = status_service
        self.progress_calculator = progress_calculator
        self.image_pipeline = image_pipeline

    def generate_images(
        self, request: ImageGenerationRequest, job_id: str
    ) -> ImageGenerationResponse:

        try:
            # 1. Initialize
            self._initialize_job(job_id, request)

            # 2. Generate enhanced prompts
            llm_response = self._generate_enhanced_prompts(request, job_id)

            # 3. Process all images
            self._process_all_images(llm_response, request, job_id)

            # 4. Create final archive
            zip_path = self._create_final_archive(job_id)

            # 5. Complete job
            self._complete_job(job_id, zip_path)

            return self._create_response(request, job_id, zip_path)

        except Exception as e:
            self._handle_failure(job_id, e)
            raise

    def _initialize_job(self, job_id: str, request: ImageGenerationRequest):
        self.status_service.create_job(job_id)

        progress = self.progress_calculator.get_stage_progress("prompt_generation")
        self.status_service.update_status(
            job_id, JobStatus.GENERATING_PROMPT, "Initializing job...", progress
        )

    def _generate_enhanced_prompts(
        self, request: ImageGenerationRequest, job_id: str
    ) -> Dict[str, Any]:
        """Generate enhanced prompts using LLM"""

        progress = self.progress_calculator.get_stage_progress("llm_processing")
        self.status_service.update_status(
            job_id,
            JobStatus.GENERATING_PROMPT,
            "Generating enhanced prompts...",
            progress,
        )

        llm_provider = self.llm_factory.create(request.llm_model)
        populated_prompt = self.prompt_service.get_populated_prompt(
            template_name="image_generation",
            variables={
                "business_description": request.prompt,
                "gallery_count": request.gallery_count,
            },
        )
        llm_response = llm_provider.generate_prompts(populated_prompt)

        # Update job with full details
        self.status_service.fill_images_data(job_id, llm_response)

        return llm_response

    def _process_all_images(
        self,
        llm_response: Dict[str, Any],
        request: ImageGenerationRequest,
        job_id: str,
    ):
        image_provider = self.image_factory.create(request.image_model)

        image_tasks = self.image_pipeline.create_image_tasks(llm_response)

        progress = self.progress_calculator.get_stage_progress("image_generation")
        self.status_service.update_status(
            job_id,
            JobStatus.ABOUT_TO_GENERATE,
            "Starting image generation...",
            progress,
        )

        for i, task in enumerate(image_tasks):
            self._process_single_image_with_status(
                task, image_provider, job_id, i, len(image_tasks)
            )

    def _process_single_image_with_status(
        self,
        task: ImageTask,
        image_provider: ImageProvider,
        job_id: str,
        current_index: int,
        total_images: int,
    ):
        try:
            progress = self.progress_calculator.calculate_image_progress(
                current_index, total_images
            )
            self.status_service.update_status(
                job_id,
                self._get_status_for_image_type(task.key),
                task.message,
                progress,
            )
            self.status_service.update_image_generating(job_id, task.key)

            # Process the image
            result = self.image_pipeline.process_image_task(
                task, image_provider, job_id
            )

            # Update status - completed
            self.status_service.update_image_completed(
                job_id, result["key"], result["url"], result["local_path"]
            )

        except Exception as e:
            self.status_service.update_image_failed(job_id, task.key, str(e))
            raise

    def _create_final_archive(self, job_id: str) -> str:
        """Create final archive"""
        progress = self.progress_calculator.get_stage_progress("archive_creation")

        self.status_service.update_status(
            job_id, JobStatus.CREATING_ZIP, "Creating archive...", progress
        )
        return self.file_manager.create_zip_from_directory(job_id)

    def _complete_job(self, job_id: str, zip_path: str):
        """Complete the job"""
        self.status_service.complete_job(job_id, zip_path)
        progress = self.progress_calculator.get_stage_progress("completion")
        self.status_service.update_status(
            job_id, JobStatus.COMPLETED, "Job completed successfully!", progress
        )

    def _create_response(
        self, request: ImageGenerationRequest, job_id: str, zip_path: str
    ) -> ImageGenerationResponse:
        """Create final response"""
        return ImageGenerationResponse(
            job_status=self.status_service.get_job_dict(job_id),
        )

    def _handle_failure(self, job_id: str, error: Exception):
        """Handle job failure"""
        self.status_service.fail_job(job_id, str(error))

    def _get_status_for_image_type(self, image_key: str) -> JobStatus:
        """Get appropriate status enum for image type"""
        if image_key == "hero":
            return JobStatus.GENERATING_HERO
        elif image_key == "about":
            return JobStatus.GENERATING_ABOUT
        else:
            return JobStatus.GENERATING_GALLERY
