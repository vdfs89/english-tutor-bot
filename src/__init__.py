"""LinguaFlow - English Tutor AI

A modern, AI-powered English learning platform.
"""

__version__ = "0.1.0"
__author__ = "vdfs89"
__email__ = "contact@linguaflow.dev"

from .core import Settings, configure_logging, logger, settings

__all__ = ["Settings", "configure_logging", "logger", "settings"]
