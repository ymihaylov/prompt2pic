from app.core.settings import settings
from app.infrastructure.providers.image.base_image_provider import ImageProvider
from app.infrastructure.providers.image.image_provider_type import ImageProviderType
from app.infrastructure.providers.image.openai_image_provider import OpenAIImageProvider
from app.infrastructure.providers.image.simulation_image_provider import (
    SimulationImageProvider,
)


class ImageProviderFactory:
    @staticmethod
    def create(
        provider_type: ImageProviderType = ImageProviderType.SIMULATION,
    ) -> ImageProvider:
        if provider_type == ImageProviderType.OPENAI:
            api_key = settings.openai_api_key
            return OpenAIImageProvider(api_key=api_key)
        elif provider_type == ImageProviderType.SIMULATION:
            return SimulationImageProvider()
        else:
            raise ValueError(f"Unsupported image provider: {provider_type}")
