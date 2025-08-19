from functools import lru_cache

from fastapi import Depends

from app.core.factories import LLMProviderFactory, ImageProviderFactory
from app.core.prompt_config import ProviderConfig
from app.services.file_manager_service import FileManagerService
from app.services.image_generation_orchestrator import ImageGenerationOrchestrator
from app.services.image_generator_service import ImageGeneratorService
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


def get_image_generator() -> ImageGeneratorService:
    """Create image generator service instance."""
    return ImageGeneratorService()


def get_request_id_service() -> RequestIdService:
    """Create request ID service instance."""
    return RequestIdService()


def get_image_generation_orchestrator(
    prompt_service: PromptTemplateService = Depends(get_prompt_template_service),
    llm_factory: LLMProviderFactory = Depends(get_llm_factory),
    image_factory: ImageProviderFactory = Depends(get_image_factory),
    file_manager: FileManagerService = Depends(get_file_manager),
    image_generator: ImageGeneratorService = Depends(get_image_generator),
) -> ImageGenerationOrchestrator:
    return ImageGenerationOrchestrator(
        prompt_service=prompt_service,
        llm_factory=llm_factory,
        image_factory=image_factory,
        file_manager=file_manager,
        image_generator=image_generator,
    )
