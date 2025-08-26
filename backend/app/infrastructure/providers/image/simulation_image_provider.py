import base64

from app.infrastructure.providers.image.base_image_provider import ImageProvider

# Minimal 1×1 gray PNG — valid image bytes for simulation without network calls
_PLACEHOLDER_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVQI12NgAAAAAgAB4iG8MwAAAABJRU5ErkJggg=="
)


class SimulationImageProvider(ImageProvider):
    def generate_image(self, prompt: str, aspect_ratio: str = "1:1", **kwargs) -> bytes:
        return _PLACEHOLDER_PNG
