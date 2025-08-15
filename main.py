from fastapi import FastAPI

# Create FastAPI instance
app = FastAPI(title="Prompt2Pic API", description="A simple FastAPI application", version="1.0.0")

# Basic hello world endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# Additional endpoint with path parameter
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
