"""FastAPI Main Application Entry Point

This module contains the main FastAPI application setup with all route registrations,
middleware configuration, and startup/shutdown event handlers.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager

from .config import settings
from .routes import text_router, image_router, audio_router, health_router
from .models.utils import ModelLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global model loader instance
model_loader = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    global model_loader
    
    # Startup
    logger.info("Starting EnnovateX AI Platform Backend...")
    try:
        model_loader = ModelLoader()
        await model_loader.initialize_models()
        logger.info("All models loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down EnnovateX AI Platform Backend...")
    if model_loader:
        await model_loader.cleanup()
    logger.info("Shutdown complete")

# Create FastAPI application
app = FastAPI(
    title="EnnovateX AI Platform API",
    description="Advanced AI platform for text, image, and audio processing with LoRA adapters",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

# Register routers
app.include_router(health_router, prefix="/api/v1", tags=["Health"])
app.include_router(text_router, prefix="/api/v1/text", tags=["Text Processing"])
app.include_router(image_router, prefix="/api/v1/image", tags=["Image Processing"])
app.include_router(audio_router, prefix="/api/v1/audio", tags=["Audio Processing"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "EnnovateX AI Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/ping"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )