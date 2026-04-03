"""
Configuration management for AI Agency Suite
SECURITY: All sensitive values are loaded from environment variables
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Core
    APP_NAME: str = Field(default="AI Agency Suite")
    DEBUG: bool = Field(default=True)
    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production")
    
    # Ollama (Local AI)
    OLLAMA_HOST: str = Field(default="http://localhost:11434")
    OLLAMA_MODEL: str = Field(default="llama3.1")
    OLLAMA_TIMEOUT: int = Field(default=120)
    
    # OpenRouter (Optional Cloud AI - Free tier available)
    OPENROUTER_API_KEY: Optional[str] = Field(default=None)
    OPENROUTER_MODEL: str = Field(default="meta-llama/llama-3.1-8b-instruct:free")
    
    # Database
    DATABASE_URL: str = Field(default="sqlite:///./ai_agency.db")
    CHROMA_PERSIST_DIR: str = Field(default="./chroma_db")
    
    # API
    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)
    API_KEY: Optional[str] = Field(default=None)
    
    # Instagram (Optional)
    INSTAGRAM_ACCESS_TOKEN: Optional[str] = Field(default=None)
    INSTAGRAM_APP_ID: Optional[str] = Field(default=None)
    INSTAGRAM_APP_SECRET: Optional[str] = Field(default=None)
    INSTAGRAM_VERIFY_TOKEN: Optional[str] = Field(default=None)
    
    # YouTube (Optional)
    YOUTUBE_API_KEY: Optional[str] = Field(default=None)
    YOUTUBE_CLIENT_ID: Optional[str] = Field(default=None)
    YOUTUBE_CLIENT_SECRET: Optional[str] = Field(default=None)
    
    # Facebook (Optional)
    FACEBOOK_ACCESS_TOKEN: Optional[str] = Field(default=None)
    FACEBOOK_PAGE_ID: Optional[str] = Field(default=None)
    
    # Text-to-Speech
    TTS_ENGINE: str = Field(default="gtts")  # gtts or pyttsx3
    TTS_LANGUAGE: str = Field(default="en")
    
    # Video
    VIDEO_OUTPUT_DIR: str = Field(default="./videos")
    THUMBNAIL_OUTPUT_DIR: str = Field(default="./thumbnails")
    VIDEO_RESOLUTION: str = Field(default="1080x1920")
    VIDEO_FPS: int = Field(default=30)
    
    # Scheduler
    SCHEDULER_ENABLED: bool = Field(default=True)
    SCHEDULER_TIMEZONE: str = Field(default="America/New_York")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: str = Field(default="./logs/app.log")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Create necessary directories
def create_directories():
    """Create required directories if they don't exist"""
    dirs = [
        settings.VIDEO_OUTPUT_DIR,
        settings.THUMBNAIL_OUTPUT_DIR,
        settings.CHROMA_PERSIST_DIR,
        os.path.dirname(settings.LOG_FILE),
        "./uploads",
        "./temp_videos",
    ]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)


# Initialize directories on import
create_directories()
