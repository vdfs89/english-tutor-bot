"""LinguaFlow Configuration Management.

This module provides centralized configuration for the LinguaFlow application.
It supports multiple environments (development, staging, production) via environment variables.
"""

import logging
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application Info
    app_name: str = "LinguaFlow"
    app_version: str = "0.1.0"
    debug: bool = False

    # Environment
    environment: str = "development"

    # API Configuration
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    api_workers: int = 1
    api_reload: bool = True

    # Groq AI Configuration
    groq_api_key: str
    groq_model: str = "mixtral-8x7b-32768"
    groq_temperature: float = 0.7
    groq_max_tokens: int = 1024

    # Logging Configuration
    log_level: str = "INFO"
    log_file: Optional[str] = None
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Streamlit Configuration
    streamlit_page_title: str = "LinguaFlow - English Tutor AI"
    streamlit_layout: str = "wide"

    # Audio Configuration
    audio_sample_rate: int = 16000
    audio_chunk_size: int = 1024

    # CORS Configuration
    allowed_origins: list = ["*"]

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


def configure_logging() -> logging.Logger:
    """Configure application logging.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("linguaflow")
    logger.setLevel(settings.log_level.upper())

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.log_level.upper())
    formatter = logging.Formatter(settings.log_format)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (if configured)
    if settings.log_file:
        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler(
            settings.log_file, maxBytes=10485760, backupCount=5  # 10MB files, 5 backups
        )
        file_handler.setLevel(settings.log_level.upper())
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Initialize logger
logger = configure_logging()
