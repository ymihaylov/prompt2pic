from functools import lru_cache

from fastapi import Depends

from app.core.settings import settings
from app.infrastructure.providers.image.image_provider_factory import (
    ImageProviderFactory,
)
from app.infrastructure.providers.llm.llm_provider_factory import LLMProviderFactory
from app.infrastructure.storage.file_storage import FileStorage
from app.infrastructure.storage.redis_service import RedisService
from app.repositories.image_repository import ImageRepository
from app.repositories.job_repository import JobRepository
from app.services.images.image_processing_service import (
    ImageProcessingService,
)
from app.services.images.image_task_pipeline import ImageTaskPipeline
from app.services.jobs.job_lifecycle_service import JobLifecycleService
from app.services.llm.llm_processing_service import (
    LLMProcessingService,
)
from app.services.sync_images_generation_workflow import SyncImagesGenerationWorkflow
from app.utils.job_id_handler import JobIdHandler
from app.utils.llm_response_validator import LLMResponseValidator
from app.utils.prompt_template_service import PromptTemplateService


@lru_cache(maxsize=1)
def get_redis_service() -> RedisService:
    return RedisService(settings.redis_url)


@lru_cache(maxsize=1)
def get_prompt_template_service() -> PromptTemplateService:
    return PromptTemplateService()


@lru_cache(maxsize=1)
def get_llm_model_factory() -> LLMProviderFactory:
    return LLMProviderFactory()


@lru_cache(maxsize=1)
def get_image_model_factory() -> ImageProviderFactory:
    return ImageProviderFactory()


@lru_cache(maxsize=1)
def get_file_storage() -> FileStorage:
    return FileStorage()


@lru_cache(maxsize=1)
def get_job_id_handler() -> JobIdHandler:
    return JobIdHandler()


def get_image_repository(
    redis_service: RedisService = Depends(get_redis_service),
) -> ImageRepository:
    return ImageRepository(redis_service)


@lru_cache(maxsize=1)
def get_llm_response_validator() -> LLMResponseValidator:
    return LLMResponseValidator()


def get_llm_processing_service(
    llm_model_factory: LLMProviderFactory = Depends(get_llm_model_factory),
    prompt_template_service: PromptTemplateService = Depends(
        get_prompt_template_service
    ),
    llm_response_validator: LLMResponseValidator = Depends(get_llm_response_validator),
) -> LLMProcessingService:
    return LLMProcessingService(
        llm_model_factory, prompt_template_service, llm_response_validator
    )


def get_job_repository(
    redis_service: RedisService = Depends(get_redis_service),
    image_repository: ImageRepository = Depends(get_image_repository),
) -> JobRepository:
    return JobRepository(image_repository, redis_service)


def get_job_lifycycle_service(
    job_repository: JobRepository = Depends(get_job_repository),
    image_repository: ImageRepository = Depends(get_image_repository),
) -> JobLifecycleService:
    return JobLifecycleService(job_repository, image_repository)


def get_image_task_pipeline(
    file_storage: FileStorage = Depends(get_file_storage),
) -> ImageTaskPipeline:
    return ImageTaskPipeline(file_storage)


def get_image_processing_service(
    image_task_pipeline: ImageTaskPipeline = Depends(get_image_task_pipeline),
    image_repository: ImageRepository = Depends(get_image_repository),
    image_factory: ImageProviderFactory = Depends(get_image_model_factory),
) -> ImageProcessingService:
    return ImageProcessingService(image_task_pipeline, image_repository, image_factory)


def get_sync_image_generation_workflow(
    llm_processing_service: LLMProcessingService = Depends(get_llm_processing_service),
    image_processing_service: ImageProcessingService = Depends(
        get_image_processing_service
    ),
    job_lifecycle_manager: JobLifecycleService = Depends(get_job_lifycycle_service),
    file_manager: FileStorage = Depends(get_file_storage),
) -> SyncImagesGenerationWorkflow:
    return SyncImagesGenerationWorkflow(
        llm_processing_service=llm_processing_service,
        image_processing_service=image_processing_service,
        job_lifecycle_service=job_lifecycle_manager,
        file_storage=file_manager,
    )
