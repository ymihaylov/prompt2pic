# app/worker/service_container.py
from dataclasses import dataclass
from functools import lru_cache

from app.core.settings import settings
from app.infrastructure.providers.image.image_provider_factory import (
    ImageProviderFactory,
)
from app.infrastructure.providers.llm.llm_provider_factory import LLMProviderFactory
from app.infrastructure.storage.file_storage import FileStorage
from app.infrastructure.storage.redis_service import RedisService
from app.repositories.image_repository import ImageRepository
from app.repositories.job_repository import JobRepository
from app.services.async_images_generation_workflow import AsyncImagesGenerationWorkflow
from app.services.images.image_processing_service import (
    ImageProcessingService,
)
from app.services.images.image_task_pipeline import ImageTaskPipeline
from app.services.jobs.job_lifecycle_service import JobLifecycleService
from app.services.llm.llm_processing_service import (
    LLMProcessingService,
)
from app.utils.llm_response_validator import LLMResponseValidator
from app.utils.prompt_template_service import PromptTemplateService


@dataclass
class ServiceContainer:
    """Centralized service container"""

    job_lifecycle_tracker: JobLifecycleService
    llm_processing_coordinator: LLMProcessingService
    image_processing_coordinator: ImageProcessingService
    file_storage: FileStorage
    job_repository: JobRepository
    image_repository: ImageRepository
    image_factory: ImageProviderFactory
    image_pipeline: ImageTaskPipeline
    async_workflow: AsyncImagesGenerationWorkflow


@lru_cache()
def create_service_container() -> ServiceContainer:
    """Create singleton service container"""
    # Lazy imports to avoid circular dependencies
    # Create core services first

    llm_factory = LLMProviderFactory()
    image_factory = ImageProviderFactory()

    prompt_template_service = PromptTemplateService()
    llm_response_validator = LLMResponseValidator()

    redis_service = RedisService(settings.redis_url)
    image_repository = ImageRepository(redis_service)
    job_repository = JobRepository(image_repository, redis_service)

    job_lifecycle_tracker = JobLifecycleService(job_repository, image_repository)
    llm_processing_coordinator = LLMProcessingService(
        llm_factory, prompt_template_service, llm_response_validator
    )

    file_storage = FileStorage()
    image_pipeline = ImageTaskPipeline(file_storage)

    image_processing_coordinator = ImageProcessingService(
        image_pipeline, image_repository, image_factory
    )

    async_workflow = AsyncImagesGenerationWorkflow(
        llm_processing_service=llm_processing_coordinator,
        image_processing_service=image_processing_coordinator,
        job_lifecycle_service=job_lifecycle_tracker,
        file_storage=file_storage,
        image_repository=image_repository,
        image_factory=image_factory,
        image_pipeline=image_pipeline,
    )

    return ServiceContainer(
        job_lifecycle_tracker,
        llm_processing_coordinator,
        image_processing_coordinator,
        file_storage,
        job_repository,
        image_repository,
        image_factory,
        image_pipeline,
        async_workflow,
    )


def service_container() -> ServiceContainer:
    return create_service_container()
