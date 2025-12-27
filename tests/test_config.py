"""Tests for configuration module.

This module tests the Settings and logging configuration.
"""

import pytest

from src.core.config import Settings, configure_logging


class TestSettings:
    """Test suite for Settings class."""

    def test_settings_defaults(self) -> None:
        """Test that Settings has proper default values."""
        settings = Settings(groq_api_key="test-key")
        assert settings.app_name == "LinguaFlow"
        assert settings.environment == "development"
        assert settings.debug is False

    def test_settings_groq_configuration(self) -> None:
        """Test Groq configuration settings."""
        settings = Settings(groq_api_key="test-key")
        assert settings.groq_api_key == "test-key"
        assert settings.groq_model == "mixtral-8x7b-32768"
        assert settings.groq_temperature == 0.7
        assert settings.groq_max_tokens == 1024

    def test_settings_api_configuration(self) -> None:
        """Test API configuration settings."""
        settings = Settings(groq_api_key="test-key")
        assert settings.api_host == "127.0.0.1"
        assert settings.api_port == 8000
        assert settings.api_workers == 1
        assert settings.api_reload is True

    def test_settings_logging_configuration(self) -> None:
        """Test logging configuration settings."""
        settings = Settings(groq_api_key="test-key")
        assert settings.log_level == "INFO"
        assert settings.log_file is None

    def test_settings_audio_configuration(self) -> None:
        """Test audio configuration settings."""
        settings = Settings(groq_api_key="test-key")
        assert settings.audio_sample_rate == 16000
        assert settings.audio_chunk_size == 1024


class TestLogging:
    """Test suite for logging configuration."""

    def test_configure_logging_returns_logger(self) -> None:
        """Test that configure_logging returns a logger instance."""
        logger = configure_logging()
        assert logger is not None
        assert logger.name == "linguaflow"

    def test_logger_level_configuration(self) -> None:
        """Test that logger level is properly configured."""
        from src.core.config import logger, settings

        # Check that logger is configured
        assert logger.name == "linguaflow"
        assert len(logger.handlers) > 0
