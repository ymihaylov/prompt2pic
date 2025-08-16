from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Optional
import uuid
from datetime import datetime

# Create FastAPI instance
app = FastAPI(title="Prompt2Pic API", description="A simple FastAPI application", version="1.0.0")

# Basic hello world endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# Additional endpoint with path parameter
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Pydantic models for request/response validation
class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., max_length=300, description="User text input (max 300 characters)")
    gallery_count: int = Field(0, ge=0, le=15, description="Number of gallery images to generate (0-15)")
    
    @validator('prompt')
    def prompt_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Prompt cannot be empty')
        return v.strip()


class ImageGenerationResponse(BaseModel):
    job_id: str
    status: str
    message: str
    created_at: datetime
    request_data: ImageGenerationRequest


# Main image generation endpoint
@app.post("/generate-images", response_model=ImageGenerationResponse)
async def generate_images(request: ImageGenerationRequest):
    """
    Receive user prompt and gallery count to start image generation process.
    
    - **prompt**: Text description (max 300 characters)
    - **gallery_count**: Number of gallery images to generate (0-15)
    """
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # For now, just return the job created response
    # Later we'll implement the actual LLM and image generation logic
    return ImageGenerationResponse(
        job_id=job_id,
        status="created",
        message=f"Image generation job created successfully. Will generate 1 hero, 1 about-us, and {request.gallery_count} gallery images.",
        created_at=datetime.utcnow(),
        request_data=request
    )
