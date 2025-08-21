#!/bin/bash
# Start Celery worker
cd "$(dirname "$0")/.."
celery -A app.worker.celery_worker worker --loglevel=info
