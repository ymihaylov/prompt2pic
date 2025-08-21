"""
Logging configuration for workers
"""

import logging
import sys
from pathlib import Path


def setup_worker_logging(log_level: str = "INFO", log_file: str = None) -> None:
    """
    Setup logging configuration for workers

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
    """

    # Create logs directory if needed
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    # Configure logging format
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - [%(process)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Setup handlers
    handlers = []

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)

    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()), handlers=handlers, force=True
    )

    # Configure specific loggers
    logging.getLogger("app.worker").setLevel(getattr(logging, log_level.upper()))
    logging.getLogger("celery").setLevel(logging.WARNING)  # Reduce celery noise
