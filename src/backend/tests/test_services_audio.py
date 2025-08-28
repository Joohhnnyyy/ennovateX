"""Tests for audio service.

This module contains tests for the AudioService class and its methods.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import asyncio
import base64
import numpy as np
from app.services.audio_service import AudioService
from app.models.audio_asr import AudioASR


class TestAudioServiceInitialization:
    """Test cases for AudioService initialization."""
    
    def test_audio_service_init(self, mock_audio_asr):
        """Test AudioService initialization."""
        service = AudioService(mock_audio_asr)
        
        assert service.model == mock_audio_asr
        assert service.stats["total_requests"] == 0
        assert service.stats["successful_requests"] == 0
        assert service.stats["failed_requests"] == 0
        assert service.stats["total_processing_time"] == 0.0
        assert service.stats["average_processing_time"] == 0.0


class TestAudioProcessing:
    """Test cases for audio processing methods."""
    
    def test_decode_base64_audio_success(self, audio_service, sample_audio_base64):
        """Test successful base64 audio decoding."""
        audio_data = audio_service._decode_base64_audio(sample_audio_base64)
        
        assert isinstance(audio_data, bytes)
        assert len(audio_data) > 0
    
    def test_decode_base64_audio_invalid_data(self, audio_service):
        """Test base64 audio decoding with invalid data."""
        invalid_base64 = "invalid_base64_data"
        
        with pytest.raises(ValueError, match="Invalid base64 audio data"):
            audio_service._decode_base64_audio(invalid_base64)
    
    def test_preprocess_audio_resample(self, audio_service):
        """Test audio preprocessing with resampling."""
        # Create mock audio data (16kHz, 1 second)
        sample_rate = 16000
        audio_array = np.random.randn(sample_rate).astype(np.float32)
        
        processed = audio_service._preprocess_audio(
            audio_array, 
            original_sample_rate=sample_rate,
            target_sample_rate=8000
        )
        
        # Should be resampled to 8kHz (half the length)
        assert len(processed) == sample_rate // 2
        assert isinstance(processed, np.ndarray)
    
    def test_preprocess_audio_normalize(self, audio_service):
        """Test audio preprocessing with normalization."""
        # Create audio with high amplitude
        audio_array = np.array([2.0, -2.0, 1.5, -1.5], dtype=np.float32)
        
        processed = audio_service._preprocess_audio(
            audio_array,
            normalize=True
        )
        
        # Should be normalized to [-1, 1] range
        assert np.max(processed) <= 1.0
        assert np.min(processed) >= -1.0
    
    def test_preprocess_audio_no_changes(self, audio_service):
        """Test audio preprocessing with no changes."""
        audio_array = np.random.randn(1000).astype(np.float32)
        
        processed = audio_service._preprocess_audio(audio_array)
        
        # Should return the same array if no preprocessing is specified
        np.testing.assert_array_equal(processed, audio_array)
    
    def test_analyze_audio_properties(self, audio_service):
        """Test audio properties analysis."""
        # Create test audio (1 second at 16kHz)
        sample_rate = 16000
        audio_array = np.random.randn(sample_rate).astype(np.float32)
        
        properties = audio_service._analyze_audio_properties(audio_array, sample_rate)
        
        assert "duration_seconds" in properties
        assert "sample_rate" in properties
        assert "channels" in properties
        assert "rms_level" in properties
        assert "has_silence" in properties
        
        assert properties["duration_seconds"] == 1.0
        assert properties["sample_rate"] == sample_rate
        assert properties["channels"] == 1
        assert isinstance(properties["rms_level"], float)
        assert isinstance(properties["has_silence"], bool)
    
    def test_detect_silence(self, audio_service):
        """Test silence detection."""
        # Create audio with silence (zeros)
        silent_audio = np.zeros(1000, dtype=np.float32)
        assert audio_service._detect_silence(silent_audio) is True
        
        # Create audio with sound
        loud_audio = np.random.randn(1000).astype(np.float32) * 0.5
        assert audio_service._detect_silence(loud_audio) is False
    
    def test_calculate_rms(self, audio_service):
        """Test RMS calculation."""
        # Test with known values
        audio_array = np.array([1.0, -1.0, 1.0, -1.0], dtype=np.float32)
        rms = audio_service._calculate_rms(audio_array)
        
        expected_rms = np.sqrt(np.mean(audio_array ** 2))
        assert abs(rms - expected_rms) < 1e-6


class TestSpeechToText:
    """Test cases for speech-to-text transcription."""
    
    @pytest.mark.asyncio
    async def test_transcribe_audio_success(self, audio_service, sample_audio_base64):
        """Test successful audio transcription."""
        expected_transcription = "Hello, this is a test transcription."
        audio_service.model.transcribe = AsyncMock(return_value=expected_transcription)
        
        result = await audio_service.transcribe_audio(
            audio_data=sample_audio_base64,
            language="en"
        )
        
        assert result == expected_transcription
        audio_service.model.transcribe.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_transcribe_audio_with_timestamps(self, audio_service, sample_audio_base64):
        """Test audio transcription with timestamps."""
        expected_result = {
            "text": "Hello, this is a test.",
            "segments": [
                {"start": 0.0, "end": 2.5, "text": "Hello, this is a test."}
            ]
        }
        audio_service.model.transcribe = AsyncMock(return_value=expected_result)
        
        result = await audio_service.transcribe_audio(
            audio_data=sample_audio_base64,
            language="en",
            return_timestamps=True
        )
        
        assert "text" in result
        assert "segments" in result
        assert result["text"] == "Hello, this is a test."
        assert len(result["segments"]) == 1
    
    @pytest.mark.asyncio
    async def test_transcribe_audio_with_preprocessing(self, audio_service, sample_audio_base64):
        """Test audio transcription with preprocessing."""
        expected_transcription = "Preprocessed transcription"
        audio_service.model.transcribe = AsyncMock(return_value=expected_transcription)
        
        result = await audio_service.transcribe_audio(
            audio_data=sample_audio_base64,
            language="en",
            preprocess=True,
            target_sample_rate=16000
        )
        
        assert result == expected_transcription
        # Verify the model was called with preprocessed audio
        audio_service.model.transcribe.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_transcribe_audio_model_error(self, audio_service, sample_audio_base64):
        """Test handling of model errors during transcription."""
        audio_service.model.transcribe = AsyncMock(side_effect=Exception("Model error"))
        
        with pytest.raises(Exception, match="Model error"):
            await audio_service.transcribe_audio(sample_audio_base64)
    
    @pytest.mark.asyncio
    async def test_transcribe_audio_empty_data(self, audio_service):
        """Test transcription with empty audio data."""
        with pytest.raises(ValueError, match="Audio data cannot be empty"):
            await audio_service.transcribe_audio("")
    
    @pytest.mark.asyncio
    async def test_transcribe_audio_auto_language_detection(self, audio_service, sample_audio_base64):
        """Test transcription with automatic language detection."""
        expected_result = {
            "text": "Bonjour, ceci est un test.",
            "language": "fr"
        }
        audio_service.model.transcribe = AsyncMock(return_value=expected_result)
        
        result = await audio_service.transcribe_audio(
            audio_data=sample_audio_base64,
            language="auto"
        )
        
        assert "text" in result
        assert "language" in result
        assert result["language"] == "fr"


class TestAudioTranslation:
    """Test cases for audio translation."""
    
    @pytest.mark.asyncio
    async def test_translate_audio_success(self, audio_service, sample_audio_base64):
        """Test successful audio translation."""
        expected_translation = "Hello, this is a test translation."
        audio_service.model.translate = AsyncMock(return_value=expected_translation)
        
        result = await audio_service.translate_audio(
            audio_data=sample_audio_base64,
            source_language="es",
            target_language="en"
        )
        
        assert result == expected_translation
        audio_service.model.translate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_translate_audio_auto_detection(self, audio_service, sample_audio_base64):
        """Test audio translation with automatic source language detection."""
        expected_result = {
            "translation": "Hello, this is a test.",
            "detected_language": "es"
        }
        audio_service.model.translate = AsyncMock(return_value=expected_result)
        
        result = await audio_service.translate_audio(
            audio_data=sample_audio_base64,
            source_language="auto",
            target_language="en"
        )
        
        assert "translation" in result
        assert "detected_language" in result
        assert result["detected_language"] == "es"
    
    @pytest.mark.asyncio
    async def test_translate_audio_unsupported_language(self, audio_service, sample_audio_base64):
        """Test audio translation with unsupported language."""
        audio_service.model.translate = AsyncMock(
            side_effect=ValueError("Unsupported language: xyz")
        )
        
        with pytest.raises(ValueError, match="Unsupported language"):
            await audio_service.translate_audio(
                audio_data=sample_audio_base64,
                source_language="xyz",
                target_language="en"
            )
    
    @pytest.mark.asyncio
    async def test_translate_audio_empty_data(self, audio_service):
        """Test translation with empty audio data."""
        with pytest.raises(ValueError, match="Audio data cannot be empty"):
            await audio_service.translate_audio(
                audio_data="",
                source_language="es",
                target_language="en"
            )


class TestEnhancedTranscription:
    """Test cases for enhanced transcription with analysis."""
    
    @pytest.mark.asyncio
    async def test_enhanced_transcribe_with_analysis(self, audio_service, sample_audio_base64):
        """Test enhanced transcription with audio analysis."""
        expected_transcription = "Enhanced transcription with analysis"
        audio_service.model.transcribe = AsyncMock(return_value=expected_transcription)
        
        result = await audio_service.enhanced_transcribe(
            audio_data=sample_audio_base64,
            language="en",
            include_analysis=True
        )
        
        assert "transcription" in result
        assert "analysis" in result
        assert result["transcription"] == expected_transcription
        assert "properties" in result["analysis"]
        assert "confidence" in result["analysis"]
    
    @pytest.mark.asyncio
    async def test_enhanced_transcribe_without_analysis(self, audio_service, sample_audio_base64):
        """Test enhanced transcription without analysis."""
        expected_transcription = "Enhanced transcription without analysis"
        audio_service.model.transcribe = AsyncMock(return_value=expected_transcription)
        
        result = await audio_service.enhanced_transcribe(
            audio_data=sample_audio_base64,
            language="en",
            include_analysis=False
        )
        
        assert "transcription" in result
        assert "analysis" not in result
        assert result["transcription"] == expected_transcription
    
    @pytest.mark.asyncio
    async def test_enhanced_transcribe_with_post_processing(self, audio_service, sample_audio_base64):
        """Test enhanced transcription with post-processing."""
        raw_transcription = "hello   this  is  a   test"
        expected_processed = "Hello this is a test."
        
        audio_service.model.transcribe = AsyncMock(return_value=raw_transcription)
        
        result = await audio_service.enhanced_transcribe(
            audio_data=sample_audio_base64,
            language="en",
            post_process=True
        )
        
        # Verify post-processing was applied
        assert result["transcription"] != raw_transcription
        assert result["transcription"] == expected_processed


class TestBatchProcessing:
    """Test cases for batch audio processing."""
    
    @pytest.mark.asyncio
    async def test_batch_transcribe_success(self, audio_service):
        """Test successful batch audio transcription."""
        audio_data_list = ["audio_data_1", "audio_data_2"]
        expected_transcriptions = ["Transcription 1", "Transcription 2"]
        
        # Mock the decode method to return valid audio data
        with patch.object(audio_service, '_decode_base64_audio') as mock_decode:
            mock_decode.return_value = b"mock_audio_bytes"
            
            audio_service.model.transcribe = AsyncMock(side_effect=expected_transcriptions)
            
            results = await audio_service.batch_transcribe(
                audio_data_list=audio_data_list,
                language="en"
            )
        
        assert len(results["results"]) == 2
        assert results["results"][0]["transcription"] == "Transcription 1"
        assert results["results"][1]["transcription"] == "Transcription 2"
        assert results["total_processed"] == 2
        assert results["successful"] == 2
        assert results["failed"] == 0
    
    @pytest.mark.asyncio
    async def test_batch_transcribe_partial_failure(self, audio_service):
        """Test batch transcription with partial failures."""
        audio_data_list = ["valid_audio_1", "invalid_audio", "valid_audio_2"]
        
        def mock_decode(data):
            if "invalid" in data:
                raise ValueError("Invalid audio")
            return b"mock_audio_bytes"
        
        with patch.object(audio_service, '_decode_base64_audio', side_effect=mock_decode):
            audio_service.model.transcribe = AsyncMock(
                side_effect=lambda audio, **kwargs: f"Transcription for {audio}"
            )
            
            results = await audio_service.batch_transcribe(
                audio_data_list=audio_data_list,
                language="en"
            )
        
        assert len(results["results"]) == 3
        assert "transcription" in results["results"][0]
        assert "error" in results["results"][1]
        assert "transcription" in results["results"][2]
        assert results["total_processed"] == 3
        assert results["successful"] == 2
        assert results["failed"] == 1
    
    @pytest.mark.asyncio
    async def test_batch_transcribe_concurrency_limit(self, audio_service):
        """Test batch transcription with concurrency limit."""
        audio_data_list = [f"audio_{i}" for i in range(10)]
        
        call_times = []
        
        async def mock_transcribe(audio, **kwargs):
            call_times.append(asyncio.get_event_loop().time())
            await asyncio.sleep(0.1)  # Simulate processing time
            return f"Transcription for {audio}"
        
        with patch.object(audio_service, '_decode_base64_audio') as mock_decode:
            mock_decode.return_value = b"mock_audio_bytes"
            
            audio_service.model.transcribe = AsyncMock(side_effect=mock_transcribe)
            
            results = await audio_service.batch_transcribe(
                audio_data_list=audio_data_list,
                language="en",
                max_concurrent=3
            )
        
        assert results["total_processed"] == 10
        assert results["successful"] == 10
        assert results["failed"] == 0
        
        # Verify concurrency was limited
        assert len(call_times) == 10
    
    @pytest.mark.asyncio
    async def test_batch_transcribe_empty_list(self, audio_service):
        """Test batch transcription with empty audio list."""
        results = await audio_service.batch_transcribe(
            audio_data_list=[],
            language="en"
        )
        
        assert results["results"] == []
        assert results["total_processed"] == 0
        assert results["successful"] == 0
        assert results["failed"] == 0


class TestSupportedLanguages:
    """Test cases for supported languages functionality."""
    
    def test_get_supported_languages(self, audio_service):
        """Test getting supported languages."""
        expected_languages = {
            "transcription": ["en", "es", "fr", "de", "it"],
            "translation": ["en", "es", "fr", "de"]
        }
        
        audio_service.model.get_supported_languages = Mock(return_value=expected_languages)
        
        languages = audio_service.get_supported_languages()
        
        assert languages == expected_languages
        assert "transcription" in languages
        assert "translation" in languages
        audio_service.model.get_supported_languages.assert_called_once()
    
    def test_get_supported_languages_exception(self, audio_service):
        """Test getting supported languages when an exception occurs."""
        audio_service.model.get_supported_languages = Mock(
            side_effect=Exception("Languages error")
        )
        
        languages = audio_service.get_supported_languages()
        
        assert "error" in languages
        assert "Languages error" in languages["error"]


class TestServiceStatistics:
    """Test cases for service statistics tracking."""
    
    @pytest.mark.asyncio
    async def test_stats_tracking_success(self, audio_service, sample_audio_base64):
        """Test statistics tracking for successful requests."""
        audio_service.model.transcribe = AsyncMock(return_value="Test transcription")
        
        initial_stats = audio_service.get_stats().copy()
        
        await audio_service.transcribe_audio(sample_audio_base64)
        
        final_stats = audio_service.get_stats()
        
        assert final_stats["total_requests"] == initial_stats["total_requests"] + 1
        assert final_stats["successful_requests"] == initial_stats["successful_requests"] + 1
        assert final_stats["failed_requests"] == initial_stats["failed_requests"]
        assert final_stats["total_processing_time"] > initial_stats["total_processing_time"]
    
    @pytest.mark.asyncio
    async def test_stats_tracking_failure(self, audio_service, sample_audio_base64):
        """Test statistics tracking for failed requests."""
        audio_service.model.transcribe = AsyncMock(side_effect=Exception("Test error"))
        
        initial_stats = audio_service.get_stats().copy()
        
        with pytest.raises(Exception):
            await audio_service.transcribe_audio(sample_audio_base64)
        
        final_stats = audio_service.get_stats()
        
        assert final_stats["total_requests"] == initial_stats["total_requests"] + 1
        assert final_stats["successful_requests"] == initial_stats["successful_requests"]
        assert final_stats["failed_requests"] == initial_stats["failed_requests"] + 1
    
    def test_get_stats(self, audio_service):
        """Test getting service statistics."""
        stats = audio_service.get_stats()
        
        required_keys = [
            "total_requests", "successful_requests", "failed_requests",
            "total_processing_time", "average_processing_time", "uptime_seconds"
        ]
        
        for key in required_keys:
            assert key in stats
        
        assert isinstance(stats["total_requests"], int)
        assert isinstance(stats["successful_requests"], int)
        assert isinstance(stats["failed_requests"], int)
        assert isinstance(stats["total_processing_time"], float)
        assert isinstance(stats["average_processing_time"], float)
        assert isinstance(stats["uptime_seconds"], float)


class TestHealthCheck:
    """Test cases for health check functionality."""
    
    @pytest.mark.asyncio
    async def test_health_check_healthy(self, audio_service):
        """Test health check when service is healthy."""
        audio_service.model.is_loaded = Mock(return_value=True)
        audio_service.model.get_model_info = Mock(return_value={
            "model_name": "test-asr",
            "device": "cpu",
            "memory_usage_mb": 768
        })
        
        health = await audio_service.health_check()
        
        assert health["status"] == "healthy"
        assert health["model_loaded"] is True
        assert health["model_name"] == "test-asr"
        assert "response_time_ms" in health
        assert "memory_usage_mb" in health
    
    @pytest.mark.asyncio
    async def test_health_check_model_not_loaded(self, audio_service):
        """Test health check when model is not loaded."""
        audio_service.model.is_loaded = Mock(return_value=False)
        
        health = await audio_service.health_check()
        
        assert health["status"] == "unhealthy"
        assert health["model_loaded"] is False
        assert "error" in health
    
    @pytest.mark.asyncio
    async def test_health_check_exception(self, audio_service):
        """Test health check when an exception occurs."""
        audio_service.model.is_loaded = Mock(side_effect=Exception("Model error"))
        
        health = await audio_service.health_check()
        
        assert health["status"] == "error"
        assert "error" in health
        assert "Model error" in health["error"]


class TestModelInfo:
    """Test cases for model information retrieval."""
    
    def test_get_model_info_success(self, audio_service):
        """Test successful model info retrieval."""
        expected_info = {
            "model_name": "test-asr",
            "is_loaded": True,
            "device": "cpu",
            "memory_usage_mb": 768,
            "supported_formats": ["wav", "mp3", "flac"]
        }
        
        audio_service.model.get_model_info = Mock(return_value=expected_info)
        
        info = audio_service.get_model_info()
        
        assert info == expected_info
        audio_service.model.get_model_info.assert_called_once()
    
    def test_get_model_info_exception(self, audio_service):
        """Test model info retrieval when an exception occurs."""
        audio_service.model.get_model_info = Mock(side_effect=Exception("Info error"))
        
        info = audio_service.get_model_info()
        
        assert info["error"] == "Info error"
        assert info["is_loaded"] is False


# Performance tests
class TestAudioServicePerformance:
    """Performance tests for audio service."""
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_transcription_performance(self, audio_service, sample_audio_base64):
        """Test transcription performance with long audio."""
        audio_service.model.transcribe = AsyncMock(return_value="Performance test transcription")
        
        import time
        start_time = time.time()
        
        result = await audio_service.transcribe_audio(sample_audio_base64)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        assert result == "Performance test transcription"
        assert processing_time < 5.0  # Should complete within 5 seconds
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_batch_processing_performance(self, audio_service):
        """Test batch processing performance."""
        audio_data_list = [f"audio_data_{i}" for i in range(20)]
        
        with patch.object(audio_service, '_decode_base64_audio') as mock_decode:
            mock_decode.return_value = b"mock_audio_bytes"
            
            audio_service.model.transcribe = AsyncMock(
                side_effect=lambda audio, **kwargs: f"Transcription for {audio}"
            )
            
            import time
            start_time = time.time()
            
            results = await audio_service.batch_transcribe(
                audio_data_list=audio_data_list,
                language="en",
                max_concurrent=5
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
        
        assert results["total_processed"] == 20
        assert results["successful"] == 20
        assert processing_time < 10.0  # Should complete within 10 seconds