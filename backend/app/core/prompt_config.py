from dataclasses import dataclass
from typing import List, Optional

from app.core.interfaces import LLMProviderType, ImageProviderType


@dataclass
class ProviderConfig:
    llm_provider: str = LLMProviderType.SIMULATION
    image_provider: str = ImageProviderType.SIMULATION
    api_key: Optional[str] = None


@dataclass
class PromptConfig:
    name: str
    file_path: str
    required_variables: List[str]


PROMPT_CONFIGS = {
    "image_generation": PromptConfig(
        name="image_generation",
        file_path="app/prompts/llm_prompt.txt",
        required_variables=["business_description", "gallery_count"],
    )
}
