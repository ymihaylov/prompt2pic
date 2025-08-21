"""
Celery application configuration following industry best practices
"""
from celery import Celery
from celery.signals import worker_process_init

from app.worker.config import CELERY_CONFIG
from app.worker.logging_config import setup_worker_logging, LOG_LEVEL, LOG_FILE

# Create Celery app with proper naming
celery_app = Celery("prompt2pic-workers")

# Apply configuration
celery_app.conf.update(CELERY_CONFIG)

# Auto-discover tasks in worker module
celery_app.autodiscover_tasks(["app.worker"])


@worker_process_init.connect
def init_worker(**kwargs):
    """Initialize worker process with logging and other setup"""
    setup_worker_logging(LOG_LEVEL, LOG_FILE)
    # Add any other worker initialization here
