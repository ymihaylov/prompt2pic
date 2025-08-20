from dataclasses import dataclass
from typing import List

from app.infrastructure.providers.image.base_image_provider import ImageProvider
from app.infrastructure.storage.file_storage import FileStorage
from app.models.domain.image_task import ImageTask
from app.models.dto.llm_image_response import LLMImageResponse


@dataclass
class ImageGenerationResult:
    image_type: str
    url: str
    local_path: str
    filename: str
    prompt: str
    aspect_ratio: str

    def to_dict(self) -> dict:
        """Convert to dict for backwards compatibility"""
        return {
            "image_type": self.image_type,
            "url": self.url,
            "local_path": self.local_path,
            "filename": self.filename,
            "prompt": self.prompt,
            "aspect_ratio": self.aspect_ratio,
        }


class ImageTaskPipeline:
    def __init__(self, file_storage: FileStorage):
        self.file_storage = file_storage

    def create_image_tasks(self, llm_response: LLMImageResponse) -> List[ImageTask]:
        tasks = [
            ImageTask(
                image_type="hero",
                data=llm_response.hero.dict(),
                base_filename="hero",
                message="Generating hero image...",
            ),
            ImageTask(
                image_type="about",
                data=llm_response.about.dict(),
                base_filename="about",
                message="Generating about image...",
            ),
        ]

        for i, gallery_item in enumerate(llm_response.gallery):
            tasks.append(
                ImageTask(
                    image_type=f"gallery_{i + 1}",
                    data=gallery_item.dict(),
                    base_filename=f"gallery_{i+1}",
                    message=f"Generating gallery image {i+1}...",
                )
            )

        return tasks

    def process_image_task(
        self, task: ImageTask, image_provider: ImageProvider, job_id: str
    ) -> ImageGenerationResult:
        # Generate image
        url = image_provider.generate_image(task.data["prompt"], task.data["aspect"])

        # Download image
        local_path, actual_filename = self.file_storage.download_single_image(
            url, job_id, task.base_filename
        )

        # Save prompt
        self.file_storage.save_prompt(task.data["prompt"], job_id, task.base_filename)

        return ImageGenerationResult(
            image_type=task.image_type,
            url=url,
            local_path=local_path,
            filename=actual_filename,
            prompt=task.data["prompt"],
            aspect_ratio=task.data["aspect"],
        )
