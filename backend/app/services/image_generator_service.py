from typing import List, Dict, Any

from app.core.interfaces import ImageProvider


class ImageGeneratorService:
    """Service responsible for generating multiple images from LLM response."""

    def generate_all_images(self, image_provider: ImageProvider, llm_response: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate all images from LLM response and collect URLs."""
        image_urls = []

        # Generate hero image
        if "hero" in llm_response:
            hero_data = llm_response["hero"]
            print(f"Generating hero image...")
            hero_url = image_provider.generate_image(
                hero_data["prompt"], hero_data["aspect"]
            )
            image_urls.append({"type": "hero", "url": hero_url, "filename": "hero.png"})

        # Generate about image
        if "about" in llm_response:
            about_data = llm_response["about"]
            print(f"Generating about image...")
            about_url = image_provider.generate_image(
                about_data["prompt"], about_data["aspect"]
            )
            image_urls.append(
                {"type": "about", "url": about_url, "filename": "about.png"}
            )

        # Generate gallery images
        if "gallery" in llm_response:
            for i, gallery_item in enumerate(llm_response["gallery"]):
                print(f"Generating gallery image {i+1}...")
                gallery_url = image_provider.generate_image(
                    gallery_item["prompt"], gallery_item["aspect"]
                )
                image_urls.append(
                    {
                        "type": "gallery",
                        "url": gallery_url,
                        "filename": f"gallery_{i+1}.png",
                    }
                )

        return image_urls
