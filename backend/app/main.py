"""
Main FastAPI application factory.
"""

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from app.api.routes import api_router


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.

    Returns:
        Configured FastAPI app instance
    """
    app = FastAPI(
        title="Prompt2Pic API",
        description="A FastAPI application for AI-powered image generation",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Include API routes
    app.include_router(api_router)

    return app


# Create app instance
app = create_app()
