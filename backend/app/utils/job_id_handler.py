import secrets


class JobIdHandler:

    length = 12

    def generate(self) -> str:
        """
        Generate a cryptographically secure, URL-safe job ID.
        """
        return secrets.token_urlsafe(self.length)
