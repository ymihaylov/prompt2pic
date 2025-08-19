from typing import Dict, Any

from app.core.interfaces import ImageProvider


class ImageGeneratorService:
    """Service responsible for generating multiple images from LLM response."""

    def generate_and_download_images(
        self,
        image_provider: ImageProvider,
        llm_response: Dict[str, Any],
        request_id: str,
        file_manager,
    ) -> None:
        """Generate each image and download it immediately."""

        # Process hero image
        if "hero" in llm_response:
            hero_data = llm_response["hero"]
            print(f"Generating hero image...")
            hero_url = image_provider.generate_image(
                hero_data["prompt"], hero_data["aspect"]
            )
            print(f"Downloading hero image...")
            file_manager.download_single_image(hero_url, request_id, "hero.png")

        # Process about image
        if "about" in llm_response:
            about_data = llm_response["about"]
            print(f"Generating about image...")
            about_url = image_provider.generate_image(
                about_data["prompt"], about_data["aspect"]
            )
            print(f"Downloading about image...")
            file_manager.download_single_image(about_url, request_id, "about.png")

        # Process gallery images
        if "gallery" in llm_response:
            for i, gallery_item in enumerate(llm_response["gallery"]):
                print(f"Generating gallery image {i+1}...")
                gallery_url = image_provider.generate_image(
                    gallery_item["prompt"], gallery_item["aspect"]
                )
                print(f"Downloading gallery image {i+1}...")
                file_manager.download_single_image(
                    gallery_url, request_id, f"gallery_{i+1}.png"
                )
