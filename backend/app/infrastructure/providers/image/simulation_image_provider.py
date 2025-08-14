from app.infrastructure.providers.image.base_image_provider import ImageProvider


class SimulationImageProvider(ImageProvider):
    def generate_image(self, prompt: str, aspect_ratio: str = "1:1", **kwargs) -> str:
        return "https://static01.nyt.com/images/2024/05/01/multimedia/01dc-pandas-mwbq/01dc-pandas-mwbq-articleLarge.jpg?quality=75&auto=webp&disable=upscale"
