"""Common Dependencies

This module contains common FastAPI dependencies used across different routes,
including authentication, rate limiting, and model access.
"""

from fastapi import Depends, HTTPException, status, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
import time
from collections import defaultdict

from .config import settings
from .models.utils import ModelLoader
from .models.text_summarizer import TextSummarizer
from .models.image_captioning import ImageCaptioner
from .models.audio_asr import AudioASR

# Security scheme
security = HTTPBearer(auto_error=False)

# Rate limiting storage (in production, use Redis)
rate_limit_storage: Dict[str, list] = defaultdict(list)

def get_model_loader() -> ModelLoader:
    """Dependency to get the global model loader instance."""
    from .main import model_loader
    if model_loader is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Models are not loaded yet. Please try again later."
        )
    return model_loader

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[Dict[str, Any]]:
    """Dependency to get current user from JWT token (optional)."""
    if not credentials:
        return None
    
    # TODO: Implement JWT token validation
    # For now, return a mock user
    return {"user_id": "anonymous", "username": "anonymous"}

def rate_limit_dependency(
    client_ip: str,
    max_requests: int = settings.RATE_LIMIT_REQUESTS,
    window_seconds: int = settings.RATE_LIMIT_WINDOW
):
    """Rate limiting dependency."""
    current_time = time.time()
    
    # Clean old requests
    rate_limit_storage[client_ip] = [
        req_time for req_time in rate_limit_storage[client_ip]
        if current_time - req_time < window_seconds
    ]
    
    # Check rate limit
    if len(rate_limit_storage[client_ip]) >= max_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Max {max_requests} requests per {window_seconds} seconds."
        )
    
    # Add current request
    rate_limit_storage[client_ip].append(current_time)

def validate_file_size(file: UploadFile, max_size: int = settings.MAX_FILE_SIZE):
    """Validate uploaded file size."""
    if file.size and file.size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size {file.size} exceeds maximum allowed size {max_size} bytes"
        )
    return file

def validate_image_file(file: UploadFile) -> UploadFile:
    """Validate uploaded image file."""
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image type. Allowed types: {settings.ALLOWED_IMAGE_TYPES}"
        )
    return validate_file_size(file)

def validate_audio_file(file: UploadFile) -> UploadFile:
    """Validate uploaded audio file."""
    if file.content_type not in settings.ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid audio type. Allowed types: {settings.ALLOWED_AUDIO_TYPES}"
        )
    return validate_file_size(file)

def validate_text_length(text: str, max_length: int = settings.MAX_TEXT_LENGTH) -> str:
    """Validate text length."""
    if len(text) > max_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Text length {len(text)} exceeds maximum allowed length {max_length}"
        )
    return text

# Global text summarizer instance
_text_summarizer: Optional[TextSummarizer] = None

def get_text_summarizer() -> TextSummarizer:
    """Dependency to get the text summarizer instance."""
    global _text_summarizer
    if _text_summarizer is None:
        _text_summarizer = TextSummarizer()
    return _text_summarizer

# Global image captioner instance
_image_captioner: Optional[ImageCaptioner] = None

def get_image_captioner() -> ImageCaptioner:
    """Dependency to get the image captioner instance."""
    global _image_captioner
    if _image_captioner is None:
        model_loader = get_model_loader()
        _image_captioner = ImageCaptioner(model_loader=model_loader)
    return _image_captioner

# Global audio ASR instance
_audio_asr: Optional[AudioASR] = None

def get_audio_asr() -> AudioASR:
    """Dependency to get the audio ASR instance."""
    global _audio_asr
    if _audio_asr is None:
        model_loader = get_model_loader()
        _audio_asr = AudioASR(model_loader=model_loader)
    return _audio_asr

def validate_text_input(text: str) -> str:
    """Validate text input for processing."""
    if not text or not text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text input cannot be empty"
        )
    return validate_text_length(text.strip())

def check_rate_limit():
    """Check rate limit for requests."""
    # For now, just pass - implement actual rate limiting as needed
    pass

def get_settings() -> Any:
    """Get application settings."""
    return settings

class CommonDependencies:
    """Class to group common dependencies for easier injection."""
    
    def __init__(
        self,
        model_loader: ModelLoader = Depends(get_model_loader),
        current_user: Optional[Dict[str, Any]] = Depends(get_current_user)
    ):
        self.model_loader = model_loader
        self.current_user = current_user