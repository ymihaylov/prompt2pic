#!/usr/bin/env python3
"""
Celery worker configuration
"""
from app.celery_app import celery_app

# This makes the app discoverable
app = celery_app

if __name__ == "__main__":
    celery_app.start()
