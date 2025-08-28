"""API Routes Package

This package contains all FastAPI route handlers for the EnnovateX AI platform,
organized by functionality: text processing, image processing, audio processing, and health checks.
"""

from .text_routes import router as text_router
from .image_routes import router as image_router
from .audio_routes import router as audio_router
from .healthcheck import router as health_router

__all__ = [
    "text_router",
    "image_router",
    "audio_router", 
    "health_router"
]