import os
import uuid
import zipfile
from typing import List, Dict

import requests


class FileManagerService:
    """Service responsible for downloading images and creating archives."""

    def __init__(self, base_dir: str = "temp_images"):
        self.base_dir = base_dir

    def download_images(self, image_urls: List[Dict[str, str]]) -> List[str]:
        """Download images from URLs to local storage."""
        downloaded_files = []

        # Create temp directory
        os.makedirs(self.base_dir, exist_ok=True)

        for image_data in image_urls:
            try:
                url = image_data["url"]
                filename = image_data["filename"]
                filepath = os.path.join(self.base_dir, filename)

                # Download image
                response = requests.get(url)
                response.raise_for_status()

                # Save to file
                with open(filepath, "wb") as f:
                    f.write(response.content)

                downloaded_files.append(filepath)
                print(f"Downloaded: {filename}")

            except Exception as e:
                print(f"Failed to download {image_data['filename']}: {e}")

        return downloaded_files

    def create_zip_archive(self, file_paths: List[str]) -> str:
        """Create zip archive from downloaded images."""
        zip_filename = f"generated_images_{uuid.uuid4().hex[:8]}.zip"
        zip_path = os.path.join(self.base_dir, zip_filename)

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file_path in file_paths:
                # Add file to zip with just the filename (not full path)
                arcname = os.path.basename(file_path)
                zipf.write(file_path, arcname)
                print(f"Added to zip: {arcname}")

        return zip_path
