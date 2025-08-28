"""Pytest configuration and shared fixtures for EnnovateX AI Platform tests.

This module provides common test fixtures and configuration for all test modules.
"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from httpx import AsyncClient
import tempfile
import os
from unittest.mock import Mock, AsyncMock

from app.main import app
from app.config import Settings
from app.models.text_summarizer import TextSummarizer
from app.models.image_captioning import ImageCaptioner
from app.models.audio_asr import AudioASR
from app.services.text_service import TextService
from app.services.image_service import ImageService
from app.services.audio_service import AudioService


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_settings() -> Settings:
    """Create test settings with mock configurations."""
    return Settings(
        app_name="EnnovateX AI Platform Test",
        app_version="0.1.0-test",
        debug=True,
        environment="test",
        log_level="DEBUG",
        max_workers=2,
        model_cache_dir="/tmp/test_models",
        enable_gpu=False,
        cors_origins=["http://localhost:3000"],
        api_prefix="/api/v1"
    )


@pytest.fixture
def client(test_settings: Settings) -> TestClient:
    """Create a test client for the FastAPI application."""
    # Override the settings dependency
    app.dependency_overrides[Settings] = lambda: test_settings
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up dependency overrides
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client(test_settings: Settings) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client for the FastAPI application."""
    # Override the settings dependency
    app.dependency_overrides[Settings] = lambda: test_settings
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    # Clean up dependency overrides
    app.dependency_overrides.clear()


@pytest.fixture
def mock_text_summarizer() -> Mock:
    """Create a mock text summarizer."""
    mock_summarizer = Mock(spec=TextSummarizer)
    mock_summarizer.summarize = AsyncMock(return_value={
        "summary": "This is a test summary.",
        "confidence": 0.95,
        "processing_time": 0.5
    })
    mock_summarizer.question_answer = AsyncMock(return_value={
        "answer": "This is a test answer.",
        "confidence": 0.90,
        "processing_time": 0.3
    })
    mock_summarizer.is_loaded = True
    mock_summarizer.model_name = "test-summarizer"
    mock_summarizer.device = "cpu"
    return mock_summarizer


@pytest.fixture
def mock_image_captioner() -> Mock:
    """Create a mock image captioner."""
    mock_captioner = Mock(spec=ImageCaptioner)
    mock_captioner.caption = AsyncMock(return_value={
        "caption": "A test image caption.",
        "confidence": 0.88,
        "processing_time": 0.7
    })
    mock_captioner.visual_question_answer = AsyncMock(return_value={
        "answer": "Test VQA answer.",
        "confidence": 0.85,
        "processing_time": 0.6
    })
    mock_captioner.is_loaded = True
    mock_captioner.model_name = "test-captioner"
    mock_captioner.device = "cpu"
    return mock_captioner


@pytest.fixture
def mock_audio_asr() -> Mock:
    """Create a mock audio ASR model."""
    mock_asr = Mock(spec=AudioASR)
    mock_asr.transcribe = AsyncMock(return_value={
        "text": "This is a test transcription.",
        "language": "en",
        "confidence": 0.92,
        "processing_time": 1.2
    })
    mock_asr.translate = AsyncMock(return_value={
        "translated_text": "This is a test translation.",
        "source_language": "es",
        "target_language": "en",
        "confidence": 0.87,
        "processing_time": 1.5
    })
    mock_asr.is_loaded = True
    mock_asr.model_name = "test-asr"
    mock_asr.device = "cpu"
    return mock_asr


@pytest.fixture
def mock_text_service(mock_text_summarizer: Mock, test_settings: Settings) -> TextService:
    """Create a text service with mocked dependencies."""
    service = TextService(mock_text_summarizer, test_settings)
    return service


@pytest.fixture
def mock_image_service(mock_image_captioner: Mock, test_settings: Settings) -> ImageService:
    """Create an image service with mocked dependencies."""
    service = ImageService(mock_image_captioner, test_settings)
    return service


@pytest.fixture
def mock_audio_service(mock_audio_asr: Mock, test_settings: Settings) -> AudioService:
    """Create an audio service with mocked dependencies."""
    service = AudioService(mock_audio_asr, test_settings)
    return service


@pytest.fixture
def sample_text() -> str:
    """Provide sample text for testing."""
    return (
        "Artificial intelligence (AI) is intelligence demonstrated by machines, "
        "in contrast to the natural intelligence displayed by humans and animals. "
        "Leading AI textbooks define the field as the study of 'intelligent agents': "
        "any device that perceives its environment and takes actions that maximize "
        "its chance of successfully achieving its goals. Colloquially, the term "
        "'artificial intelligence' is often used to describe machines that mimic "
        "'cognitive' functions that humans associate with the human mind, such as "
        "'learning' and 'problem solving'."
    )


@pytest.fixture
def sample_base64_image() -> str:
    """Provide a sample base64 encoded image for testing."""
    # This is a minimal 1x1 pixel PNG image encoded in base64
    return (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )


@pytest.fixture
def sample_base64_audio() -> str:
    """Provide a sample base64 encoded audio for testing."""
    # This is a minimal WAV file header encoded in base64
    return (
        "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA="
    )


@pytest.fixture
def temp_file() -> Generator[str, None, None]:
    """Create a temporary file for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"test content")
        temp_path = tmp.name
    
    yield temp_path
    
    # Clean up
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_path:
        yield temp_path


# Test data fixtures
@pytest.fixture
def text_summarization_request_data() -> dict:
    """Sample text summarization request data."""
    return {
        "text": "This is a sample text that needs to be summarized for testing purposes.",
        "max_length": 50,
        "min_length": 10,
        "summary_type": "abstractive",
        "include_analysis": False,
        "use_lora": False
    }


@pytest.fixture
def image_captioning_request_data(sample_base64_image: str) -> dict:
    """Sample image captioning request data."""
    return {
        "image_data": sample_base64_image,
        "max_length": 50,
        "min_length": 5,
        "num_beams": 5,
        "temperature": 1.0,
        "include_analysis": False,
        "use_lora": False
    }


@pytest.fixture
def speech_to_text_request_data(sample_base64_audio: str) -> dict:
    """Sample speech-to-text request data."""
    return {
        "audio_data": sample_base64_audio,
        "language": "en",
        "task": "transcribe",
        "return_timestamps": False,
        "include_analysis": False,
        "use_lora": False
    }


# Mock external dependencies
@pytest.fixture(autouse=True)
def mock_external_dependencies(monkeypatch):
    """Mock external dependencies that might not be available in test environment."""
    # Mock torch if not available
    try:
        import torch
    except ImportError:
        mock_torch = Mock()
        mock_torch.cuda.is_available.return_value = False
        mock_torch.device.return_value = "cpu"
        monkeypatch.setattr("torch", mock_torch)
    
    # Mock transformers if not available
    try:
        import transformers
    except ImportError:
        mock_transformers = Mock()
        monkeypatch.setattr("transformers", mock_transformers)
    
    # Mock other ML libraries as needed
    try:
        import PIL
    except ImportError:
        mock_pil = Mock()
        monkeypatch.setattr("PIL", mock_pil)


# Performance testing fixtures
@pytest.fixture
def performance_threshold() -> dict:
    """Define performance thresholds for testing."""
    return {
        "text_summarization_max_time": 5.0,  # seconds
        "image_captioning_max_time": 10.0,   # seconds
        "speech_to_text_max_time": 15.0,     # seconds
        "max_memory_usage_mb": 1000,         # MB
    }


# Database fixtures (if needed in the future)
@pytest.fixture
def mock_database():
    """Mock database connection for testing."""
    # This can be expanded when database functionality is added
    return Mock()


# Cleanup fixture
@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Cleanup resources after each test."""
    yield
    # Perform any necessary cleanup here
    # For example, clear caches, reset global state, etc.
    pass