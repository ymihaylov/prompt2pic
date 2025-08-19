"""
Service for generating secure, unique request IDs.
"""

import secrets


class RequestIdService:

    length = 12

    def generate(self) -> str:
        """
        Generate a cryptographically secure, URL-safe request ID.

        Returns:
            str: Secure request ID (e.g., "a1B2c3D4e5F6g7H8")
        """
        return secrets.token_urlsafe(self.length)

    def validate(self, request_id: str) -> bool:
        """
        Validate if a string looks like a valid request ID.

        Args:
            request_id: String to validate

        Returns:
            bool: True if valid format, False otherwise
        """
        if not request_id:
            return False

        # Check for prefix format
        if "_" in request_id:
            parts = request_id.split("_", 1)
            if len(parts) != 2:
                return False
            prefix, token = parts
            # Validate prefix is alphanumeric
            if not prefix.isalnum():
                return False
            request_id = token

        # Validate token part (URL-safe base64 characters)
        valid_chars = set(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        )
        return all(c in valid_chars for c in request_id) and len(request_id) >= 8
