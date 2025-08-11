# Prompt2Pic — AI Image Generator

A full-stack application that turns natural language business descriptions into AI-generated images. Users describe their business in a chat interface, choose LLM and image models, and receive a generated image gallery they can download.

## Architecture Overview

```
prompt2pic/
├── backend/          # FastAPI + Celery Python service
└── frontend/         # React chat-based UI
```

**Backend** — FastAPI application backed by Celery for async image generation:
- LLM layer (OpenAI GPT or Ollama) reads the business description and produces enhanced image prompts
- Image layer (OpenAI DALL-E or simulation mode) generates images in parallel via Celery workers
- Job state is tracked in Redis; generated files are stored on disk and served as static files

**Frontend** — React SPA with a chat-style workflow:
- User enters a business description and selects LLM + image model
- A job is submitted and polled until completion
- Generated images are displayed in a gallery with download support

---

## Prerequisites

| Dependency | Minimum version | Notes |
|---|---|---|
| Python | 3.11+ | Backend runtime |
| Node.js | 14+ | Frontend dev server |
| Redis | 6+ | Job queue & result backend |
| Ollama | latest | Optional — for local LLM |
| OpenAI API key | — | Required for OpenAI providers |

---

## Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd prompt2pic
```

### 2. Backend setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set OPENAI_API_KEY (and optionally OLLAMA_LLM_BASE_URL)
```

Start Redis (must be running before the app):

```bash
redis-server
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
# API available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

Start the Celery worker (separate terminal, same venv):

```bash
celery -A app.celery_app worker --loglevel=info
```

### 3. Frontend setup

```bash
cd frontend

npm install
npm start
# App available at http://localhost:3000
```

The React dev server proxies `/api` requests to `http://localhost:8000`.

---

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in the values:

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | Yes* | — | OpenAI API key (*required for OpenAI providers) |
| `OLLAMA_LLM_BASE_URL` | No | `http://localhost:11434` | Ollama server URL |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Redis connection string |
| `REDIS_JOB_TTL` | No | `86400` | Job TTL in seconds |

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Health check / welcome |
| `GET` | `/health` | Service health status |
| `POST` | `/images/generate` | Submit an image generation job |
| `GET` | `/jobs/status/{job_id}` | Poll job status and retrieve results |
| `GET` | `/data/{job_id}/...` | Serve generated image files |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc API docs |

### Image generation request body

```json
{
  "business_description": "A cozy artisan coffee shop in the city centre",
  "llm_model": "gpt-4",
  "image_model": "openai",
  "gallery_count": 4
}
```

---

## LLM Providers

| Key | Description |
|---|---|
| `openai` | GPT-4 / GPT-3.5 via OpenAI API |
| `ollama` | Local models via Ollama (e.g. llama3, mistral) |
| `simulation` | Stub that returns canned prompts — no API key needed |

## Image Providers

| Key | Description |
|---|---|
| `openai` | DALL-E 3 via OpenAI Images API |
| `simulation` | Returns placeholder images — useful for development |

---

## Project Structure

```
backend/
├── app/
│   ├── api/                    # FastAPI routers and middleware
│   │   └── endpoints/          # home, health, images, jobs
│   ├── core/                   # Settings, logging, prompt config
│   ├── infrastructure/
│   │   ├── providers/
│   │   │   ├── llm/            # OpenAI, Ollama, Simulation LLM providers
│   │   │   └── image/          # OpenAI DALL-E, Simulation image providers
│   │   └── storage/            # Redis service, file storage
│   ├── models/
│   │   ├── domain/             # Job status, image status, image task
│   │   └── dto/                # Request/response schemas
│   ├── repositories/           # Job and image state in Redis
│   ├── services/
│   │   ├── jobs/               # Job lifecycle management
│   │   ├── images/             # Image processing pipeline
│   │   └── llm/                # LLM prompt processing
│   ├── worker/                 # Celery app, tasks, service container
│   ├── celery_app.py
│   ├── cli.py                  # CLI for direct image generation
│   ├── dependencies.py
│   └── main.py
├── requirements.txt
└── .env.example

frontend/
├── public/
└── src/
    ├── components/             # Header, Chat, Input, Gallery, Modal, ...
    ├── hooks/                  # useJobPolling
    ├── services/               # api.js (Axios client)
    └── styles/
```

---

## CLI Usage

Generate images directly without the web interface:

```bash
cd backend
source venv/bin/activate

python -m app.cli \
  --description "A modern tech startup office" \
  --llm-model openai \
  --image-model openai \
  --count 3
```

---

## Development Notes

- The simulation providers (LLM and image) require no API keys and are the default when `OPENAI_API_KEY` is not set. Use them for local development.
- Celery requires Redis to be running as both the broker and result backend.
- Generated images are stored under `backend/data/<job_id>/` and served as static files via FastAPI's `StaticFiles` mount.
- The frontend proxies all requests to the backend via the `"proxy"` field in `package.json`.
