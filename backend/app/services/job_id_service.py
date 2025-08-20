"""
Service for generating secure, unique job IDs.
"""

import secrets


class JobIdService:

    length = 12

    def generate(self) -> str:
        """
        Generate a cryptographically secure, URL-safe job ID.

        Returns:
            str: Secure job ID (e.g., "a1B2c3D4e5F6g7H8")
        """
        return secrets.token_urlsafe(self.length)

    def validate(self, job_id: str) -> bool:
        """
        Validate if a string looks like a valid job ID.

        Args:
            job_id: String to validate

        Returns:
            bool: True if valid format, False otherwise
        """
        if not job_id:
            return False

        # Check for prefix format
        if "_" in job_id:
            parts = job_id.split("_", 1)
            if len(parts) != 2:
                return False
            prefix, token = parts
            # Validate prefix is alphanumeric
            if not prefix.isalnum():
                return False
            job_id = token

        # Validate token part (URL-safe base64 characters)
        valid_chars = set(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        )
        return all(c in valid_chars for c in job_id) and len(job_id) >= 8
