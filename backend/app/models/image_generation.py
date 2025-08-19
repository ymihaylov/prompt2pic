from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.core.interfaces import LLMProviderType, ImageProviderType


class ImageGenerationRequest(BaseModel):
    """Request model for image generation."""

    prompt: str = Field(
        ..., max_length=300, description="User text prompt input (max 300 characters)"
    )
    gallery_count: int = Field(
        0, ge=0, le=15, description="Number of gallery images to generate (0-15)"
    )
    llm_model: LLMProviderType = Field(
        default=LLMProviderType.OPENAI, description="LLM provider choice"
    )
    image_model: ImageProviderType = Field(
        default=ImageProviderType.OPENAI, description="Image provider choice"
    )

    @field_validator("prompt")
    @classmethod
    def prompt_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v.strip()


class ImageGenerationResponse(BaseModel):
    job_id: str
    status: str
    message: str
    created_at: datetime
    request_data: ImageGenerationRequest
    # generated_images: Optional[dict] = None
    # provider_info: Optional[dict] = None
    # processing_time: Optional[float] = None


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: int = Field(ge=0, le=100, description="Progress percentage (0-100)")
    message: str
    created_at: datetime
    updated_at: datetime
    images_generated: int = Field(ge=0, description="Number of images generated so far")
    total_images: int = Field(ge=1, description="Total number of images to generate")


class HelloResponse(BaseModel):
    message: str
