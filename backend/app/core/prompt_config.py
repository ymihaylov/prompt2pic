from dataclasses import dataclass
from typing import List


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
