#!/bin/bash
# Start Celery worker with production settings

set -e  # Exit on error

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Default environment variables
export WORKER_LOG_LEVEL="${WORKER_LOG_LEVEL:-INFO}"
export WORKER_CONCURRENCY="${WORKER_CONCURRENCY:-4}"
export WORKER_PREFETCH_MULTIPLIER="${WORKER_PREFETCH_MULTIPLIER:-1}"

echo "Starting Celery worker..."
echo "Project root: $PROJECT_ROOT"
echo "Log level: $WORKER_LOG_LEVEL"
echo "Concurrency: $WORKER_CONCURRENCY"

# Start worker with optimized settings
exec celery -A app.worker.celery_worker worker \
  --loglevel="$WORKER_LOG_LEVEL" \
  --concurrency="$WORKER_CONCURRENCY" \
  --prefetch-multiplier="$WORKER_PREFETCH_MULTIPLIER" \
  --pool=prefork \
  --optimization=fair \
  --without-gossip \
  --without-mingle \
  --without-heartbeat
