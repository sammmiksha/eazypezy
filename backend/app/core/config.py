"""Core application configuration."""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "EasyPezy Product Finder"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./easypezy.db"  # Fallback to local SQLite if Postgres not connected
    POSTGRES_SERVER: Optional[str] = "localhost"
    POSTGRES_USER: Optional[str] = "postgres"
    POSTGRES_PASSWORD: Optional[str] = "postgres"
    POSTGRES_DB: Optional[str] = "easypezy"
    
    # LLM keys (optional, fallback parser will activate if not set)
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    # Optional licensed product-search provider. When unset the application uses
    # its transparent demo catalog; it never silently scrapes retailer pages.
    SERPAPI_API_KEY: Optional[str] = None
    SERPAPI_ENDPOINT: str = "https://serpapi.com/search.json"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
