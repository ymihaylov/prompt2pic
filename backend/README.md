# Prompt2Pic FastAPI Project

A simple FastAPI application with basic endpoints.

## Quick Start

### 1. Activate your virtual environment
```bash
source venv/bin/activate
```

### 2. Install dependencies (if not already installed)
```bash
pip install -r requirements.txt
```

### 3. Run the server
```bash
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

## Available Endpoints

- `GET /` - Returns "Hello World" message
- `GET /hello/{name}` - Returns personalized greeting
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## Example Usage

```bash
# Basic hello world
curl http://localhost:8000/

# Personalized greeting
curl http://localhost:8000/hello/John

# Health check
curl http://localhost:8000/health
```
