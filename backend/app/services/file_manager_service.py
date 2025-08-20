import os
import zipfile

import requests


class FileManagerService:

    def __init__(self, base_dir: str = "generated_images"):
        self.base_dir = base_dir

    def setup_request_directory(self, request_id: str) -> str:
        request_dir = os.path.join(self.base_dir, request_id)
        os.makedirs(request_dir, exist_ok=True)

        return request_dir

    def download_single_image(self, url: str, request_id: str, filename: str) -> str:
        request_dir = self.setup_request_directory(request_id)
        filepath = os.path.join(request_dir, filename)

        response = requests.get(url)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            f.write(response.content)

        return filepath

    def create_zip_from_directory(self, request_id: str) -> str:
        request_dir = os.path.join(self.base_dir, request_id)
        zip_filename = f"generated_images_{request_id}.zip"
        zip_path = os.path.join(request_dir, zip_filename)

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for filename in os.listdir(request_dir):
                file_path = os.path.join(request_dir, filename)
                # Skip the zip file itself and only include image files
                if os.path.isfile(file_path) and not filename.endswith(".zip"):
                    zipf.write(file_path, filename)
                    print(f"Added to zip: {filename}")

        return zip_path
