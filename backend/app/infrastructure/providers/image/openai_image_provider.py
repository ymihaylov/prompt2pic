import base64
import logging

from openai import OpenAI

from app.infrastructure.providers.image.base_image_provider import ImageProvider


class OpenAIImageProvider(ImageProvider):
    def __init__(self, api_key: str, model: str = "gpt-image-1"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_image(self, prompt: str, aspect_ratio: str = "1:1", **kwargs) -> bytes:
        try:
            size_map = {
                "1:1": "1024x1024",
                "16:9": "1536x1024",
                "3:4": "1024x1536",
            }
            size = size_map.get(aspect_ratio, "1024x1024")

            response = self.client.images.generate(
                model=self.model,
                prompt=prompt,
                size=size,
                n=1,
            )

            b64 = response.data[0].b64_json
            if not b64:
                raise ValueError("No image data returned from API")

            return base64.b64decode(b64)
        except Exception as e:
            logging.getLogger(__name__).exception("Image generation failed")
            raise RuntimeError(f"Image generation failed: {e}")
