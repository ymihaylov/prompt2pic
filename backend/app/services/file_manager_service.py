import os
import zipfile
from typing import Tuple
from urllib.parse import urlparse

import requests


class FileManagerService:

    def __init__(self, base_dir: str = "generated_images"):
        self.base_dir = base_dir

    def setup_job_directory(self, job_id: str) -> str:
        job_dir = os.path.join(self.base_dir, job_id)
        os.makedirs(job_dir, exist_ok=True)

        return job_dir

    def _detect_file_extension(self, response: requests.Response, url: str) -> str:
        """Detect file extension from response headers or URL"""
        # First, check Content-Type header
        content_type = response.headers.get("content-type", "").lower()

        if "image/jpeg" in content_type or "image/jpg" in content_type:
            return ".jpg"
        elif "image/png" in content_type:
            return ".png"
        elif "image/webp" in content_type:
            return ".webp"
        elif "image/gif" in content_type:
            return ".gif"
        elif "image/bmp" in content_type:
            return ".bmp"
        elif "image/svg" in content_type:
            return ".svg"

        # Fallback: try to extract from URL
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()

        if path.endswith((".jpg", ".jpeg")):
            return ".jpg"
        elif path.endswith(".png"):
            return ".png"
        elif path.endswith(".webp"):
            return ".webp"
        elif path.endswith(".gif"):
            return ".gif"
        elif path.endswith(".bmp"):
            return ".bmp"
        elif path.endswith(".svg"):
            return ".svg"

        # Default fallback to .jpg if unable to detect
        return ".jpg"

    def download_single_image(
        self, url: str, job_id: str, base_filename: str
    ) -> Tuple[str, str]:
        """
        Download image and return (actual_filepath, actual_filename) with proper extension

        Args:
            url: Image URL to download
            job_id: Job ID for directory organization
            base_filename: Base filename without extension (e.g., 'hero', 'gallery_1')

        Returns:
            Tuple of (full_filepath, actual_filename_with_extension)
        """
        job_dir = self.setup_job_directory(job_id)

        response = requests.get(url)
        response.raise_for_status()

        # Detect the actual file extension
        extension = self._detect_file_extension(response, url)

        # Create filename with proper extension
        actual_filename = f"{base_filename}{extension}"
        filepath = os.path.join(job_dir, actual_filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        return filepath, actual_filename

    def create_zip_from_directory(self, job_id: str) -> str:
        job_dir = os.path.join(self.base_dir, job_id)
        zip_filename = f"generated_images_{job_id}.zip"
        zip_path = os.path.join(job_dir, zip_filename)

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for filename in os.listdir(job_dir):
                file_path = os.path.join(job_dir, filename)
                # Skip the zip file itself and only include image files
                if os.path.isfile(file_path) and not filename.endswith(".zip"):
                    zipf.write(file_path, filename)

        return zip_path
