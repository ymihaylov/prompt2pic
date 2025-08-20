"""
Simple job status tracking service.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, List


class JobStatus(Enum):
    INIT = "init"
    PENDING = "pending"
    GENERATING_PROMPT = "generating_prompt"
    ABOUT_TO_GENERATE = "about_to_generate_images"  # TODO: Rename this:
    GENERATING_HERO = "generating_hero"
    GENERATING_ABOUT = "generating_about"
    GENERATING_GALLERY = "generating_gallery"
    CREATING_ZIP = "creating_zip"
    COMPLETED = "completed"
    FAILED = "failed"


class ImageStatus(Enum):
    PENDING = "pending"
    GENERATING = "generating"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ImageInfo:
    type: str  # TODO: Change this to be enum
    status: ImageStatus = ImageStatus.PENDING
    url: Optional[str] = None
    local_path: Optional[str] = None
    filename: Optional[str] = None
    prompt: Optional[str] = None
    aspect_ratio: Optional[str] = None
    error: Optional[str] = None
    generated_at: Optional[datetime] = None
    downloaded_at: Optional[datetime] = None


@dataclass
class JobInfo:
    job_id: str
    status: JobStatus = JobStatus.INIT
    progress: int = 0
    message: str = ""
    images: Dict[str, ImageInfo] = field(default_factory=dict)
    zip_path: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()


class JobStatusService:
    """Simple in-memory job status tracking."""

    def __init__(self):
        self._jobs: Dict[str, JobInfo] = {}

    def create_job(self, job_id: str, llm_response: Dict = None) -> JobInfo:
        """Create new job with INIT status and setup image placeholders."""
        # TODO: Check if the job with this id already exists and throw exception
        job = JobInfo(
            job_id=job_id, status=JobStatus.INIT, message="Job created"
        )

        self._jobs[job_id] = job
        return job

    def fill_images_data(self, job_id: str, llm_response: Dict[str, ImageInfo]):
        job = self._jobs[job_id]

        if not job:
            return False

        if llm_response:
            if "hero" in llm_response:
                hero_data = llm_response["hero"]
                job.images["hero"] = ImageInfo(
                    type="hero",
                    prompt=hero_data.get("prompt"),
                    aspect_ratio=hero_data.get("aspect"),
                    filename="hero",  # Extension will be set dynamically during download
                )

            if "about" in llm_response:
                about_data = llm_response["about"]
                job.images["about"] = ImageInfo(
                    type="about",
                    prompt=about_data.get("prompt"),
                    aspect_ratio=about_data.get("aspect"),
                    filename="about",  # Extension will be set dynamically during download
                )

            if "gallery" in llm_response:
                for i, gallery_item in enumerate(llm_response["gallery"]):
                    key = f"gallery_{i+1}"
                    job.images[key] = ImageInfo(
                        type=key,
                        prompt=gallery_item.get("prompt"),
                        aspect_ratio=gallery_item.get("aspect"),
                        filename=f"gallery_{i+1}",  # Extension will be set dynamically during download
                    )

    def update_status(
        self,
        job_id: str,
        status: JobStatus,
        message: str = "",
        progress: int = None,
    ):
        """Update job status."""
        job = self._jobs.get(job_id)
        if not job:
            return False  # TODO: Throw an error

        job.status = status
        job.message = message

        if progress is not None:
            job.progress = progress

        job.updated_at = datetime.utcnow()

        return True

    def update_image_generating(self, job_id: str, image_key: str):
        """Mark image as generating."""
        job = self._jobs.get(job_id)

        if job and image_key in job.images:
            image = job.images[image_key]
            image.status = ImageStatus.GENERATING
            image.generated_at = datetime.utcnow()
            job.updated_at = datetime.utcnow()

            return True

        return False

    def update_image_completed(
        self, job_id: str, image_key: str, url: str, local_path: str
    ):
        job = self._jobs.get(job_id)

        if job and image_key in job.images:
            image = job.images[image_key]
            image.status = ImageStatus.COMPLETED
            image.url = url
            image.local_path = local_path
            image.downloaded_at = datetime.utcnow()
            job.updated_at = datetime.utcnow()
            print(f"[{job_id}] Image {image_key}: completed - {url}")
            return True

        return False

    def update_image_failed(self, job_id: str, image_key: str, error: str):
        job = self._jobs.get(job_id)

        if job and image_key in job.images:
            image = job.images[image_key]
            image.status = ImageStatus.FAILED
            image.error = error
            job.updated_at = datetime.utcnow()

            return True

        return False

    def complete_job(self, job_id: str, zip_path: str = None):
        job = self._jobs.get(job_id)

        if job:
            job.status = JobStatus.COMPLETED
            job.zip_path = zip_path
            job.message = "All images generated and archived"
            job.updated_at = datetime.utcnow()

    def fail_job(self, job_id: str, error: str):
        job = self._jobs.get(job_id)

        if job:
            job.status = JobStatus.FAILED
            job.error = error
            job.message = f"Failed: {error}"
            job.updated_at = datetime.utcnow()

    def get_job(self, job_id: str) -> Optional[JobInfo]:
        return self._jobs.get(job_id)

    def get_job_dict(self, job_id: str) -> Dict:
        job = self._jobs.get(job_id)

        if not job:
            return {"error": "Job not found"}

        total_images = len(job.images)

        completed_images = sum(
            1 for img in job.images.values() if img.status == ImageStatus.COMPLETED
        )

        calculated_progress = (
            int((completed_images / total_images) * 100) if total_images > 0 else 0
        )

        progress = max(job.progress, calculated_progress)

        # TODO: Should be a type or something?
        return {
            "job_id": job.job_id,
            "status": job.status.value,
            "message": job.message,
            "progress": progress,
            "total_images": total_images,
            "completed_images": completed_images,
            "images": {
                key: {
                    "type": img.type,
                    "status": img.status.value,
                    "url": img.url,
                    "local_path": img.local_path,
                    "filename": img.filename,
                    "prompt": img.prompt,
                    "aspect_ratio": img.aspect_ratio,
                    "error": img.error,
                    "generated_at": (
                        img.generated_at.isoformat() if img.generated_at else None
                    ),
                    "downloaded_at": (
                        img.downloaded_at.isoformat() if img.downloaded_at else None
                    ),
                }
                for key, img in job.images.items()
            },
            "zip_path": job.zip_path,
            "created_at": job.created_at.isoformat(),
            "updated_at": job.updated_at.isoformat(),
            "error": job.error,
        }

    def get_completed_images(self, job_id: str) -> List[ImageInfo]:
        """Get all completed images for display."""
        job = self._jobs.get(job_id)
        if not job:
            return []

        return [
            img for img in job.images.values() if img.status == ImageStatus.COMPLETED
        ]
