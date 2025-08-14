from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_prompt(self, populated_prompt: str) -> Dict[str, Any]:
        pass
