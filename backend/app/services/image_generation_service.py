"""
Business logic for image generation.
"""

import os
import uuid
from datetime import datetime

from app.models.image_generation import ImageGenerationRequest, ImageGenerationResponse
from app.services.llm_service import LLMService
from app.services.prompt_template_service import PromptTemplateService


class ImageGenerationService:
    def __init__(self):
        self.prompt_service = PromptTemplateService()

        # Get OpenAI API key from environment
        api_key = os.getenv("OPENAI_API_KEY")

        self.llm_service = LLMService(api_key)

    def create_generation_job(
        self, request: ImageGenerationRequest
    ) -> ImageGenerationResponse:
        job_id = str(uuid.uuid4())

        try:
            variables = {
                "business_description": request.prompt,
                "gallery_count": request.gallery_count,
            }

            populated_prompt = self.prompt_service.get_populated_prompt(
                template_name="image_generation", variables=variables
            )

            llm_response = self.llm_service.generate_image_prompts(populated_prompt)
            print(f"LLM Response for job {job_id}:")
            print("=" * 50)
            print(llm_response)
            print("=" * 50)

        except Exception as e:
            print(f"Error in prompt generation/LLM call: {e}")
            # Continue with job creation even if LLM fails

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
