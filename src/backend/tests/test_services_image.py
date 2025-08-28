"""Tests for image service.

This module contains tests for the ImageService class and its methods.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import asyncio
import base64
from PIL import Image
import io
from app.services.image_service import ImageService
from app.models.image_captioning import ImageCaptioner


class TestImageServiceInitialization:
    """Test cases for ImageService initialization."""
    
    def test_image_service_init(self, mock_image_captioner):
        """Test ImageService initialization."""
        service = ImageService(mock_image_captioner)
        
        assert service.model == mock_image_captioner
        assert service.stats["total_requests"] == 0
        assert service.stats["successful_requests"] == 0
        assert service.stats["failed_requests"] == 0
        assert service.stats["total_processing_time"] == 0.0
        assert service.stats["average_processing_time"] == 0.0


class TestImageProcessing:
    """Test cases for image processing methods."""
    
    def test_decode_base64_image_success(self, image_service, sample_image_base64):
        """Test successful base64 image decoding."""
        image = image_service._decode_base64_image(sample_image_base64)
        
        assert isinstance(image, Image.Image)
        assert image.size == (100, 100)  # Based on sample image
        assert image.mode in ['RGB', 'RGBA']
    
    def test_decode_base64_image_invalid_data(self, image_service):
        """Test base64 image decoding with invalid data."""
        invalid_base64 = "invalid_base64_data"
        
        with pytest.raises(ValueError, match="Invalid base64 image data"):
            image_service._decode_base64_image(invalid_base64)
    
    def test_decode_base64_image_not_image(self, image_service):
        """Test base64 decoding with non-image data."""
        text_data = base64.b64encode(b"This is not an image").decode('utf-8')
        
        with pytest.raises(ValueError, match="Invalid image format"):
            image_service._decode_base64_image(text_data)
    
    def test_analyze_image_properties(self, image_service, sample_image_base64):
        """Test image properties analysis."""
        image = image_service._decode_base64_image(sample_image_base64)
        properties = image_service._analyze_image_properties(image)
        
        assert "width" in properties
        assert "height" in properties
        assert "format" in properties
        assert "mode" in properties
        assert "size_bytes" in properties
        assert "aspect_ratio" in properties
        
        assert properties["width"] == 100
        assert properties["height"] == 100
        assert properties["aspect_ratio"] == 1.0
    
    def test_preprocess_image_resize(self, image_service, sample_image_base64):
        """Test image preprocessing with resizing."""
        image = image_service._decode_base64_image(sample_image_base64)
        processed = image_service._preprocess_image(image, target_size=(224, 224))
        
        assert processed.size == (224, 224)
        assert processed.mode == 'RGB'
    
    def test_preprocess_image_normalize(self, image_service, sample_image_base64):
        """Test image preprocessing with normalization."""
        image = image_service._decode_base64_image(sample_image_base64)
        processed = image_service._preprocess_image(image, normalize=True)
        
        # Image should be converted to RGB and potentially normalized
        assert processed.mode == 'RGB'
    
    def test_preprocess_image_no_changes(self, image_service, sample_image_base64):
        """Test image preprocessing with no changes."""
        image = image_service._decode_base64_image(sample_image_base64)
        processed = image_service._preprocess_image(image)
        
        # Should return the same image if no preprocessing is specified
        assert processed.size == image.size


class TestImageCaptioning:
    """Test cases for image captioning."""
    
    @pytest.mark.asyncio
    async def test_caption_image_success(self, image_service, sample_image_base64):
        """Test successful image captioning."""
        expected_caption = "A beautiful landscape with mountains and trees"
        image_service.model.generate_caption = AsyncMock(return_value=expected_caption)
        
        result = await image_service.caption_image(
            image_data=sample_image_base64,
            max_length=50
        )
        
        assert result == expected_caption
        image_service.model.generate_caption.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_caption_image_with_preprocessing(self, image_service, sample_image_base64):
        """Test image captioning with preprocessing."""
        expected_caption = "Preprocessed image caption"
        image_service.model.generate_caption = AsyncMock(return_value=expected_caption)
        
        result = await image_service.caption_image(
            image_data=sample_image_base64,
            max_length=50,
            preprocess=True,
            target_size=(224, 224)
        )
        
        assert result == expected_caption
        # Verify the model was called with a preprocessed image
        image_service.model.generate_caption.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_caption_image_model_error(self, image_service, sample_image_base64):
        """Test handling of model errors during captioning."""
        image_service.model.generate_caption = AsyncMock(side_effect=Exception("Model error"))
        
        with pytest.raises(Exception, match="Model error"):
            await image_service.caption_image(sample_image_base64)
    
    @pytest.mark.asyncio
    async def test_caption_image_empty_data(self, image_service):
        """Test captioning with empty image data."""
        with pytest.raises(ValueError, match="Image data cannot be empty"):
            await image_service.caption_image("")
    
    @pytest.mark.asyncio
    async def test_caption_image_invalid_max_length(self, image_service, sample_image_base64):
        """Test captioning with invalid max_length parameter."""
        with pytest.raises(ValueError, match="max_length must be positive"):
            await image_service.caption_image(
                sample_image_base64, max_length=0
            )


class TestVisualQuestionAnswering:
    """Test cases for visual question answering."""
    
    @pytest.mark.asyncio
    async def test_answer_visual_question_success(self, image_service, sample_image_base64):
        """Test successful visual question answering."""
        question = "What objects are in this image?"
        expected_answer = "There are mountains and trees in this image."
        
        image_service.model.answer_question = AsyncMock(return_value=expected_answer)
        
        result = await image_service.answer_visual_question(
            image_data=sample_image_base64,
            question=question
        )
        
        assert result == expected_answer
        image_service.model.answer_question.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_answer_visual_question_no_answer(self, image_service, sample_image_base64):
        """Test visual question answering when no answer is found."""
        question = "What is the meaning of life?"
        
        image_service.model.answer_question = AsyncMock(return_value=None)
        
        result = await image_service.answer_visual_question(
            image_data=sample_image_base64,
            question=question
        )
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_answer_visual_question_empty_image(self, image_service):
        """Test visual question answering with empty image data."""
        with pytest.raises(ValueError, match="Image data cannot be empty"):
            await image_service.answer_visual_question(
                image_data="",
                question="What is in this image?"
            )
    
    @pytest.mark.asyncio
    async def test_answer_visual_question_empty_question(self, image_service, sample_image_base64):
        """Test visual question answering with empty question."""
        with pytest.raises(ValueError, match="Question cannot be empty"):
            await image_service.answer_visual_question(
                image_data=sample_image_base64,
                question=""
            )


class TestDetailedImageDescription:
    """Test cases for detailed image description."""
    
    @pytest.mark.asyncio
    async def test_describe_image_detailed_success(self, image_service, sample_image_base64):
        """Test successful detailed image description."""
        expected_description = "This is a detailed description of the image with comprehensive analysis."
        image_service.model.generate_detailed_description = AsyncMock(return_value=expected_description)
        
        result = await image_service.describe_image_detailed(
            image_data=sample_image_base64,
            include_objects=True,
            include_scene=True,
            include_colors=True
        )
        
        assert "description" in result
        assert "properties" in result
        assert result["description"] == expected_description
        assert "width" in result["properties"]
        assert "height" in result["properties"]
    
    @pytest.mark.asyncio
    async def test_describe_image_detailed_minimal(self, image_service, sample_image_base64):
        """Test detailed image description with minimal options."""
        expected_description = "Basic image description"
        image_service.model.generate_detailed_description = AsyncMock(return_value=expected_description)
        
        result = await image_service.describe_image_detailed(
            image_data=sample_image_base64,
            include_objects=False,
            include_scene=False,
            include_colors=False
        )
        
        assert result["description"] == expected_description
        image_service.model.generate_detailed_description.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_describe_image_detailed_with_analysis(self, image_service, sample_image_base64):
        """Test detailed description with comprehensive analysis."""
        expected_description = "Comprehensive image analysis"
        image_service.model.generate_detailed_description = AsyncMock(return_value=expected_description)
        
        result = await image_service.describe_image_detailed(
            image_data=sample_image_base64,
            include_objects=True,
            include_scene=True,
            include_colors=True,
            include_text=True
        )
        
        assert "description" in result
        assert "properties" in result
        # Verify comprehensive analysis was requested
        call_args = image_service.model.generate_detailed_description.call_args
        assert call_args[1]["include_objects"] is True
        assert call_args[1]["include_scene"] is True
        assert call_args[1]["include_colors"] is True
        assert call_args[1]["include_text"] is True


class TestEnhancedCaptioning:
    """Test cases for enhanced captioning with analysis."""
    
    @pytest.mark.asyncio
    async def test_enhanced_caption_with_analysis(self, image_service, sample_image_base64):
        """Test enhanced captioning with image analysis."""
        expected_caption = "Enhanced caption with analysis"
        image_service.model.generate_caption = AsyncMock(return_value=expected_caption)
        
        result = await image_service.enhanced_caption(
            image_data=sample_image_base64,
            max_length=100,
            include_analysis=True
        )
        
        assert "caption" in result
        assert "analysis" in result
        assert result["caption"] == expected_caption
        assert "properties" in result["analysis"]
        assert "confidence" in result["analysis"]
    
    @pytest.mark.asyncio
    async def test_enhanced_caption_without_analysis(self, image_service, sample_image_base64):
        """Test enhanced captioning without analysis."""
        expected_caption = "Enhanced caption without analysis"
        image_service.model.generate_caption = AsyncMock(return_value=expected_caption)
        
        result = await image_service.enhanced_caption(
            image_data=sample_image_base64,
            max_length=100,
            include_analysis=False
        )
        
        assert "caption" in result
        assert "analysis" not in result
        assert result["caption"] == expected_caption
    
    @pytest.mark.asyncio
    async def test_enhanced_caption_with_custom_model(self, image_service, sample_image_base64):
        """Test enhanced captioning with custom model parameters."""
        expected_caption = "Custom model caption"
        image_service.model.generate_caption = AsyncMock(return_value=expected_caption)
        
        result = await image_service.enhanced_caption(
            image_data=sample_image_base64,
            max_length=100,
            model_params={"temperature": 0.7, "top_p": 0.9}
        )
        
        assert result["caption"] == expected_caption
        # Verify custom parameters were passed
        call_args = image_service.model.generate_caption.call_args
        assert "model_params" in call_args[1]


class TestBatchProcessing:
    """Test cases for batch image processing."""
    
    @pytest.mark.asyncio
    async def test_batch_caption_success(self, image_service):
        """Test successful batch image captioning."""
        image_data_list = ["base64_image_1", "base64_image_2"]
        expected_captions = ["Caption 1", "Caption 2"]
        
        # Mock the decode method to return valid images
        with patch.object(image_service, '_decode_base64_image') as mock_decode:
            mock_image = Mock(spec=Image.Image)
            mock_image.size = (100, 100)
            mock_decode.return_value = mock_image
            
            image_service.model.generate_caption = AsyncMock(side_effect=expected_captions)
            
            results = await image_service.batch_caption(
                image_data_list=image_data_list,
                max_length=50
            )
        
        assert len(results["results"]) == 2
        assert results["results"][0]["caption"] == "Caption 1"
        assert results["results"][1]["caption"] == "Caption 2"
        assert results["total_processed"] == 2
        assert results["successful"] == 2
        assert results["failed"] == 0
    
    @pytest.mark.asyncio
    async def test_batch_caption_partial_failure(self, image_service):
        """Test batch captioning with partial failures."""
        image_data_list = ["valid_image_1", "invalid_image", "valid_image_2"]
        
        def mock_decode(data):
            if "invalid" in data:
                raise ValueError("Invalid image")
            mock_image = Mock(spec=Image.Image)
            mock_image.size = (100, 100)
            return mock_image
        
        with patch.object(image_service, '_decode_base64_image', side_effect=mock_decode):
            image_service.model.generate_caption = AsyncMock(
                side_effect=lambda img, **kwargs: f"Caption for {img}"
            )
            
            results = await image_service.batch_caption(
                image_data_list=image_data_list,
                max_length=50
            )
        
        assert len(results["results"]) == 3
        assert "caption" in results["results"][0]
        assert "error" in results["results"][1]
        assert "caption" in results["results"][2]
        assert results["total_processed"] == 3
        assert results["successful"] == 2
        assert results["failed"] == 1
    
    @pytest.mark.asyncio
    async def test_batch_caption_concurrency_limit(self, image_service):
        """Test batch captioning with concurrency limit."""
        image_data_list = [f"image_{i}" for i in range(10)]
        
        call_times = []
        
        async def mock_caption(img, **kwargs):
            call_times.append(asyncio.get_event_loop().time())
            await asyncio.sleep(0.1)  # Simulate processing time
            return f"Caption for {img}"
        
        with patch.object(image_service, '_decode_base64_image') as mock_decode:
            mock_image = Mock(spec=Image.Image)
            mock_image.size = (100, 100)
            mock_decode.return_value = mock_image
            
            image_service.model.generate_caption = AsyncMock(side_effect=mock_caption)
            
            results = await image_service.batch_caption(
                image_data_list=image_data_list,
                max_length=50,
                max_concurrent=3
            )
        
        assert results["total_processed"] == 10
        assert results["successful"] == 10
        assert results["failed"] == 0
        
        # Verify concurrency was limited
        assert len(call_times) == 10
    
    @pytest.mark.asyncio
    async def test_batch_caption_empty_list(self, image_service):
        """Test batch captioning with empty image list."""
        results = await image_service.batch_caption(
            image_data_list=[],
            max_length=50
        )
        
        assert results["results"] == []
        assert results["total_processed"] == 0
        assert results["successful"] == 0
        assert results["failed"] == 0


class TestServiceStatistics:
    """Test cases for service statistics tracking."""
    
    @pytest.mark.asyncio
    async def test_stats_tracking_success(self, image_service, sample_image_base64):
        """Test statistics tracking for successful requests."""
        image_service.model.generate_caption = AsyncMock(return_value="Test caption")
        
        initial_stats = image_service.get_stats().copy()
        
        await image_service.caption_image(sample_image_base64)
        
        final_stats = image_service.get_stats()
        
        assert final_stats["total_requests"] == initial_stats["total_requests"] + 1
        assert final_stats["successful_requests"] == initial_stats["successful_requests"] + 1
        assert final_stats["failed_requests"] == initial_stats["failed_requests"]
        assert final_stats["total_processing_time"] > initial_stats["total_processing_time"]
    
    @pytest.mark.asyncio
    async def test_stats_tracking_failure(self, image_service, sample_image_base64):
        """Test statistics tracking for failed requests."""
        image_service.model.generate_caption = AsyncMock(side_effect=Exception("Test error"))
        
        initial_stats = image_service.get_stats().copy()
        
        with pytest.raises(Exception):
            await image_service.caption_image(sample_image_base64)
        
        final_stats = image_service.get_stats()
        
        assert final_stats["total_requests"] == initial_stats["total_requests"] + 1
        assert final_stats["successful_requests"] == initial_stats["successful_requests"]
        assert final_stats["failed_requests"] == initial_stats["failed_requests"] + 1
    
    def test_get_stats(self, image_service):
        """Test getting service statistics."""
        stats = image_service.get_stats()
        
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
    async def test_health_check_healthy(self, image_service):
        """Test health check when service is healthy."""
        image_service.model.is_loaded = Mock(return_value=True)
        image_service.model.get_model_info = Mock(return_value={
            "model_name": "test-captioner",
            "device": "cpu",
            "memory_usage_mb": 1024
        })
        
        health = await image_service.health_check()
        
        assert health["status"] == "healthy"
        assert health["model_loaded"] is True
        assert health["model_name"] == "test-captioner"
        assert "response_time_ms" in health
        assert "memory_usage_mb" in health
    
    @pytest.mark.asyncio
    async def test_health_check_model_not_loaded(self, image_service):
        """Test health check when model is not loaded."""
        image_service.model.is_loaded = Mock(return_value=False)
        
        health = await image_service.health_check()
        
        assert health["status"] == "unhealthy"
        assert health["model_loaded"] is False
        assert "error" in health
    
    @pytest.mark.asyncio
    async def test_health_check_exception(self, image_service):
        """Test health check when an exception occurs."""
        image_service.model.is_loaded = Mock(side_effect=Exception("Model error"))
        
        health = await image_service.health_check()
        
        assert health["status"] == "error"
        assert "error" in health
        assert "Model error" in health["error"]


class TestModelInfo:
    """Test cases for model information retrieval."""
    
    def test_get_model_info_success(self, image_service):
        """Test successful model info retrieval."""
        expected_info = {
            "model_name": "test-captioner",
            "is_loaded": True,
            "device": "cpu",
            "memory_usage_mb": 1024,
            "supported_formats": ["jpg", "png", "bmp"]
        }
        
        image_service.model.get_model_info = Mock(return_value=expected_info)
        
        info = image_service.get_model_info()
        
        assert info == expected_info
        image_service.model.get_model_info.assert_called_once()
    
    def test_get_model_info_exception(self, image_service):
        """Test model info retrieval when an exception occurs."""
        image_service.model.get_model_info = Mock(side_effect=Exception("Info error"))
        
        info = image_service.get_model_info()
        
        assert info["error"] == "Info error"
        assert info["is_loaded"] is False


# Performance tests
class TestImageServicePerformance:
    """Performance tests for image service."""
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_captioning_performance(self, image_service, sample_image_base64):
        """Test captioning performance with large image."""
        image_service.model.generate_caption = AsyncMock(return_value="Performance test caption")
        
        import time
        start_time = time.time()
        
        result = await image_service.caption_image(sample_image_base64)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        assert result == "Performance test caption"
        assert processing_time < 5.0  # Should complete within 5 seconds
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_batch_processing_performance(self, image_service):
        """Test batch processing performance."""
        image_data_list = [f"image_data_{i}" for i in range(20)]
        
        with patch.object(image_service, '_decode_base64_image') as mock_decode:
            mock_image = Mock(spec=Image.Image)
            mock_image.size = (100, 100)
            mock_decode.return_value = mock_image
            
            image_service.model.generate_caption = AsyncMock(
                side_effect=lambda img, **kwargs: f"Caption for {img}"
            )
            
            import time
            start_time = time.time()
            
            results = await image_service.batch_caption(
                image_data_list=image_data_list,
                max_length=50,
                max_concurrent=5
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
        
        assert results["total_processed"] == 20
        assert results["successful"] == 20
        assert processing_time < 10.0  # Should complete within 10 seconds