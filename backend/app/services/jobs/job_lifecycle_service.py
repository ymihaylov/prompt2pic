from app.models.domain.job_status import JobStatusType
from app.models.dto.image_generation_request import ImageGenerationRequest
from app.models.dto.llm_image_response import LLMImageResponse
from app.repositories.image_repository import ImageRepository
from app.repositories.job_repository import JobRepository


class JobLifecycleService:

    def __init__(
        self, job_repository: JobRepository, image_repository: ImageRepository
    ):
        self.job_repository = job_repository
        self.image_repository = image_repository

    def initialize_job(self, job_id: str, request: ImageGenerationRequest):
        self.job_repository.create_job(
            job_id,
            request.prompt,
            request.llm_model,
            request.image_model,
            request.gallery_count,
        )
        self.job_repository.update_status(
            job_id, JobStatusType.GENERATING_PROMPT, "Initializing job..."
        )

    def start_prompt_generation(self, job_id: str):
        self.job_repository.update_status(
            job_id, JobStatusType.GENERATING_PROMPT, "Generating enhanced prompts..."
        )

    def complete_prompt_generation(self, job_id: str, llm_response: LLMImageResponse):
        self.image_repository.setup_image_placeholders(job_id, llm_response)

        self.job_repository.update_status(
            job_id,
            JobStatusType.GENERATING_IMAGES,
            "Prompts ready, preparing images...",
        )

    def start_image_generation(self, job_id: str):
        self.job_repository.update_status(
            job_id, JobStatusType.GENERATING_IMAGES, "Image generation..."
        )

    def start_archiving(self, job_id: str):
        self.job_repository.update_status(
            job_id, JobStatusType.CREATING_ZIP, "Creating archive..."
        )

    def complete_job(self, job_id: str, zip_path: str):
        self.job_repository.complete_job(job_id, zip_path)
        self.job_repository.update_status(
            job_id, JobStatusType.COMPLETED, "Job completed successfully!"
        )

        return self.job_repository.get_job_dict(job_id)

    def fail_job(self, job_id: str, error: Exception):
        self.job_repository.fail_job(job_id, str(error))
