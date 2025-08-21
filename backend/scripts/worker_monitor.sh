#!/bin/bash
# Monitor Celery workers and tasks

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "=== Celery Worker Status ==="
celery -A app.worker.celery_worker inspect active

echo -e "\n=== Worker Stats ==="
celery -A app.worker.celery_worker inspect stats

echo -e "\n=== Registered Tasks ==="
celery -A app.worker.celery_worker inspect registered

echo -e "\n=== Queue Status ==="
celery -A app.worker.celery_worker inspect active_queues
