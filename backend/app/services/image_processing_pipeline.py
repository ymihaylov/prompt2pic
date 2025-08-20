# app/services/image_processing_pipeline.py
from dataclasses import dataclass
from typing import List, Dict, Any

from app.core.interfaces import ImageProvider
from app.services.file_manager_service import FileManagerService
from app.services.image_generator_service import ImageGeneratorService


@dataclass
class ImageTask:
    key: str
    data: Dict[str, Any]
    base_filename: str  # Without extension, e.g., 'hero', 'gallery_1'
    message: str


class ImageProcessingPipeline:
    """Handles the image generation workflow logic"""

    def __init__(
        self, image_generator: ImageGeneratorService, file_manager: FileManagerService
    ):
        self.image_generator = image_generator
        self.file_manager = file_manager

    def create_image_tasks(self, llm_response: Dict[str, Any]) -> List[ImageTask]:
        """Convert LLM response into image tasks"""
        tasks = []

        # Single images
        for key in ["hero", "about"]:
            if key in llm_response:
                tasks.append(
                    ImageTask(
                        key=key,
                        data=llm_response[key],
                        base_filename=key,  # Dynamic extension will be determined during download
                        message=f"Generating {key} image...",
                    )
                )

        # Gallery images
        if "gallery" in llm_response:
            for i, gallery_data in enumerate(llm_response["gallery"]):
                tasks.append(
                    ImageTask(
                        key=f"gallery_{i+1}",
                        data=gallery_data,
                        base_filename=f"gallery_{i+1}",  # Dynamic extension will be determined during download
                        message=f"Generating gallery image {i+1}...",
                    )
                )

        return tasks

    def process_image_task(
        self, task: ImageTask, image_provider: ImageProvider, job_id: str
    ) -> Dict[str, Any]:
        """Process a single image task"""

        # Generate image
        url = self.image_generator.generate_single_image(
            image_provider, task.data["prompt"], task.data["aspect"]
        )

        # Download image with dynamic extension detection
        local_path, actual_filename = self.file_manager.download_single_image(
            url, job_id, task.base_filename
        )

        return {
            "key": task.key,
            "url": url,
            "local_path": local_path,
            "filename": actual_filename,  # Now contains the proper extension
        }
