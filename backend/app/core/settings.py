from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str
    redis_job_ttl: int = 86400
    openai_api_key: str
    ollama_llm_base_url: str

    class Config:
        env_file = ".env"


settings = Settings()
