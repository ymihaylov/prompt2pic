"""
Worker configuration following industry best practices
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Redis Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Logging Configuration
LOG_LEVEL = os.getenv("WORKER_LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("WORKER_LOG_FILE")  # Optional log file path

# Task Configuration
TASK_TIME_LIMIT = int(os.getenv("TASK_TIME_LIMIT", "3600"))  # 1 hour default
TASK_SOFT_TIME_LIMIT = int(os.getenv("TASK_SOFT_TIME_LIMIT", "3000"))  # 50 minutes default

# Worker Configuration
WORKER_CONCURRENCY = int(os.getenv("WORKER_CONCURRENCY", "4"))
WORKER_PREFETCH_MULTIPLIER = int(os.getenv("WORKER_PREFETCH_MULTIPLIER", "1"))

# Celery Configuration
CELERY_CONFIG: Dict[str, Any] = {
    "broker": REDIS_URL,
    "backend": REDIS_URL,
    "task_serializer": "json",
    "accept_content": ["json"],
    "result_serializer": "json",
    "timezone": "UTC",
    "enable_utc": True,
    "task_time_limit": TASK_TIME_LIMIT,
    "task_soft_time_limit": TASK_SOFT_TIME_LIMIT,
    "worker_prefetch_multiplier": WORKER_PREFETCH_MULTIPLIER,
    "task_acks_late": True,
    "worker_disable_rate_limits": False,
    "task_reject_on_worker_lost": True,
    "result_expires": 86400,  # 24 hours
    "task_track_started": True,
    "task_send_sent_event": True,
    # Task routing
    "task_routes": {
        "image_generation.*": {"queue": "image_generation"},
    },
    # Default queue configuration
    "task_default_queue": "default",
    "task_default_exchange": "default",
    "task_default_exchange_type": "direct",
    "task_default_routing_key": "default",
}
