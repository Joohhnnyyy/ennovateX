"""Tests for audio processing routes.

This module contains tests for all audio-related API endpoints including
speech-to-text, translation, and batch processing.
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import Mock, AsyncMock, patch
import json
import time
import base64


class TestSpeechToTextRoute:
    """Test cases for speech-to-text endpoint."""
    
    def test_speech_to_text_success(self, client: TestClient, speech_to_text_request_data: dict):
        """Test successful speech-to-text transcription."""
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.transcribe_audio = AsyncMock(return_value={
                "text": "Hello, this is a test transcription.",
                "language": "en",
                "confidence": 0.95,
                "processing_time": 1.2,
                "model_used": "test-asr",
                "audio_properties": {
                    "duration_seconds": 5.0,
                    "sample_rate": 16000,
                    "channels": 1,
                    "format": "wav"
                }
            })
            
            response = client.post("/api/v1/audio/speech-to-text", json=speech_to_text_request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "text" in data
            assert "language" in data
            assert "confidence" in data
            assert data["text"] == "Hello, this is a test transcription."
    
    def test_speech_to_text_with_timestamps(self, client: TestClient, sample_base64_audio: str):
        """Test speech-to-text with timestamps enabled."""
        request_data = {
            "audio_data": sample_base64_audio,
            "language": "en",
            "return_timestamps": True
        }
        
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.transcribe_audio = AsyncMock(return_value={
                "text": "Hello world",
                "language": "en",
                "confidence": 0.92,
                "timestamps": [
                    {"start": 0.0, "end": 1.5, "text": "Hello"},
                    {"start": 1.5, "end": 2.8, "text": "world"}
                ],
                "processing_time": 1.5
            })
            
            response = client.post("/api/v1/audio/speech-to-text", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "timestamps" in data
            assert len(data["timestamps"]) == 2
    
    def test_speech_to_text_invalid_audio(self, client: TestClient):
        """Test speech-to-text with invalid audio data."""
        invalid_data = {
            "audio_data": "invalid_base64_audio_data",
            "language": "en"
        }
        
        response = client.post("/api/v1/audio/speech-to-text", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_speech_to_text_missing_data(self, client: TestClient):
        """Test speech-to-text with missing audio data."""
        incomplete_data = {
            "language": "en"
            # Missing 'audio_data' field
        }
        
        response = client.post("/api/v1/audio/speech-to-text", json=incomplete_data)
        assert response.status_code == 422
    
    def test_speech_to_text_with_analysis(self, client: TestClient, sample_base64_audio: str):
        """Test speech-to-text with analysis enabled."""
        request_data = {
            "audio_data": sample_base64_audio,
            "language": "en",
            "include_analysis": True
        }
        
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.transcribe_audio = AsyncMock(return_value={
                "text": "Analyzed transcription.",
                "language": "en",
                "confidence": 0.88,
                "analysis": {
                    "speech_rate_wpm": 150,
                    "pause_count": 3,
                    "volume_level": "normal",
                    "background_noise_level": "low",
                    "speaker_count": 1
                },
                "processing_time": 2.1
            })
            
            response = client.post("/api/v1/audio/speech-to-text", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "analysis" in data
            assert "speech_rate_wpm" in data["analysis"]
    
    @pytest.mark.asyncio
    async def test_speech_to_text_async(self, async_client: AsyncClient, speech_to_text_request_data: dict):
        """Test async speech-to-text transcription."""
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.transcribe_audio = AsyncMock(return_value={
                "text": "Async test transcription.",
                "language": "en",
                "confidence": 0.90,
                "processing_time": 1.0
            })
            
            response = await async_client.post("/api/v1/audio/speech-to-text", json=speech_to_text_request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["text"] == "Async test transcription."


class TestAudioTranslationRoute:
    """Test cases for audio translation endpoint."""
    
    def test_audio_translation_success(self, client: TestClient, sample_base64_audio: str):
        """Test successful audio translation."""
        request_data = {
            "audio_data": sample_base64_audio,
            "source_language": "es",
            "target_language": "en",
            "task": "translate"
        }
        
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.translate_audio = AsyncMock(return_value={
                "translated_text": "Hello, this is a test translation.",
                "original_text": "Hola, esta es una traducción de prueba.",
                "source_language": "es",
                "target_language": "en",
                "confidence": 0.91,
                "processing_time": 2.3
            })
            
            response = client.post("/api/v1/audio/translate", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["translated_text"] == "Hello, this is a test translation."
            assert data["source_language"] == "es"
            assert data["target_language"] == "en"
    
    def test_audio_translation_auto_detect(self, client: TestClient, sample_base64_audio: str):
        """Test audio translation with auto language detection."""
        request_data = {
            "audio_data": sample_base64_audio,
            "source_language": "auto",
            "target_language": "en",
            "task": "translate"
        }
        
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.translate_audio = AsyncMock(return_value={
                "translated_text": "Auto-detected translation.",
                "original_text": "Texto original detectado automáticamente.",
                "source_language": "es",  # Auto-detected
                "target_language": "en",
                "confidence": 0.87,
                "processing_time": 2.8
            })
            
            response = client.post("/api/v1/audio/translate", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["source_language"] == "es"  # Should be auto-detected
    
    def test_audio_translation_unsupported_language(self, client: TestClient, sample_base64_audio: str):
        """Test audio translation with unsupported language."""
        request_data = {
            "audio_data": sample_base64_audio,
            "source_language": "xyz",  # Unsupported language
            "target_language": "en"
        }
        
        response = client.post("/api/v1/audio/translate", json=request_data)
        assert response.status_code == 422  # Validation error


class TestAudioBatchProcessingRoute:
    """Test cases for batch audio processing endpoint."""
    
    def test_batch_transcribe_success(self, client: TestClient, sample_base64_audio: str):
        """Test successful batch audio transcription."""
        request_data = {
            "audio_files": [
                {"audio_data": sample_base64_audio, "audio_id": "audio1", "language": "en"},
                {"audio_data": sample_base64_audio, "audio_id": "audio2", "language": "en"},
                {"audio_data": sample_base64_audio, "audio_id": "audio3", "language": "es"}
            ],
            "task": "transcribe",
            "batch_size": 2
        }
        
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.batch_transcribe = AsyncMock(return_value={
                "transcriptions": [
                    {"audio_id": "audio1", "text": "First transcription", "language": "en", "processing_time": 1.2},
                    {"audio_id": "audio2", "text": "Second transcription", "language": "en", "processing_time": 1.1},
                    {"audio_id": "audio3", "text": "Tercera transcripción", "language": "es", "processing_time": 1.3}
                ],
                "total_processing_time": 3.6,
                "successful_count": 3,
                "failed_count": 0,
                "performance_metrics": {
                    "average_processing_time": 1.2,
                    "throughput_files_per_second": 0.83
                }
            })
            
            response = client.post("/api/v1/audio/batch-transcribe", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert len(data["transcriptions"]) == 3
            assert data["successful_count"] == 3
            assert data["failed_count"] == 0
    
    def test_batch_transcribe_partial_failure(self, client: TestClient, sample_base64_audio: str):
        """Test batch transcription with some failures."""
        request_data = {
            "audio_files": [
                {"audio_data": sample_base64_audio, "audio_id": "audio1", "language": "en"},
                {"audio_data": "invalid_data", "audio_id": "audio2", "language": "en"},
                {"audio_data": sample_base64_audio, "audio_id": "audio3", "language": "en"}
            ],
            "task": "transcribe"
        }
        
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.batch_transcribe = AsyncMock(return_value={
                "transcriptions": [
                    {"audio_id": "audio1", "text": "Valid transcription", "processing_time": 1.2},
                    {"audio_id": "audio2", "error": "Invalid audio data", "processing_time": 0.0},
                    {"audio_id": "audio3", "text": "Another valid transcription", "processing_time": 1.1}
                ],
                "total_processing_time": 2.3,
                "successful_count": 2,
                "failed_count": 1
            })
            
            response = client.post("/api/v1/audio/batch-transcribe", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["successful_count"] == 2
            assert data["failed_count"] == 1
    
    def test_batch_transcribe_empty_list(self, client: TestClient):
        """Test batch transcription with empty audio list."""
        request_data = {
            "audio_files": [],
            "task": "transcribe"
        }
        
        response = client.post("/api/v1/audio/batch-transcribe", json=request_data)
        assert response.status_code == 422  # Validation error


class TestAudioServiceInfoRoute:
    """Test cases for audio service information endpoints."""
    
    def test_get_supported_languages(self, client: TestClient):
        """Test getting supported languages."""
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.get_supported_languages = Mock(return_value={
                "transcription_languages": [
                    {"code": "en", "name": "English", "native_name": "English"},
                    {"code": "es", "name": "Spanish", "native_name": "Español"},
                    {"code": "fr", "name": "French", "native_name": "Français"}
                ],
                "translation_languages": [
                    {"code": "en", "name": "English", "native_name": "English"},
                    {"code": "es", "name": "Spanish", "native_name": "Español"}
                ],
                "auto_detect_available": True
            })
            
            response = client.get("/api/v1/audio/languages")
            
            assert response.status_code == 200
            data = response.json()
            assert "transcription_languages" in data
            assert "translation_languages" in data
            assert len(data["transcription_languages"]) == 3
    
    def test_get_audio_models_info(self, client: TestClient):
        """Test getting audio models information."""
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.get_model_info = Mock(return_value={
                "model_name": "test-asr",
                "model_type": "transformer",
                "device": "cpu",
                "memory_usage_mb": 768,
                "is_loaded": True,
                "supported_formats": ["wav", "mp3", "flac", "m4a"],
                "max_audio_length_seconds": 300,
                "sample_rate": 16000
            })
            
            response = client.get("/api/v1/audio/models/info")
            
            assert response.status_code == 200
            data = response.json()
            assert data["model_name"] == "test-asr"
            assert data["is_loaded"] is True
            assert "supported_formats" in data
    
    def test_get_audio_service_stats(self, client: TestClient):
        """Test getting audio service statistics."""
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.get_stats = Mock(return_value={
                "total_requests": 120,
                "successful_requests": 115,
                "failed_requests": 5,
                "average_processing_time": 2.1,
                "total_processing_time": 241.5,
                "audio_files_processed": 115,
                "total_audio_duration_seconds": 1800,
                "average_audio_duration_seconds": 15.6
            })
            
            response = client.get("/api/v1/audio/stats")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_requests"] == 120
            assert data["audio_files_processed"] == 115
    
    def test_audio_service_health_check(self, client: TestClient):
        """Test audio service health check."""
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.health_check = AsyncMock(return_value={
                "status": "healthy",
                "model_loaded": True,
                "memory_usage_mb": 384,
                "gpu_available": False,
                "supported_formats": ["wav", "mp3"],
                "last_request_time": time.time(),
                "response_time_ms": 35
            })
            
            response = client.get("/api/v1/audio/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["model_loaded"] is True


class TestAudioRouteErrorHandling:
    """Test error handling in audio routes."""
    
    def test_service_unavailable_error(self, client: TestClient, speech_to_text_request_data: dict):
        """Test handling of service unavailable errors."""
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.transcribe_audio = AsyncMock(side_effect=Exception("Service unavailable"))
            
            response = client.post("/api/v1/audio/speech-to-text", json=speech_to_text_request_data)
            
            assert response.status_code == 500
    
    def test_audio_processing_error(self, client: TestClient, sample_base64_audio: str):
        """Test handling of audio processing errors."""
        request_data = {
            "audio_data": sample_base64_audio,
            "language": "en"
        }
        
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.transcribe_audio = AsyncMock(side_effect=ValueError("Invalid audio format"))
            
            response = client.post("/api/v1/audio/speech-to-text", json=request_data)
            
            assert response.status_code == 500
    
    def test_timeout_error(self, client: TestClient, speech_to_text_request_data: dict):
        """Test handling of timeout errors."""
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.transcribe_audio = AsyncMock(side_effect=TimeoutError("Processing timeout"))
            
            response = client.post("/api/v1/audio/speech-to-text", json=speech_to_text_request_data)
            
            assert response.status_code == 500
    
    def test_memory_error(self, client: TestClient, speech_to_text_request_data: dict):
        """Test handling of memory errors."""
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.transcribe_audio = AsyncMock(side_effect=MemoryError("Out of memory"))
            
            response = client.post("/api/v1/audio/speech-to-text", json=speech_to_text_request_data)
            
            assert response.status_code == 500


class TestAudioRoutePerformance:
    """Performance tests for audio routes."""
    
    @pytest.mark.performance
    def test_transcription_performance(self, client: TestClient, performance_threshold: dict, sample_base64_audio: str):
        """Test that speech-to-text meets performance requirements."""
        request_data = {
            "audio_data": sample_base64_audio,
            "language": "en"
        }
        
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.transcribe_audio = AsyncMock(return_value={
                "text": "Performance test transcription.",
                "processing_time": 2.0
            })
            
            start_time = time.time()
            response = client.post("/api/v1/audio/speech-to-text", json=request_data)
            end_time = time.time()
            
            assert response.status_code == 200
            assert (end_time - start_time) < performance_threshold["speech_to_text_max_time"]
    
    @pytest.mark.performance
    def test_batch_processing_performance(self, client: TestClient, sample_base64_audio: str):
        """Test batch processing performance with multiple audio files."""
        request_data = {
            "audio_files": [
                {"audio_data": sample_base64_audio, "audio_id": f"audio{i}", "language": "en"} 
                for i in range(3)
            ],
            "task": "transcribe"
        }
        
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.batch_transcribe = AsyncMock(return_value={
                "transcriptions": [{"audio_id": f"audio{i}", "text": f"Transcription {i}"} for i in range(3)],
                "total_processing_time": 6.0,
                "successful_count": 3,
                "failed_count": 0
            })
            
            start_time = time.time()
            response = client.post("/api/v1/audio/batch-transcribe", json=request_data)
            end_time = time.time()
            
            assert response.status_code == 200
            assert (end_time - start_time) < 10.0  # Should complete within 10 seconds


# Integration tests
class TestAudioRouteIntegration:
    """Integration tests for audio routes."""
    
    @pytest.mark.integration
    def test_full_audio_processing_workflow(self, client: TestClient, sample_base64_audio: str):
        """Test complete audio processing workflow."""
        # First, check service health
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.health_check = AsyncMock(return_value={"status": "healthy"})
            health_response = client.get("/api/v1/audio/health")
            assert health_response.status_code == 200
        
        # Then, get supported languages
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.get_supported_languages = Mock(return_value={"transcription_languages": []})
            languages_response = client.get("/api/v1/audio/languages")
            assert languages_response.status_code == 200
        
        # Get model info
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.get_model_info = Mock(return_value={"model_name": "test"})
            info_response = client.get("/api/v1/audio/models/info")
            assert info_response.status_code == 200
        
        # Finally, process audio
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.transcribe_audio = AsyncMock(return_value={"text": "Test transcription"})
            process_response = client.post("/api/v1/audio/speech-to-text", json={
                "audio_data": sample_base64_audio,
                "language": "en"
            })
            assert process_response.status_code == 200
    
    @pytest.mark.integration
    def test_transcription_to_translation_workflow(self, client: TestClient, sample_base64_audio: str):
        """Test workflow from transcription to translation."""
        # First, transcribe audio
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.transcribe_audio = AsyncMock(return_value={
                "text": "Hola mundo",
                "language": "es"
            })
            transcribe_response = client.post("/api/v1/audio/speech-to-text", json={
                "audio_data": sample_base64_audio,
                "language": "es"
            })
            assert transcribe_response.status_code == 200
        
        # Then, translate the audio directly
        with patch('app.routes.audio.audio_service') as mock_service:
            mock_service.translate_audio = AsyncMock(return_value={
                "translated_text": "Hello world",
                "source_language": "es",
                "target_language": "en"
            })
            translate_response = client.post("/api/v1/audio/translate", json={
                "audio_data": sample_base64_audio,
                "source_language": "es",
                "target_language": "en"
            })
            assert translate_response.status_code == 200