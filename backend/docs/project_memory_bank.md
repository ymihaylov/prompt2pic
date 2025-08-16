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

## Database Architecture (Hybrid Approach)

### SQLite (Persistent History)
- **Purpose**: Long-term storage, job records, audit trail
- **Benefits**: Complex queries, analytics, reporting, durability
- **Schema**:
  ```sql
  CREATE TABLE jobs (
      id TEXT PRIMARY KEY,
      original_prompt TEXT NOT NULL,
      gallery_count INTEGER,
      llm_model TEXT,
      llm_response JSON,
      final_status TEXT,
      created_at TIMESTAMP,
      completed_at TIMESTAMP,
      error_message TEXT
  );

  CREATE TABLE generated_images (
      id TEXT PRIMARY KEY,
      job_id TEXT REFERENCES jobs(id),
      image_type TEXT, -- 'hero', 'about', 'gallery'
      prompt TEXT,
      file_path TEXT,
      file_size INTEGER,
      created_at TIMESTAMP
  );
  ```

### Redis (Real-time Status)
- **Purpose**: Fast reads/writes, real-time progress tracking
- **Benefits**: Sub-millisecond updates, pub/sub, TTL auto-cleanup
- **Data Structure**:
  ```python
  redis_key = f"job_progress:{job_id}"
  redis_data = {
      "status": "processing",
      "progress": 65,
      "current_step": "Generating gallery image 2/3",
      "eta_seconds": 45,
      "updated_at": "2025-01-01T12:05:30Z"
  }
  # TTL: 24 hours (auto-cleanup)
  ```

### Data Flow Design
```
Job Creation Flow:
1. API receives request
2. Create job record in SQLite (persistent)
3. Set initial status in Redis (fast access)
4. Return job_id to client

Progress Updates:
1. Update Redis with current progress (0-100%)
2. Frontend polls Redis for real-time updates
3. On completion: Update SQLite with final results

Status Queries:
1. GET /status/{job_id} → Read from Redis (fast)
2. GET /history/{job_id} → Read from SQLite (complete data)
```

## LLM Integration Strategy

### Prompt Engineering Flow
1. **Input**: User business description (≤300 chars) + gallery count
2. **Template**: Use `docs/temp_llm_prompt.md` with variable substitution
3. **Model**: OpenAI GPT-4o mini for reliability and speed
4. **Output**: Structured JSON with prompts for each image type

### LLM Prompt Template Structure
- Replace `{business_description}` with user input
- Replace `{gallery_count}` with requested number
- Expected JSON response:
  ```json
  {
    "hero": { "prompt": "...", "aspect": "16:9" },
    "about": { "prompt": "...", "aspect": "3:4" },
    "gallery": [
      { "prompt": "...", "aspect": "1:1" },
      { "prompt": "...", "aspect": "1:1" }
    ],
    "negative_prompt": "text, watermark, logo, trademark, blurry"
  }
  ```

## Implementation Dependencies

### Required Packages
```python
# requirements.txt additions
sqlalchemy==2.0.23      # SQLite ORM
redis==5.0.1            # Redis client
openai==1.3.0           # OpenAI API
alembic==1.13.1         # Database migrations
```

### Project Structure
```
app/
├── services/
│   ├── database_service.py     # SQLite operations
│   ├── redis_service.py        # Redis operations  
│   ├── llm_service.py          # OpenAI integration
│   └── image_generation_service.py  # Orchestrates everything
├── models/
│   ├── database.py             # SQLAlchemy models
│   └── redis_models.py         # Redis data structures
├── core/
│   └── config.py               # App configuration
```

### Configuration Settings
```python
# app/core/config.py
class Settings:
    sqlite_url = "sqlite:///./data/jobs.db"
    redis_url = "redis://localhost:6379"
    openai_api_key = "sk-..."
    job_progress_ttl = 86400  # 24 hours
```

## Benefits of Hybrid Architecture

1. **Performance**: Redis handles high-frequency status reads
2. **Reliability**: SQLite ensures no data loss
3. **Scalability**: Redis can handle thousands of concurrent status checks
4. **Analytics**: SQLite enables complex queries for insights
5. **Real-time**: Perfect for WebSocket updates or polling
6. **Cost-effective**: Both are lightweight and fast

## MVP Path

### Step 1 (Current)
✅ Sync FastAPI endpoint structure
✅ Basic request/response models
✅ Project structure with proper separation

### Step 2 (In Progress)
- Add SQLite + Redis integration
- Implement OpenAI LLM service
- Create job persistence and status tracking
- Synchronous image generation pipeline

### Step 3
Add job queue + async processing

### Step 4
Add WebSocket progress updates + frontend

### Step 5
Add cloud storage + ZIP downloads

### Step 6
Add local models + model selection