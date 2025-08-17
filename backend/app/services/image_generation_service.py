"""
Business logic for image generation.
"""

import uuid
from datetime import datetime

from app.models.image_generation import ImageGenerationRequest, ImageGenerationResponse
from app.services.prompt_template_service import PromptTemplateService


class ImageGenerationService:
    """Service class for handling image generation business logic."""

    def __init__(self):
        """Initialize the image generation service."""
        self.prompt_service = PromptTemplateService()

    def create_generation_job(
            self, request: ImageGenerationRequest
    ) -> ImageGenerationResponse:
        """
        Create a new image generation job.

        Args:
            request: Image generation request

        Returns:
            ImageGenerationResponse: Job creation response
        """
        job_id = str(uuid.uuid4())

        # Get populated prompt from template service
        try:
            variables = {
                "business_description": request.prompt,
                "gallery_count": request.gallery_count,
            }

            populated_prompt = self.prompt_service.get_populated_prompt(
                template_name="image_generation", variables=variables
            )

            # For now, just print the populated prompt (later we'll send to LLM)
            print(f"Generated prompt for job {job_id}:")
            print("=" * 50)
            print(populated_prompt)
            print("=" * 50)

        except Exception as e:
            print(f"Error generating prompt: {e}")
            # For now, continue with job creation even if prompt generation fails

        return ImageGenerationResponse(
            job_id=job_id,
            status="created",
            message=f"Image generation job created successfully. Will generate 1 hero, 1 about-us, and {request.gallery_count} gallery images.",
            created_at=datetime.utcnow(),
            request_data=request,
        )

    @staticmethod
    def get_job_status(job_id: str) -> dict:
        # Placeholder - implement actual job tracking later
        return {"job_id": job_id, "status": "processing", "progress": 0.5}
