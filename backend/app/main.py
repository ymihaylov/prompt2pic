"""
Main FastAPI application factory.
"""

import logging

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()

from app.api.endpoints import api_router
from app.core.logging_config import configure_logging
from app.api.middlewares import register_middlewares


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Prompt2Pic API",
        description="A FastAPI application for AI-powered image generation",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    register_middlewares(app)

    app.include_router(api_router)
    
    # Mount static files for serving images and downloads
    app.mount("/data", StaticFiles(directory="data"), name="files")

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request):
        logging.getLogger(__name__).exception(
            "Unhandled exception",
            extra={
                "path": request.url.path,
                "method": request.method,
            },
        )
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
            },
        )

    return app


app = create_app()
