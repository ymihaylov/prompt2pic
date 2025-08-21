from functools import lru_cache

from fastapi import Depends

from app.core.config import settings
from app.core.factories import LLMProviderFactory, ImageProviderFactory
from app.core.prompt_config import ProviderConfig
from app.services.file_manager_service import FileManagerService
from app.services.image_generation_orchestrator import ImageGenerationOrchestrator
from app.services.image_generator_service import ImageGeneratorService
from app.services.image_processing_pipeline import ImageProcessingPipeline
from app.services.job_id_service import JobIdService
from app.services.job_status_service import JobStatusService
from app.services.progress_calculator import ProgressCalculator
from app.services.prompt_template_service import PromptTemplateService
from app.services.redis_service import RedisService


@lru_cache()
def get_provider_config() -> ProviderConfig:
    return ProviderConfig()


@lru_cache()
def get_redis_service() -> RedisService:
    return RedisService(settings.redis_url)


def get_prompt_template_service() -> PromptTemplateService:
    return PromptTemplateService()


def get_llm_factory() -> LLMProviderFactory:
    return LLMProviderFactory()


def get_image_factory() -> ImageProviderFactory:
    return ImageProviderFactory()


def get_file_manager() -> FileManagerService:
    return FileManagerService()


def get_job_id_service() -> JobIdService:
    return JobIdService()


@lru_cache()
def get_job_status_service(
    redis_service: RedisService = Depends(get_redis_service),
) -> JobStatusService:
    return JobStatusService(redis_service)


def get_image_generator() -> ImageGeneratorService:
    return ImageGeneratorService()


def get_image_processing_pipeline(
    image_generator: ImageGeneratorService = Depends(get_image_generator),
    file_manager: FileManagerService = Depends(get_file_manager),
) -> ImageProcessingPipeline:
    return ImageProcessingPipeline(image_generator, file_manager)


def get_progress_calculator() -> ProgressCalculator:
    return ProgressCalculator()


def get_image_generation_orchestrator(
    prompt_service: PromptTemplateService = Depends(get_prompt_template_service),
    llm_factory: LLMProviderFactory = Depends(get_llm_factory),
    image_factory: ImageProviderFactory = Depends(get_image_factory),
    file_manager: FileManagerService = Depends(get_file_manager),
    image_generator: ImageGeneratorService = Depends(get_image_generator),
    status_service: JobStatusService = Depends(get_job_status_service),
    progress_calculator: ProgressCalculator = Depends(get_progress_calculator),
    image_processing_pipeline: ImageProcessingPipeline = Depends(
        get_image_processing_pipeline
    ),
) -> ImageGenerationOrchestrator:
    return ImageGenerationOrchestrator(
        prompt_service=prompt_service,
        llm_factory=llm_factory,
        image_factory=image_factory,
        file_manager=file_manager,
        image_generator=image_generator,
        status_service=status_service,
        progress_calculator=progress_calculator,
        image_pipeline=image_processing_pipeline,
    )
