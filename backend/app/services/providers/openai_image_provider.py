from openai import OpenAI
from app.core.interfaces import ImageProvider


class OpenAIImageProvider(ImageProvider):
    def __init__(self, api_key: str, model: str = "dall-e-3"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_image(self, prompt: str, aspect_ratio: str = "1:1", **kwargs) -> dict:
        try:
            size_map = {"1:1": "1024x1024", "16:9": "1792x1024", "3:4": "1024x1792"}
            size = size_map.get(aspect_ratio, "1024x1024")
            
            response = self.client.images.generate(
                model=self.model, 
                prompt=prompt, 
                size=size, 
                n=1
            )
            
            return {
                "url": response.data[0].url,
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "size": size,
                "model": self.model,
            }
            
        except Exception as e:
            raise RuntimeError(f"Image generation failed: {e}")
