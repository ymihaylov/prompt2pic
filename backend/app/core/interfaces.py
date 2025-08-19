from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any


class LLMProvider(ABC):
    @abstractmethod
    def generate_prompts(self, populated_prompt: str) -> Dict[str, Any]:
        pass


class ImageProvider(ABC):
    @abstractmethod
    def generate_image(self, prompt: str, aspect_ratio: str = "1:1", **kwargs) -> str:
        pass


class LLMProviderType(Enum):
    OPENAI = "openai"
    SIMULATION = "simulation"


class ImageProviderType(Enum):
    OPENAI = "openai"
    SIMULATION = "simulation"
