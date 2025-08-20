from functools import lru_cache

from fastapi import Depends

from app.core.factories import LLMProviderFactory, ImageProviderFactory
from app.core.prompt_config import ProviderConfig
from app.services.file_manager_service import FileManagerService
from app.services.image_generation_orchestrator import ImageGenerationOrchestrator
from app.services.image_generator_service import ImageGeneratorService
from app.services.image_processing_pipeline import ImageProcessingPipeline
from app.services.job_status_service import JobStatusService
from app.services.progress_calculator import ProgressCalculator
from app.services.prompt_template_service import PromptTemplateService
from app.services.request_id_service import RequestIdService


@lru_cache()
def get_provider_config() -> ProviderConfig:
    """Get provider configuration - can be overridden for testing."""
    return ProviderConfig()


def get_prompt_template_service() -> PromptTemplateService:
    """Create prompt template service instance."""
    return PromptTemplateService()


def get_llm_factory() -> LLMProviderFactory:
    """Get LLM provider factory."""
    return LLMProviderFactory()


def get_image_factory() -> ImageProviderFactory:
    """Get image provider factory."""
    return ImageProviderFactory()


def get_file_manager() -> FileManagerService:
    """Create file manager service instance."""
    return FileManagerService()


def get_request_id_service() -> RequestIdService:
    """Create request ID service instance."""
    return RequestIdService()


def get_job_status_service() -> JobStatusService:
    """Create job status service instance."""
    return JobStatusService()


def get_image_generator() -> ImageGeneratorService:
    """Create image generator service instance."""
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
