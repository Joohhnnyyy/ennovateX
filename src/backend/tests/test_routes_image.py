"""Tests for image processing routes.

This module contains tests for all image-related API endpoints including
captioning, visual question answering, and batch processing.
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import Mock, AsyncMock, patch
import json
import time
import base64


class TestImageCaptioningRoute:
    """Test cases for image captioning endpoint."""
    
    def test_caption_image_success(self, client: TestClient, image_captioning_request_data: dict):
        """Test successful image captioning."""
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.caption_image = AsyncMock(return_value={
                "caption": "A beautiful landscape with mountains and trees.",
                "confidence": 0.92,
                "processing_time": 0.8,
                "model_used": "test-captioner",
                "image_properties": {
                    "width": 1024,
                    "height": 768,
                    "format": "JPEG",
                    "size_bytes": 204800
                }
            })
            
            response = client.post("/api/v1/image/caption", json=image_captioning_request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "caption" in data
            assert "confidence" in data
            assert "processing_time" in data
            assert data["caption"] == "A beautiful landscape with mountains and trees."
    
    def test_caption_image_invalid_base64(self, client: TestClient):
        """Test image captioning with invalid base64 data."""
        invalid_data = {
            "image_data": "invalid_base64_data",
            "max_length": 50
        }
        
        response = client.post("/api/v1/image/caption", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_caption_image_missing_data(self, client: TestClient):
        """Test image captioning with missing image data."""
        incomplete_data = {
            "max_length": 50
            # Missing 'image_data' field
        }
        
        response = client.post("/api/v1/image/caption", json=incomplete_data)
        assert response.status_code == 422
    
    def test_caption_image_with_analysis(self, client: TestClient, sample_base64_image: str):
        """Test image captioning with analysis enabled."""
        request_data = {
            "image_data": sample_base64_image,
            "max_length": 50,
            "include_analysis": True
        }
        
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.caption_image = AsyncMock(return_value={
                "caption": "Analyzed image caption.",
                "analysis": {
                    "dominant_colors": ["blue", "green", "white"],
                    "detected_objects": ["mountain", "tree", "sky"],
                    "scene_type": "landscape",
                    "lighting_conditions": "daylight"
                },
                "confidence": 0.88,
                "processing_time": 1.2
            })
            
            response = client.post("/api/v1/image/caption", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "analysis" in data
            assert "dominant_colors" in data["analysis"]
    
    @pytest.mark.asyncio
    async def test_caption_image_async(self, async_client: AsyncClient, image_captioning_request_data: dict):
        """Test async image captioning."""
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.caption_image = AsyncMock(return_value={
                "caption": "Async test caption.",
                "confidence": 0.85,
                "processing_time": 0.6
            })
            
            response = await async_client.post("/api/v1/image/caption", json=image_captioning_request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["caption"] == "Async test caption."


class TestVisualQuestionAnsweringRoute:
    """Test cases for visual question answering endpoint."""
    
    def test_visual_qa_success(self, client: TestClient, sample_base64_image: str):
        """Test successful visual question answering."""
        request_data = {
            "image_data": sample_base64_image,
            "question": "What color is the sky in this image?",
            "max_answer_length": 50
        }
        
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.visual_question_answer = AsyncMock(return_value={
                "answer": "The sky is blue.",
                "confidence": 0.94,
                "processing_time": 1.1,
                "attention_regions": [
                    {"x": 0, "y": 0, "width": 100, "height": 50, "confidence": 0.9}
                ]
            })
            
            response = client.post("/api/v1/image/visual-qa", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["answer"] == "The sky is blue."
            assert data["confidence"] == 0.94
    
    def test_visual_qa_no_answer_found(self, client: TestClient, sample_base64_image: str):
        """Test visual QA when no answer is found."""
        request_data = {
            "image_data": sample_base64_image,
            "question": "What is the temperature in this image?",
            "max_answer_length": 50
        }
        
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.visual_question_answer = AsyncMock(return_value={
                "answer": "Cannot determine from the image.",
                "confidence": 0.2,
                "processing_time": 0.8
            })
            
            response = client.post("/api/v1/image/visual-qa", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "Cannot determine" in data["answer"]
            assert data["confidence"] < 0.5
    
    def test_visual_qa_invalid_question(self, client: TestClient, sample_base64_image: str):
        """Test visual QA with invalid question."""
        request_data = {
            "image_data": sample_base64_image,
            "question": "",  # Empty question
            "max_answer_length": 50
        }
        
        response = client.post("/api/v1/image/visual-qa", json=request_data)
        assert response.status_code == 422  # Validation error


class TestImageBatchProcessingRoute:
    """Test cases for batch image processing endpoint."""
    
    def test_batch_caption_success(self, client: TestClient, sample_base64_image: str):
        """Test successful batch image captioning."""
        request_data = {
            "images": [
                {"image_data": sample_base64_image, "image_id": "img1"},
                {"image_data": sample_base64_image, "image_id": "img2"},
                {"image_data": sample_base64_image, "image_id": "img3"}
            ],
            "max_length": 50,
            "batch_size": 2
        }
        
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.batch_caption = AsyncMock(return_value={
                "captions": [
                    {"image_id": "img1", "caption": "First image caption", "processing_time": 0.8},
                    {"image_id": "img2", "caption": "Second image caption", "processing_time": 0.9},
                    {"image_id": "img3", "caption": "Third image caption", "processing_time": 0.7}
                ],
                "total_processing_time": 2.4,
                "successful_count": 3,
                "failed_count": 0,
                "performance_metrics": {
                    "average_processing_time": 0.8,
                    "throughput_images_per_second": 1.25
                }
            })
            
            response = client.post("/api/v1/image/batch-caption", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert len(data["captions"]) == 3
            assert data["successful_count"] == 3
            assert data["failed_count"] == 0
    
    def test_batch_caption_partial_failure(self, client: TestClient, sample_base64_image: str):
        """Test batch captioning with some failures."""
        request_data = {
            "images": [
                {"image_data": sample_base64_image, "image_id": "img1"},
                {"image_data": "invalid_data", "image_id": "img2"},
                {"image_data": sample_base64_image, "image_id": "img3"}
            ],
            "max_length": 50
        }
        
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.batch_caption = AsyncMock(return_value={
                "captions": [
                    {"image_id": "img1", "caption": "Valid caption", "processing_time": 0.8},
                    {"image_id": "img2", "error": "Invalid image data", "processing_time": 0.0},
                    {"image_id": "img3", "caption": "Another valid caption", "processing_time": 0.9}
                ],
                "total_processing_time": 1.7,
                "successful_count": 2,
                "failed_count": 1
            })
            
            response = client.post("/api/v1/image/batch-caption", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["successful_count"] == 2
            assert data["failed_count"] == 1
    
    def test_batch_caption_empty_list(self, client: TestClient):
        """Test batch captioning with empty image list."""
        request_data = {
            "images": [],
            "max_length": 50
        }
        
        response = client.post("/api/v1/image/batch-caption", json=request_data)
        assert response.status_code == 422  # Validation error


class TestImageDetailedDescriptionRoute:
    """Test cases for detailed image description endpoint."""
    
    def test_detailed_description_success(self, client: TestClient, sample_base64_image: str):
        """Test successful detailed image description."""
        request_data = {
            "image_data": sample_base64_image,
            "detail_level": "high",
            "include_objects": True,
            "include_scene_analysis": True
        }
        
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.get_detailed_description = AsyncMock(return_value={
                "description": "A detailed description of the image with comprehensive analysis.",
                "objects": [
                    {"name": "tree", "confidence": 0.95, "bbox": [10, 20, 100, 200]},
                    {"name": "mountain", "confidence": 0.88, "bbox": [200, 50, 400, 300]}
                ],
                "scene_analysis": {
                    "scene_type": "outdoor_landscape",
                    "lighting": "natural_daylight",
                    "weather": "clear",
                    "time_of_day": "afternoon"
                },
                "processing_time": 2.1,
                "confidence": 0.91
            })
            
            response = client.post("/api/v1/image/detailed-description", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "description" in data
            assert "objects" in data
            assert "scene_analysis" in data
            assert len(data["objects"]) == 2
    
    def test_detailed_description_minimal(self, client: TestClient, sample_base64_image: str):
        """Test detailed description with minimal options."""
        request_data = {
            "image_data": sample_base64_image,
            "detail_level": "low",
            "include_objects": False,
            "include_scene_analysis": False
        }
        
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.get_detailed_description = AsyncMock(return_value={
                "description": "A simple description of the image.",
                "processing_time": 0.5,
                "confidence": 0.85
            })
            
            response = client.post("/api/v1/image/detailed-description", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "description" in data
            assert "objects" not in data
            assert "scene_analysis" not in data


class TestImageServiceInfoRoute:
    """Test cases for image service information endpoints."""
    
    def test_get_image_models_info(self, client: TestClient):
        """Test getting image models information."""
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.get_model_info = Mock(return_value={
                "model_name": "test-captioner",
                "model_type": "vision_transformer",
                "device": "cpu",
                "memory_usage_mb": 1024,
                "is_loaded": True,
                "supported_formats": ["JPEG", "PNG", "WEBP"],
                "max_image_size": {"width": 2048, "height": 2048}
            })
            
            response = client.get("/api/v1/image/models/info")
            
            assert response.status_code == 200
            data = response.json()
            assert data["model_name"] == "test-captioner"
            assert data["is_loaded"] is True
            assert "supported_formats" in data
    
    def test_get_image_service_stats(self, client: TestClient):
        """Test getting image service statistics."""
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.get_stats = Mock(return_value={
                "total_requests": 75,
                "successful_requests": 72,
                "failed_requests": 3,
                "average_processing_time": 1.2,
                "total_processing_time": 90.0,
                "images_processed": 72,
                "average_image_size_mb": 2.5
            })
            
            response = client.get("/api/v1/image/stats")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_requests"] == 75
            assert data["images_processed"] == 72
    
    def test_image_service_health_check(self, client: TestClient):
        """Test image service health check."""
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.health_check = AsyncMock(return_value={
                "status": "healthy",
                "model_loaded": True,
                "memory_usage_mb": 512,
                "gpu_available": False,
                "last_request_time": time.time(),
                "response_time_ms": 25
            })
            
            response = client.get("/api/v1/image/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["model_loaded"] is True


class TestImageRouteErrorHandling:
    """Test error handling in image routes."""
    
    def test_service_unavailable_error(self, client: TestClient, image_captioning_request_data: dict):
        """Test handling of service unavailable errors."""
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.caption_image = AsyncMock(side_effect=Exception("Service unavailable"))
            
            response = client.post("/api/v1/image/caption", json=image_captioning_request_data)
            
            assert response.status_code == 500
    
    def test_image_processing_error(self, client: TestClient, sample_base64_image: str):
        """Test handling of image processing errors."""
        request_data = {
            "image_data": sample_base64_image,
            "max_length": 50
        }
        
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.caption_image = AsyncMock(side_effect=ValueError("Invalid image format"))
            
            response = client.post("/api/v1/image/caption", json=request_data)
            
            assert response.status_code == 500
    
    def test_memory_error(self, client: TestClient, image_captioning_request_data: dict):
        """Test handling of memory errors."""
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.caption_image = AsyncMock(side_effect=MemoryError("Out of memory"))
            
            response = client.post("/api/v1/image/caption", json=image_captioning_request_data)
            
            assert response.status_code == 500


class TestImageRoutePerformance:
    """Performance tests for image routes."""
    
    @pytest.mark.performance
    def test_captioning_performance(self, client: TestClient, performance_threshold: dict, sample_base64_image: str):
        """Test that image captioning meets performance requirements."""
        request_data = {
            "image_data": sample_base64_image,
            "max_length": 100
        }
        
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.caption_image = AsyncMock(return_value={
                "caption": "Performance test caption.",
                "processing_time": 1.0
            })
            
            start_time = time.time()
            response = client.post("/api/v1/image/caption", json=request_data)
            end_time = time.time()
            
            assert response.status_code == 200
            assert (end_time - start_time) < performance_threshold["image_captioning_max_time"]
    
    @pytest.mark.performance
    def test_batch_processing_performance(self, client: TestClient, sample_base64_image: str):
        """Test batch processing performance with multiple images."""
        request_data = {
            "images": [
                {"image_data": sample_base64_image, "image_id": f"img{i}"} 
                for i in range(5)
            ],
            "max_length": 50
        }
        
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.batch_caption = AsyncMock(return_value={
                "captions": [{"image_id": f"img{i}", "caption": f"Caption {i}"} for i in range(5)],
                "total_processing_time": 4.0,
                "successful_count": 5,
                "failed_count": 0
            })
            
            start_time = time.time()
            response = client.post("/api/v1/image/batch-caption", json=request_data)
            end_time = time.time()
            
            assert response.status_code == 200
            assert (end_time - start_time) < 8.0  # Should complete within 8 seconds


# Integration tests
class TestImageRouteIntegration:
    """Integration tests for image routes."""
    
    @pytest.mark.integration
    def test_full_image_processing_workflow(self, client: TestClient, sample_base64_image: str):
        """Test complete image processing workflow."""
        # First, check service health
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.health_check = AsyncMock(return_value={"status": "healthy"})
            health_response = client.get("/api/v1/image/health")
            assert health_response.status_code == 200
        
        # Then, get model info
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.get_model_info = Mock(return_value={"model_name": "test"})
            info_response = client.get("/api/v1/image/models/info")
            assert info_response.status_code == 200
        
        # Finally, process image
        with patch('app.routes.image.image_service') as mock_service:
            mock_service.caption_image = AsyncMock(return_value={"caption": "Test caption"})
            process_response = client.post("/api/v1/image/caption", json={
                "image_data": sample_base64_image,
                "max_length": 50
            })
            assert process_response.status_code == 200