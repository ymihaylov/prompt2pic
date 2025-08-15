from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class ImageStatusType(Enum):
    PENDING = "pending"
    GENERATING = "generating"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ImageStatusInfo:
    type: str
    status: ImageStatusType = ImageStatusType.PENDING
    url: Optional[str] = None
    local_path: Optional[str] = None
    filename: Optional[str] = None
    prompt: Optional[str] = None
    aspect_ratio: Optional[str] = None
    error: Optional[str] = None
    downloaded_at: Optional[datetime] = None
