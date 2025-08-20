from app.core.interfaces import ImageProvider


class ImageGeneratorService:
    """Service responsible for generating single images from prompts."""

    def generate_single_image(self, image_provider: ImageProvider, prompt: str, aspect_ratio: str = "1:1") -> str:
        """Generate a single image and return the URL."""
        try:
            url = image_provider.generate_image(prompt, aspect_ratio)
            return url
        except Exception as e:
            raise RuntimeError(f"Failed to generate image: {e}")
