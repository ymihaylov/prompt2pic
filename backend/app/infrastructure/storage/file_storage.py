import os
import zipfile
from typing import Tuple
from urllib.parse import urlparse

import requests


class FileStorage:

    def __init__(self, base_dir: str = "data"):
        self.base_dir = base_dir

    def setup_job_directory(self, job_id: str) -> str:
        job_dir = os.path.join(self.base_dir, job_id)
        os.makedirs(job_dir, exist_ok=True)

        return job_dir

    def save_image_bytes(
        self, data: bytes, job_id: str, base_filename: str, extension: str = ".png"
    ) -> Tuple[str, str]:
        job_dir = self.setup_job_directory(job_id)
        actual_filename = f"{base_filename}{extension}"
        filepath = os.path.join(job_dir, actual_filename)

        with open(filepath, "wb") as f:
            f.write(data)

        return filepath, actual_filename

    def download_single_image(
        self, url: str, job_id: str, base_filename: str
    ) -> Tuple[str, str]:
        job_dir = self.setup_job_directory(job_id)

        response = requests.get(url)
        response.raise_for_status()

        extension = self._detect_file_extension(response, url)

        actual_filename = f"{base_filename}{extension}"
        filepath = os.path.join(job_dir, actual_filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        return filepath, actual_filename

    def save_prompt(
        self, prompt: str, job_id: str, base_filename: str
    ) -> Tuple[str, str]:
        job_dir = self.setup_job_directory(job_id)

        prompt_filename = f"{base_filename}_prompt.txt"
        filepath = os.path.join(job_dir, prompt_filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(prompt)

        return filepath, prompt_filename

    def create_zip_from_directory(self, job_id: str) -> str:
        job_dir = os.path.join(self.base_dir, job_id)
        zip_filename = f"data_{job_id}.zip"
        zip_path = os.path.join(job_dir, zip_filename)

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for filename in os.listdir(job_dir):
                file_path = os.path.join(job_dir, filename)

                if os.path.isfile(file_path) and not filename.endswith(".zip"):
                    zipf.write(file_path, filename)

        return zip_path

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
