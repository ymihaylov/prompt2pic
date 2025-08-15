# app/models/llm_image_response.py
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class ImagePromptData(BaseModel):

    prompt: str = Field(..., min_length=10)
    aspect: Literal["1:1", "16:9", "3:4"]

    image_type: Optional[str] = None
    base_filename: Optional[str] = None


class LLMImageResponse(BaseModel):
    hero: ImagePromptData
    about: ImagePromptData
    gallery: List[ImagePromptData] = Field(..., min_items=1, max_items=15)
    negative_prompt: str = Field(default="text, watermark, logo, trademark, blurry")

    @field_validator("gallery")
    def validate_gallery_aspects(cls, v):
        for item in v:
            if item.aspect != "1:1":
                raise ValueError("Gallery images must have 1:1 aspect ratio")
        return v

    @field_validator("hero")
    def validate_hero_aspect(cls, v):
        if v.aspect != "16:9":
            raise ValueError("Hero image must have 16:9 aspect ratio")
        return v

    @field_validator("about")
    def validate_about_aspect(cls, v):
        if v.aspect != "3:4":
            raise ValueError("About image must have 3:4 aspect ratio")
        return v
