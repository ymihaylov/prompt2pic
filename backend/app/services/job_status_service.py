"""
Redis-based job status tracking service.
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, List

from app.services.redis_service import RedisService


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

    def to_json(self) -> str:
        data = asdict(self)
        data["status"] = self.status.value
        # Convert datetime objects to ISO format strings
        if data.get("created_at"):
            data["created_at"] = data["created_at"].isoformat()
        if data.get("updated_at"):
            data["updated_at"] = data["updated_at"].isoformat()

        # Convert ImageInfo datetime fields and status enum
        for image_key, image_data in data.get("images", {}).items():
            if image_data.get("generated_at"):
                image_data["generated_at"] = image_data["generated_at"].isoformat()
            if image_data.get("downloaded_at"):
                image_data["downloaded_at"] = image_data["downloaded_at"].isoformat()
            if image_data.get("status"):
                image_data["status"] = image_data["status"].value

        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> "JobInfo":
        data = json.loads(json_str)
        data["status"] = JobStatus(data["status"])

        # Convert ISO format strings back to datetime objects
        if data.get("created_at"):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])

        # Convert ImageInfo objects back
        if data.get("images"):
            images = {}
            for image_key, image_data in data["images"].items():
                if image_data.get("generated_at"):
                    image_data["generated_at"] = datetime.fromisoformat(
                        image_data["generated_at"]
                    )
                if image_data.get("downloaded_at"):
                    image_data["downloaded_at"] = datetime.fromisoformat(
                        image_data["downloaded_at"]
                    )
                if image_data.get("status"):
                    image_data["status"] = ImageStatus(image_data["status"])
                images[image_key] = ImageInfo(**image_data)
            data["images"] = images

        return cls(**data)


class JobStatusService:
    def __init__(self, redis_service: RedisService):
        self.redis_client = redis_service.get_client()
        self.job_prefix = "job:"
        self.job_ttl = 86400  # 24 hours

    def create_job(self, job_id: str) -> JobInfo:
        # Check if the job with this id already exists and throw exception
        if self.redis_client.exists(f"{self.job_prefix}{job_id}"):
            raise ValueError(f"Job with ID {job_id} already exists")

        job = JobInfo(job_id=job_id, status=JobStatus.INIT, message="Job created")

        self.redis_client.setex(
            f"{self.job_prefix}{job_id}",
            self.job_ttl,
            job.to_json(),
        )

        return job

    def fill_images_data(self, job_id: str, llm_response: Dict[str, ImageInfo]):
        job_data = self.redis_client.get(f"{self.job_prefix}{job_id}")
        if not job_data:
            raise ValueError(f"Job with ID {job_id} not found")

        job = JobInfo.from_json(job_data.decode())

        if llm_response:
            if "hero" in llm_response:
                hero_data = llm_response["hero"]
                job.images["hero"] = ImageInfo(
                    type="hero",
                    prompt=hero_data.get("prompt"),
                    aspect_ratio=hero_data.get("aspect"),
                    filename="hero",
                )

            if "about" in llm_response:
                about_data = llm_response["about"]
                job.images["about"] = ImageInfo(
                    type="about",
                    prompt=about_data.get("prompt"),
                    aspect_ratio=about_data.get("aspect"),
                    filename="about",
                )

            if "gallery" in llm_response:
                for i, gallery_item in enumerate(llm_response["gallery"]):
                    key = f"gallery_{i+1}"
                    job.images[key] = ImageInfo(
                        type=key,
                        prompt=gallery_item.get("prompt"),
                        aspect_ratio=gallery_item.get("aspect"),
                        filename=f"gallery_{i+1}",
                    )

        self.redis_client.setex(
            f"{self.job_prefix}{job_id}",
            self.job_ttl,
            job.to_json(),
        )

    def update_status(
        self,
        job_id: str,
        status: JobStatus,
        message: str = "",
        progress: int = None,
    ):
        job_data = self.redis_client.get(f"{self.job_prefix}{job_id}")
        if not job_data:
            raise ValueError(f"Job with ID {job_id} not found")

        job = JobInfo.from_json(job_data.decode())

        job.status = status
        job.message = message

        if progress is not None:
            job.progress = progress

        job.updated_at = datetime.utcnow()

        self.redis_client.setex(
            f"{self.job_prefix}{job_id}",
            self.job_ttl,
            job.to_json(),
        )

        return True

    def update_image_generating(self, job_id: str, image_key: str):
        """Mark image as generating."""
        job_data = self.redis_client.get(f"{self.job_prefix}{job_id}")
        if not job_data:
            raise ValueError(f"Job with ID {job_id} not found")

        job = JobInfo.from_json(job_data.decode())

        if job and image_key in job.images:
            image = job.images[image_key]
            image.status = ImageStatus.GENERATING
            image.generated_at = datetime.utcnow()
            job.updated_at = datetime.utcnow()

            self.redis_client.setex(
                f"{self.job_prefix}{job_id}",
                self.job_ttl,
                job.to_json(),
            )

            return True

        return False

    def update_image_completed(
        self, job_id: str, image_key: str, url: str, local_path: str
    ):
        job_data = self.redis_client.get(f"{self.job_prefix}{job_id}")
        if not job_data:
            raise ValueError(f"Job with ID {job_id} not found")

        job = JobInfo.from_json(job_data.decode())

        if job and image_key in job.images:
            image = job.images[image_key]
            image.status = ImageStatus.COMPLETED
            image.url = url
            image.local_path = local_path
            image.downloaded_at = datetime.utcnow()
            job.updated_at = datetime.utcnow()

            self.redis_client.setex(
                f"{self.job_prefix}{job_id}",
                self.job_ttl,
                job.to_json(),
            )

            return True

        return False

    def update_image_failed(self, job_id: str, image_key: str, error: str):
        job_data = self.redis_client.get(f"{self.job_prefix}{job_id}")
        if not job_data:
            raise ValueError(f"Job with ID {job_id} not found")

        job = JobInfo.from_json(job_data.decode())

        if job and image_key in job.images:
            image = job.images[image_key]
            image.status = ImageStatus.FAILED
            image.error = error
            job.updated_at = datetime.utcnow()

            self.redis_client.setex(
                f"{self.job_prefix}{job_id}",
                self.job_ttl,
                job.to_json(),
            )

            return True

        return False

    def complete_job(self, job_id: str, zip_path: str = None):
        job_data = self.redis_client.get(f"{self.job_prefix}{job_id}")
        if not job_data:
            raise ValueError(f"Job with ID {job_id} not found")

        job = JobInfo.from_json(job_data.decode())

        if job:
            job.status = JobStatus.COMPLETED
            job.zip_path = zip_path
            job.message = "All images generated and archived"
            job.updated_at = datetime.utcnow()

            self.redis_client.setex(
                f"{self.job_prefix}{job_id}",
                self.job_ttl,
                job.to_json(),
            )

    def fail_job(self, job_id: str, error: str):
        job_data = self.redis_client.get(f"{self.job_prefix}{job_id}")
        if not job_data:
            raise ValueError(f"Job with ID {job_id} not found")

        job = JobInfo.from_json(job_data.decode())

        if job:
            job.status = JobStatus.FAILED
            job.error = error
            job.message = f"Failed: {error}"
            job.updated_at = datetime.utcnow()

            self.redis_client.setex(
                f"{self.job_prefix}{job_id}",
                self.job_ttl,
                job.to_json(),
            )

    def get_job_dict(self, job_id: str) -> Dict:
        job_data = self.redis_client.get(f"{self.job_prefix}{job_id}")
        if not job_data:
            raise ValueError(f"Job with ID {job_id} not found")

        job = JobInfo.from_json(job_data.decode())

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
        job_data = self.redis_client.get(f"{self.job_prefix}{job_id}")
        if not job_data:
            raise ValueError(f"Job with ID {job_id} not found")

        job = JobInfo.from_json(job_data.decode())
        if not job:
            return []

        return [
            img for img in job.images.values() if img.status == ImageStatus.COMPLETED
        ]

    def health_check(self) -> bool:
        """Check if Redis is accessible"""
        try:
            return self.redis_client.ping()
        except:
            return False
