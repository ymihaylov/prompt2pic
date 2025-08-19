import os

from app.core.interfaces import (
    LLMProvider,
    ImageProvider,
    LLMProviderType,
    ImageProviderType,
)
from app.services.providers.llm_simulation_provider import LLMSimulationProvider
from app.services.providers.openai_image_provider import OpenAIImageProvider
from app.services.providers.openai_llm_provider import OpenAILLMProvider


class LLMProviderFactory:
    @staticmethod
    def create(
        provider_type: LLMProviderType = LLMProviderType.SIMULATION,
    ) -> LLMProvider:

        if provider_type == LLMProviderType.OPENAI:
            api_key = os.getenv("OPENAI_API_KEY")
            return OpenAILLMProvider(api_key=api_key)
        elif provider_type == LLMProviderType.SIMULATION:
            return LLMSimulationProvider()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_type}")


class ImageProviderFactory:
    @staticmethod
    def create(provider_type: str = ImageProviderType) -> ImageProvider:
        if provider_type == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            return OpenAIImageProvider(api_key=api_key)
        elif provider_type == ImageProviderType.SIMULATION:
            return LLMSimulationProvider()
        else:
            raise ValueError(f"Unsupported image provider: {provider_type}")


class SimulationProviderFactory:
    @staticmethod
    def create(provider_type: str = "mock") -> LLMSimulationProvider:
        if provider_type == "mock":
            return MockSimulationProvider()
        else:
            raise ValueError(f"Unsupported simulation provider: {provider_type}")
