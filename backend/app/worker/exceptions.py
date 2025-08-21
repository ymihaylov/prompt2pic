"""
Worker-specific exceptions
"""


class WorkerError(Exception):
    """Base exception for worker errors"""
    pass


class TaskValidationError(WorkerError):
    """Raised when task input validation fails"""
    pass


class ServiceInitializationError(WorkerError):
    """Raised when service initialization fails"""
    pass


class ImageGenerationTaskError(WorkerError):
    """Raised when image generation task fails"""
    pass
