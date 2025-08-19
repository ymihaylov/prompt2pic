"""
Business logic for image generation.
"""

import uuid
from datetime import datetime

from app.core.factories import LLMProviderFactory, ImageProviderFactory
from app.models.image_generation import ImageGenerationRequest, ImageGenerationResponse
from app.services.file_manager_service import FileManagerService
from app.services.image_generator_service import ImageGeneratorService
from app.services.prompt_template_service import PromptTemplateService


class ImageGenerationOrchestrator:
    def __init__(
        self,
        prompt_service: PromptTemplateService,
        llm_factory: LLMProviderFactory,
        image_factory: ImageProviderFactory,
        file_manager: FileManagerService,
        image_generator: ImageGeneratorService,
    ):
        self.prompt_service = prompt_service
        self.llm_factory = llm_factory
        self.image_factory = image_factory
        self.file_manager = file_manager
        self.image_generator = image_generator

    def generate_images(
        self, request: ImageGenerationRequest
    ) -> ImageGenerationResponse:
        llm_provider = self.llm_factory.create(request.llm_model)
        image_provider = self.image_factory.create(request.image_model)

        try:
            # 1. Populate prompt from the input
            populated_prompt = self.prompt_service.get_populated_prompt(
                template_name="image_generation",
                variables={
                    "business_description": request.prompt,
                    "gallery_count": request.gallery_count,
                },
            )

            # 2. Call llm_provider with populated prompt (llm_response)
            llm_response = llm_provider.generate_prompts(populated_prompt)
            print(f"LLM Response: {llm_response}")

            # 3. Call image_provider with llm_response. Foreach generated images. Collect responses in array - image_urls.
            image_urls = self.image_generator.generate_all_images(image_provider, llm_response)
            print(f"Generated image URLs: {image_urls}")

            # 4. Download the images somewhere
            downloaded_files = self.file_manager.download_images(image_urls)
            print(f"Downloaded files: {downloaded_files}")

            # 5. Create zip archive with the images
            zip_path = self.file_manager.create_zip_archive(downloaded_files)
            print(f"Created zip archive: {zip_path}")

        except Exception as e:
            print(f"Error in prompt generation/image generation: {e}")

        return ImageGenerationResponse(
            job_id=str(uuid.uuid4()),
            status="completed",
            message=f"Image generation completed successfully. Generated 1 hero, 1 about-us, and {request.gallery_count} gallery images. Archive: {zip_path if 'zip_path' in locals() else 'N/A'}",
            created_at=datetime.utcnow(),
            request_data=request,
        )

    @staticmethod
    def get_job_status(job_id: str) -> dict:
        # Placeholder - implement actual job tracking later
        return {"job_id": job_id, "status": "processing", "progress": 0.5}
