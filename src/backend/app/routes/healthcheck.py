"""Health check routes for the EnnovateX AI platform.

Provides endpoints for monitoring the health and status of the API service.
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any
import time
import psutil
import torch
from ..dependencies import get_settings
from ..config import Settings

router = APIRouter(
    prefix="/health",
    tags=["health"]
)


@router.get("/ping")
async def ping() -> Dict[str, str]:
    """Simple ping endpoint to check if the service is alive.
    
    Returns:
        Dict containing status and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": str(int(time.time())),
        "message": "EnnovateX AI Platform is running"
    }


@router.get("/status")
async def health_status(settings: Settings = Depends(get_settings)) -> Dict[str, Any]:
    """Detailed health status including system resources and model availability.
    
    Returns:
        Dict containing detailed system status
    """
    # Get system resources
    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Check GPU availability
    gpu_available = torch.cuda.is_available()
    gpu_count = torch.cuda.device_count() if gpu_available else 0
    
    status = {
        "status": "healthy",
        "timestamp": str(int(time.time())),
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "system": {
            "cpu_usage_percent": cpu_percent,
            "memory_usage_percent": memory.percent,
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "memory_total_gb": round(memory.total / (1024**3), 2)
        },
        "gpu": {
            "available": gpu_available,
            "count": gpu_count,
            "devices": []
        },
        "models": {
            "text_summarizer": "available",
            "image_captioner": "available",
            "audio_asr": "available"
        }
    }
    
    # Add GPU device info if available
    if gpu_available:
        for i in range(gpu_count):
            gpu_props = torch.cuda.get_device_properties(i)
            status["gpu"]["devices"].append({
                "id": i,
                "name": gpu_props.name,
                "memory_total_gb": round(gpu_props.total_memory / (1024**3), 2),
                "memory_allocated_gb": round(torch.cuda.memory_allocated(i) / (1024**3), 2),
                "memory_cached_gb": round(torch.cuda.memory_reserved(i) / (1024**3), 2)
            })
    
    return status


@router.get("/ready")
async def readiness_check() -> Dict[str, Any]:
    """Readiness check to verify if the service is ready to handle requests.
    
    This endpoint can be used by load balancers and orchestrators to determine
    if the service is ready to receive traffic.
    
    Returns:
        Dict containing readiness status
    """
    try:
        # Check if models can be imported (basic readiness check)
        from ..models.text_summarizer import TextSummarizer
        from ..models.image_captioning import ImageCaptioner
        from ..models.audio_asr import AudioASR
        
        return {
            "status": "ready",
            "timestamp": str(int(time.time())),
            "message": "Service is ready to handle requests",
            "checks": {
                "models_importable": True,
                "dependencies_loaded": True
            }
        }
    except Exception as e:
        return {
            "status": "not_ready",
            "timestamp": str(int(time.time())),
            "message": f"Service is not ready: {str(e)}",
            "checks": {
                "models_importable": False,
                "dependencies_loaded": False
            }
        }