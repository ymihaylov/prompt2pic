"""
Ollama LLM provider implementation.
"""

import json

import httpx

from app.core.settings import settings
from app.infrastructure.providers.llm.base_llm_provider import BaseLLMProvider


class OllamaLLMProvider(BaseLLMProvider):
    def __init__(self, model: str = "llama3"):
        self.model = model
        self.base_url = settings.ollama_llm_base_url

    def generate_prompt(self, prompt: str) -> dict:
        payload = {"model": self.model, "prompt": prompt, "stream": False}

        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}/api/generate", json=payload, timeout=60.0
            )
            response.raise_for_status()

            result = response.json()
            raw_response = result["response"]

            start = raw_response.find("{")
            end = raw_response.rfind("}")

            data = json.loads(raw_response[start : end + 1])

            return data
