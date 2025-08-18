import json
from datetime import datetime
from typing import Dict

from app.infrastructure.storage.redis_service import RedisService
from app.models.domain.image_status import ImageStatusType
from app.models.dto.llm_image_response import LLMImageResponse


class ImageRepository:
    def __init__(self, redis_service: RedisService):
        self.redis_client = redis_service.get_client()
        self.image_prefix = "img:"
        self.job_ttl = 86400

    def set_image_status(
        self,
        job_id: str,
        image_key: str,
        status: ImageStatusType,
        **kwargs,
    ):
        redis_key = self._image_key(job_id, image_key)

        update_data = {
            "status": status.value,
            "updated_at": datetime.utcnow().isoformat(),
        }

        for key, value in kwargs.items():
            if value is not None:
                update_data[key] = (
                    value if isinstance(value, str) else json.dumps(value)
                )

        self.redis_client.hmset(redis_key, update_data)
        self.redis_client.expire(redis_key, self.job_ttl)

    def get_all_image_statuses(self, job_id: str) -> Dict[str, Dict]:
        pattern = f"{self.image_prefix}{job_id}:*"
        keys = self.redis_client.keys(pattern)

        if not keys:
            return {}

        statuses = {}

        for key in keys:
            data = self.redis_client.hgetall(key)

            if data:
                image_key = key.decode().split(":")[-1]
                statuses[image_key] = {k.decode(): v.decode() for k, v in data.items()}

        return statuses

    def update_image_generating(self, job_id: str, image_key: str) -> bool:
        self.set_image_status(
            job_id,
            image_key,
            ImageStatusType.GENERATING,
        )
        return True

    def update_image_completed(
        self, job_id: str, image_key: str, url: str, local_path: str
    ) -> bool:
        self.set_image_status(
            job_id,
            image_key,
            ImageStatusType.COMPLETED,
            url=url,
            local_path=local_path,
            downloaded_at=datetime.utcnow().isoformat(),
        )
        return True

    def update_image_failed(self, job_id: str, image_key: str, error: str) -> bool:
        self.set_image_status(job_id, image_key, ImageStatusType.FAILED, error=error)

        return True

    def setup_image_placeholders(self, job_id: str, llm_response: LLMImageResponse):
        if llm_response.hero:
            self.set_image_status(
                job_id,
                "hero",
                ImageStatusType.PENDING,
                type="hero",
                prompt=llm_response.hero.prompt,
                aspect_ratio=llm_response.hero.aspect,
                filename="hero",
            )

        if llm_response.about:
            self.set_image_status(
                job_id,
                "about",
                ImageStatusType.PENDING,
                type="about",
                prompt=llm_response.about.prompt,
                aspect_ratio=llm_response.about.aspect,
                filename="about",
            )

        for i, gallery_item in enumerate(llm_response.gallery):
            key = f"gallery_{i+1}"
            self.set_image_status(
                job_id,
                key,
                ImageStatusType.PENDING,
                type=key,
                prompt=gallery_item.prompt,
                aspect_ratio=gallery_item.aspect,
                filename=f"gallery_{i+1}",
            )

    def _image_key(self, job_id: str, image_key: str) -> str:
        return f"{self.image_prefix}{job_id}:{image_key}"
