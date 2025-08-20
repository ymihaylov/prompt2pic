from celery import chord, group

from app.infrastructure.providers.image.base_image_provider import ImageProvider
from app.infrastructure.providers.image.image_provider_factory import (
    ImageProviderFactory,
)
from app.infrastructure.providers.image.image_provider_type import ImageProviderType
from app.models.domain.image_task import ImageTask
from app.models.dto.llm_image_response import LLMImageResponse
from app.repositories.image_repository import ImageRepository
from app.services.images.image_task_pipeline import ImageTaskPipeline


class ImageProcessingService:

    def __init__(
        self,
        image_pipeline: ImageTaskPipeline,
        image_repository: ImageRepository,
        image_factory: ImageProviderFactory,
    ):
        self.image_pipeline = image_pipeline
        self.image_repository = image_repository
        self.image_factory = image_factory

    def process_all_images_sequential(
        self,
        llm_response: LLMImageResponse,
        image_model: ImageProviderType,
        job_id: str,
    ):
        image_tasks = self.image_pipeline.create_image_tasks(llm_response)

        image_provider = self.image_factory.create(image_model)

        for image_task in image_tasks:
            self._process_single_image(image_task, image_provider, job_id)

    def process_all_images_parallel(
        self,
        llm_response: LLMImageResponse,
        image_model: ImageProviderType,
        job_id: str,
    ) -> str:
        """Process all images in parallel using Celery chord"""

        from app.worker.tasks import (
            generate_single_image_task,
            finalize_generation_task,
        )

        image_tasks = self.image_pipeline.create_image_tasks(llm_response)

        image_job_group = group(
            [
                generate_single_image_task.s(task.to_dict(), image_model.value, job_id)
                for task in image_tasks
            ]
        )

        callback = finalize_generation_task.s(job_id)

        chord_result = chord(image_job_group)(callback)

        return chord_result.id

    def _process_single_image(
        self,
        image_task: ImageTask,
        image_provider: ImageProvider,
        job_id: str,
    ):
        try:
            self.image_repository.update_image_generating(job_id, image_task.image_type)

            result = self.image_pipeline.process_image_task(
                image_task, image_provider, job_id
            )

            self.image_repository.update_image_completed(
                job_id, result.image_type, result.url, result.local_path
            )

        except Exception as e:
            self.image_repository.update_image_failed(
                job_id, image_task.image_type, str(e)
            )
            raise
