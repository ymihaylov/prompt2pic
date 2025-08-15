from typing import Dict

from pydantic import BaseModel, Field, field_validator

from app.infrastructure.providers.image.image_provider_type import ImageProviderType
from app.infrastructure.providers.llm.llm_provider_type import LLMProviderType


class ImageGenerationRequest(BaseModel):
    prompt: str = Field(
        ..., max_length=300, description="User text prompt input (max 300 characters)"
    )
    gallery_count: int = Field(
        0, ge=0, le=15, description="Number of gallery images to generate (0-15)"
    )
    llm_model: LLMProviderType = Field(
        default=LLMProviderType.SIMULATION, description="LLM provider choice"
    )
    image_model: ImageProviderType = Field(
        default=ImageProviderType.SIMULATION, description="Image provider choice"
    )

    @field_validator("prompt")
    @classmethod
    def prompt_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v.strip()


class ImageGenerationResponse(BaseModel):
    job_status: Dict
