from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ImageTask:
    image_type: str
    data: Dict[str, Any]
    base_filename: str
    message: str

    def to_dict(self) -> dict:
        return {
            "image_type": self.image_type,
            "data": self.data,
            "base_filename": self.base_filename,
            "message": self.message,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ImageTask":
        return cls(**data)
