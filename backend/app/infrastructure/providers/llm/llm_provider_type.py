from enum import Enum


class LLMProviderType(Enum):
    OPENAI = "openai"
    OLLAMA = "ollama"
    SIMULATION = "simulation"
