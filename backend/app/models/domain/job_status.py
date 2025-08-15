import json
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Optional


class JobStatusType(Enum):
    INIT = "init"
    GENERATING_PROMPT = "generating_prompt"
    GENERATING_IMAGES = "generating_images"
    CREATING_ZIP = "creating_zip"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class JobStatusInfo:
    job_id: str
    status: JobStatusType = JobStatusType.INIT
    message: str = ""
    prompt: str = ""
    llm_model: str = ""
    image_model: str = ""
    gallery_count: int = 0
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

        if data.get("created_at"):
            data["created_at"] = data["created_at"].isoformat()
        if data.get("updated_at"):
            data["updated_at"] = data["updated_at"].isoformat()

        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> "JobStatusInfo":
        data = json.loads(json_str)
        data["status"] = JobStatusType(data["status"])

        if data.get("created_at"):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])

        return cls(**data)
