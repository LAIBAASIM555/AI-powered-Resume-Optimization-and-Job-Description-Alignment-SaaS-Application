"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "AI Resume Optimizer"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "default-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # PostgreSQL Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password123"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "resume_optimizer"
    DATABASE_URL: str = None  # Will be constructed if not provided
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "docx"]
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    @property
    def database_url(self) -> str:
        """Construct PostgreSQL database URL"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins as a list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Create upload directory if not exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

