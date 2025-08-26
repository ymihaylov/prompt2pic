from abc import ABC, abstractmethod


class ImageProvider(ABC):
    @abstractmethod
    def generate_image(self, prompt: str, aspect_ratio: str = "1:1", **kwargs) -> bytes:
        pass
