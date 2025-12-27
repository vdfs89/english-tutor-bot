"""Pytest configuration and shared fixtures.

This module provides shared test fixtures and pytest configuration
for the LinguaFlow test suite.
"""

import pytest

from src.core.config import Settings


@pytest.fixture
def settings_fixture() -> Settings:
    """Provide a Settings instance for testing.

    Returns:
        Settings: A Settings instance with test configuration.
    """
    return Settings(groq_api_key="test-api-key")


@pytest.fixture
def test_config() -> dict:
    """Provide test configuration dictionary.

    Returns:
        dict: Test configuration with default values.
    """
    return {
        "api_host": "127.0.0.1",
        "api_port": 8000,
        "groq_api_key": "test-key",
        "log_level": "INFO",
    }
