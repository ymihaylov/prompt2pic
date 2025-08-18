from datetime import datetime
from typing import Dict

from app.infrastructure.providers.image.image_provider_type import ImageProviderType
from app.infrastructure.providers.llm.llm_provider_type import LLMProviderType
from app.infrastructure.storage.redis_service import RedisService
from app.models.domain.job_status import JobStatusType, JobStatusInfo
from app.repositories.image_repository import (
    ImageRepository,
)


class JobRepository:
    def __init__(self, image_repository: ImageRepository, redis_service: RedisService):
        self.image_repository = image_repository
        self.redis_client = redis_service.get_client()

        self.job_prefix = "job:"
        self.job_ttl = 86400  # 24h

    def create_job(
        self,
        job_id: str,
        prompt: str,
        llm_model: LLMProviderType,
        image_model: ImageProviderType,
        gallery_count,
    ) -> JobStatusInfo:
        if self.redis_client.exists(self._job_key(job_id)):
            raise ValueError(f"Job with ID {job_id} already exists")

        job = JobStatusInfo(
            job_id=job_id,
            status=JobStatusType.INIT,
            message="Job created",
            llm_model=llm_model.value,
            image_model=image_model.value,
            gallery_count=gallery_count,
            prompt=prompt,
        )

        self.redis_client.setex(self._job_key(job_id), self.job_ttl, job.to_json())

        return job

    def update_status(self, job_id: str, status: JobStatusType, message: str = ""):
        job_data = self.redis_client.get(self._job_key(job_id))
        if not job_data:
            raise ValueError(f"Job with ID {job_id} not found")

        job = JobStatusInfo.from_json(job_data.decode())

        job.status = status
        job.message = message

        job.updated_at = datetime.utcnow()

        self.redis_client.set(
            self._job_key(job_id),
            job.to_json(),
        )

        return True

    def _job_key(self, job_id: str) -> str:
        return f"{self.job_prefix}{job_id}"

    def get_job_dict(self, job_id: str) -> Dict:
        key = self._job_key(job_id)
        raw = self.redis_client.get(key)
        if not raw:
            raise ValueError(f"Job with ID {job_id} not found")

        job = JobStatusInfo.from_json(raw.decode("utf-8"))

        image_statuses = self.image_repository.get_all_image_statuses(job_id)

        expected_images = 2 + (job.gallery_count or 0)  # hero + about + gallery_count
        total_images = len(image_statuses) or expected_images
        completed_images = sum(
            1 for d in image_statuses.values() if d.get("status") == "completed"
        )

        images_payload = {
            k: {
                "type": d.get("type", k),
                "status": d.get("status", "pending"),
                "url": d.get("url"),
                "local_path": d.get("local_path"),
                "prompt": d.get("prompt"),
                "aspect_ratio": d.get("aspect_ratio"),
                "error": d.get("error"),
                "downloaded_at": d.get("downloaded_at"),
            }
            for k, d in image_statuses.items()
        }

        return {
            "job_id": job.job_id,
            "status": job.status.value,
            "message": job.message,
            "expected_images": expected_images,
            "total_images": total_images,
            "completed_images": completed_images,
            "images": images_payload,
            "zip_path": job.zip_path,
            "created_at": job.created_at,
            "updated_at": job.updated_at,
            "error": job.error,
        }

    def fail_job(self, job_id: str, error: str):
        job_data = self.redis_client.get(self._job_key(job_id))
        if not job_data:
            raise ValueError(f"Job with ID {job_id} not found")

        job = JobStatusInfo.from_json(job_data.decode())

        if job:
            job.status = JobStatusType.FAILED
            job.error = error
            job.message = f"Failed: {error}"
            job.updated_at = datetime.utcnow()

            self.redis_client.set(
                self._job_key(job_id),
                job.to_json(),
            )

    def complete_job(self, job_id: str, zip_path: str = None):
        job_data = self.redis_client.get(self._job_key(job_id))
        if not job_data:
            raise ValueError(f"Job with ID {job_id} not found")

        job = JobStatusInfo.from_json(job_data.decode())

        if job:
            job.status = JobStatusType.COMPLETED
            job.zip_path = zip_path
            job.message = "All images generated and archived"
            job.updated_at = datetime.utcnow()

            self.redis_client.set(
                self._job_key(job_id),
                job.to_json(),
            )
