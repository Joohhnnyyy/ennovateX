"""Configuration Settings

This module contains all configuration settings for the EnnovateX AI platform,
including environment variables, API keys, model paths, and application settings.
"""

import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application settings
    APP_NAME: str = "EnnovateX AI Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        env="ALLOWED_ORIGINS"
    )
    
    # API Keys
    HUGGINGFACE_API_KEY: Optional[str] = Field(default=None, env="HUGGINGFACE_API_KEY")
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    
    # Model settings
    MODEL_CACHE_DIR: str = Field(default="./models", env="MODEL_CACHE_DIR")
    MAX_MODEL_MEMORY: int = Field(default=4096, env="MAX_MODEL_MEMORY")  # MB
    DEVICE: str = Field(default="auto", env="DEVICE")  # auto, cpu, cuda, mps
    
    # Text model settings
    TEXT_SUMMARIZER_MODEL: str = Field(
        default="facebook/bart-large-cnn",
        env="TEXT_SUMMARIZER_MODEL"
    )
    TEXT_SUMMARIZER_LORA: Optional[str] = Field(
        default=None,
        env="TEXT_SUMMARIZER_LORA"
    )
    
    # Image model settings
    IMAGE_CAPTION_MODEL: str = Field(
        default="Salesforce/blip-image-captioning-base",
        env="IMAGE_CAPTION_MODEL"
    )
    IMAGE_CAPTION_LORA: Optional[str] = Field(
        default=None,
        env="IMAGE_CAPTION_LORA"
    )
    
    # Audio model settings
    AUDIO_ASR_MODEL: str = Field(
        default="openai/whisper-base",
        env="AUDIO_ASR_MODEL"
    )
    
    # File upload settings
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = Field(
        default=["image/jpeg", "image/png", "image/webp", "image/bmp"],
        env="ALLOWED_IMAGE_TYPES"
    )
    ALLOWED_AUDIO_TYPES: List[str] = Field(
        default=["audio/wav", "audio/mp3", "audio/flac", "audio/ogg"],
        env="ALLOWED_AUDIO_TYPES"
    )
    
    # Processing settings
    MAX_TEXT_LENGTH: int = Field(default=10000, env="MAX_TEXT_LENGTH")
    MAX_SUMMARY_LENGTH: int = Field(default=500, env="MAX_SUMMARY_LENGTH")
    MAX_CAPTION_LENGTH: int = Field(default=200, env="MAX_CAPTION_LENGTH")
    
    # Rate limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=3600, env="RATE_LIMIT_WINDOW")  # seconds
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: Optional[str] = Field(default=None, env="LOG_FILE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

# Global settings instance
settings = get_settings()

# Model configurations
MODEL_CONFIGS = {
    "text_summarizer": {
        "model_name": settings.TEXT_SUMMARIZER_MODEL,
        "lora_adapter": settings.TEXT_SUMMARIZER_LORA,
        "max_length": settings.MAX_SUMMARY_LENGTH,
        "task": "summarization"
    },
    "image_captioner": {
        "model_name": settings.IMAGE_CAPTION_MODEL,
        "lora_adapter": settings.IMAGE_CAPTION_LORA,
        "max_length": settings.MAX_CAPTION_LENGTH,
        "task": "image-to-text"
    },
    "audio_asr": {
        "model_name": settings.AUDIO_ASR_MODEL,
        "task": "automatic-speech-recognition"
    }
}