from openai import OpenAI
import logging

from app.infrastructure.providers.image.base_image_provider import ImageProvider


class OpenAIImageProvider(ImageProvider):
    def __init__(self, api_key: str, model: str = "dall-e-3"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_image(self, prompt: str, aspect_ratio: str = "1:1", **kwargs) -> str:
        try:
            size_map = {
                "1:1": "1024x1024",
                "16:9": "1792x1024",
                "3:4": "1024x1792",
            }
            size = size_map.get(aspect_ratio, "1024x1024")

            response = self.client.images.generate(
                model=self.model, prompt=prompt, size=size, n=1
            )

            if not response.data[0] or not response.data[0].url:
                raise Exception("Generation failed")

            return response.data[0].url
        except Exception as e:
            logging.getLogger(__name__).exception("Image generation failed")
            raise RuntimeError(f"Image generation failed: {e}")
