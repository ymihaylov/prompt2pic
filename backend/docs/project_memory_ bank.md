# Project Memory Bank: AI Website Image Generator

## Assignment Summary

Build a web service that:

1. Takes user text input (≤300 chars) + number of gallery images (0–15)
2. Uses an LLM to expand into detailed prompts for different website images
3. Uses an image generation model (local or hosted) to create:
   - 1 panoramic hero image (16:9, max 1024px)
   - 1 portrait about-us image (3:4, max 1024px)
   - 0–15 square gallery images (1:1, max 1024px)
4. Returns download links + a bulk ZIP with images + prompts

## Tech Requirements

### Core Technologies
- **Python** (FastAPI for API)
- **Minimal frontend**: form + live status + image gallery
- Handle **concurrent requests** gracefully (queue, async, worker)
- Support both **local** and **cloud-hosted models**

### Plus Points
- Local models (Ollama for LLM, Stable Diffusion for images)
- Model selection per request
- CLI + batch processing
- Logging, monitoring, health endpoints
- Cloud storage (S3/GCS)

## Planned Architecture

### Frontend
- Simple HTML/JS React page
- Form → API → WebSocket for status

### API Endpoints
- /generate-images/	Main image generation job (POST)
- /job-status/{job_id}/	Job status polling (GET)
- /download/image/{image_id}/	Single image download (GET)
- /download/job/{job_id}/	Bulk ZIP download (GET)
- /models/	List/select image/prompt models (GET)
- /health/	Service health/status (GET)

### Workers
- Start with sync background tasks (simple)
- Later: Redis queue (RQ or Celery) for scalability

### Models
- **LLM**: Ollama local, or OpenAI as fallback
- **Image gen**: diffusers/Stable Diffusion local, or hosted API fallback

### Storage
- **Dev**: local `./data/{job_id}`
- **Prod**: S3 with pre-signed URLs

## Data Flow

1. User input → API
2. API calls LLM → build structured prompts
3. Generate hero, about, gallery images via image model
4. Save files, build ZIP, expose URLs
5. Frontend shows progress + images + download link

## Best Practices

- Queue + semaphore for GPU tasks
- Structured logging (JSON, job_id)
- `GET /healthz` (fast), `/readyz` (GPU + redis)
- Prometheus metrics
- Idempotency keys to avoid duplicate jobs
- Timeout + retry per image

## MVP Path

### Step 1
Sync FastAPI endpoint → LLM (any) → image model (any) → return direct images/links

### Step 2
Add job queue + status API

### Step 3
Add WS progress updates + frontend

### Step 4
Add cloud storage + ZIP

### Step 5
Add local models + selection