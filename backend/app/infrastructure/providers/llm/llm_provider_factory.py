from app.core.settings import settings
from app.infrastructure.providers.llm.base_llm_provider import BaseLLMProvider
from app.infrastructure.providers.llm.llm_provider_type import LLMProviderType
from app.infrastructure.providers.llm.ollama_llm_provider import OllamaLLMProvider
from app.infrastructure.providers.llm.openai_llm_provider import OpenAILLMProviderBase
from app.infrastructure.providers.llm.simulation_llm_provider import (
    SimulationProviderBase,
)


class LLMProviderFactory:
    @staticmethod
    def create(
        provider_type: LLMProviderType = LLMProviderType.SIMULATION,
    ) -> BaseLLMProvider:

        if provider_type == LLMProviderType.OPENAI:
            api_key = settings.openai_api_key

            return OpenAILLMProviderBase(api_key=api_key)
        elif provider_type == LLMProviderType.OLLAMA:
            return OllamaLLMProvider()
        elif provider_type == LLMProviderType.SIMULATION:
            return SimulationProviderBase()
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_type}")
