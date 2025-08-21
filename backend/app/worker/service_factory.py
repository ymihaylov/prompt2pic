"""
Factory for creating service instances in worker context
"""
import logging
from typing import Dict, Any

from app.worker.config import REDIS_URL
from app.worker.exceptions import ServiceInitializationError
from app.services.image_generation_orchestrator import ImageGenerationOrchestrator
from app.services.prompt_template_service import PromptTemplateService
from app.core.factories import LLMProviderFactory, ImageProviderFactory
from app.services.file_manager_service import FileManagerService
from app.services.image_generator_service import ImageGeneratorService
from app.services.job_status_service import JobStatusService
from app.services.progress_calculator import ProgressCalculator
from app.services.image_processing_pipeline import ImageProcessingPipeline
from app.services.redis_service import RedisService

logger = logging.getLogger(__name__)


class WorkerServiceFactory:
    """Factory for creating service instances in worker context"""
    
    _orchestrator_cache: Dict[str, ImageGenerationOrchestrator] = {}
    
    @classmethod
    def create_image_generation_orchestrator(cls) -> ImageGenerationOrchestrator:
        """
        Create and cache image generation orchestrator
        
        Returns:
            ImageGenerationOrchestrator: Configured orchestrator instance
            
        Raises:
            ServiceInitializationError: If service creation fails
        """
        worker_id = "default"  # Could be made dynamic based on worker process
        
        if worker_id in cls._orchestrator_cache:
            return cls._orchestrator_cache[worker_id]
            
        try:
            logger.info("Initializing image generation orchestrator for worker")
            
            # Create all required services
            prompt_service = PromptTemplateService()
            llm_factory = LLMProviderFactory()
            image_factory = ImageProviderFactory()
            file_manager = FileManagerService()
            image_generator = ImageGeneratorService()
            redis_service = RedisService(REDIS_URL)
            status_service = JobStatusService(redis_service)
            progress_calculator = ProgressCalculator()
            image_pipeline = ImageProcessingPipeline(image_generator, file_manager)
            
            orchestrator = ImageGenerationOrchestrator(
                prompt_service=prompt_service,
                llm_factory=llm_factory,
                image_factory=image_factory,
                file_manager=file_manager,
                image_generator=image_generator,
                status_service=status_service,
                progress_calculator=progress_calculator,
                image_pipeline=image_pipeline,
            )
            
            cls._orchestrator_cache[worker_id] = orchestrator
            logger.info("Image generation orchestrator initialized successfully")
            
            return orchestrator
            
        except Exception as e:
            logger.error(f"Failed to initialize image generation orchestrator: {e}")
            raise ServiceInitializationError(f"Service initialization failed: {e}")
    
    @classmethod
    def clear_cache(cls) -> None:
        """Clear service cache (useful for testing)"""
        cls._orchestrator_cache.clear()
        logger.info("Service cache cleared")
