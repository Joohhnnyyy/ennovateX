"""Tests for text processing routes.

This module contains tests for all text-related API endpoints including
summarization, question answering, and batch processing.
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import Mock, AsyncMock, patch
import json
import time


class TestTextSummarizationRoute:
    """Test cases for text summarization endpoint."""
    
    def test_summarize_text_success(self, client: TestClient, text_summarization_request_data: dict):
        """Test successful text summarization."""
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.summarize_text = AsyncMock(return_value={
                "summary": "This is a test summary.",
                "original_length": 100,
                "summary_length": 25,
                "compression_ratio": 0.25,
                "processing_time": 0.5,
                "model_used": "test-model",
                "confidence": 0.95
            })
            
            response = client.post("/api/v1/text/summarize", json=text_summarization_request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "summary" in data
            assert "processing_time" in data
            assert "confidence" in data
            assert data["summary"] == "This is a test summary."
    
    def test_summarize_text_invalid_input(self, client: TestClient):
        """Test text summarization with invalid input."""
        invalid_data = {
            "text": "",  # Empty text
            "max_length": -1  # Invalid max_length
        }
        
        response = client.post("/api/v1/text/summarize", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_summarize_text_missing_fields(self, client: TestClient):
        """Test text summarization with missing required fields."""
        incomplete_data = {
            "max_length": 50
            # Missing 'text' field
        }
        
        response = client.post("/api/v1/text/summarize", json=incomplete_data)
        assert response.status_code == 422
    
    def test_summarize_text_with_analysis(self, client: TestClient):
        """Test text summarization with analysis enabled."""
        request_data = {
            "text": "Sample text for analysis.",
            "max_length": 50,
            "include_analysis": True
        }
        
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.summarize_text = AsyncMock(return_value={
                "summary": "Analyzed summary.",
                "analysis": {
                    "readability_score": 85.5,
                    "key_phrases": ["sample", "analysis"]
                },
                "processing_time": 0.8
            })
            
            response = client.post("/api/v1/text/summarize", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "analysis" in data
            assert "readability_score" in data["analysis"]
    
    @pytest.mark.asyncio
    async def test_summarize_text_async(self, async_client: AsyncClient, text_summarization_request_data: dict):
        """Test async text summarization."""
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.summarize_text = AsyncMock(return_value={
                "summary": "Async test summary.",
                "processing_time": 0.3
            })
            
            response = await async_client.post("/api/v1/text/summarize", json=text_summarization_request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["summary"] == "Async test summary."


class TestTextQuestionAnsweringRoute:
    """Test cases for text question answering endpoint."""
    
    def test_question_answer_success(self, client: TestClient):
        """Test successful question answering."""
        request_data = {
            "text": "The capital of France is Paris. It is known for the Eiffel Tower.",
            "question": "What is the capital of France?",
            "max_answer_length": 50
        }
        
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.answer_question = AsyncMock(return_value={
                "answer": "Paris",
                "confidence": 0.98,
                "context_start": 20,
                "context_end": 25,
                "processing_time": 0.4
            })
            
            response = client.post("/api/v1/text/question-answer", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["answer"] == "Paris"
            assert data["confidence"] == 0.98
    
    def test_question_answer_no_answer_found(self, client: TestClient):
        """Test question answering when no answer is found."""
        request_data = {
            "text": "This text doesn't contain the answer.",
            "question": "What is the capital of Mars?",
            "max_answer_length": 50
        }
        
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.answer_question = AsyncMock(return_value={
                "answer": "No answer found",
                "confidence": 0.1,
                "processing_time": 0.2
            })
            
            response = client.post("/api/v1/text/question-answer", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "No answer found" in data["answer"]
            assert data["confidence"] < 0.5


class TestTextBatchProcessingRoute:
    """Test cases for batch text processing endpoint."""
    
    def test_batch_summarize_success(self, client: TestClient):
        """Test successful batch text summarization."""
        request_data = {
            "texts": [
                "First text to summarize.",
                "Second text to summarize.",
                "Third text to summarize."
            ],
            "max_length": 30,
            "batch_size": 2
        }
        
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.batch_summarize = AsyncMock(return_value={
                "summaries": [
                    {"summary": "First summary", "processing_time": 0.3},
                    {"summary": "Second summary", "processing_time": 0.4},
                    {"summary": "Third summary", "processing_time": 0.2}
                ],
                "total_processing_time": 0.9,
                "successful_count": 3,
                "failed_count": 0
            })
            
            response = client.post("/api/v1/text/batch-summarize", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert len(data["summaries"]) == 3
            assert data["successful_count"] == 3
            assert data["failed_count"] == 0
    
    def test_batch_summarize_partial_failure(self, client: TestClient):
        """Test batch summarization with some failures."""
        request_data = {
            "texts": ["Valid text", "", "Another valid text"],  # Empty text should fail
            "max_length": 30
        }
        
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.batch_summarize = AsyncMock(return_value={
                "summaries": [
                    {"summary": "Valid summary", "processing_time": 0.3},
                    {"error": "Empty text provided", "processing_time": 0.0},
                    {"summary": "Another summary", "processing_time": 0.4}
                ],
                "total_processing_time": 0.7,
                "successful_count": 2,
                "failed_count": 1
            })
            
            response = client.post("/api/v1/text/batch-summarize", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["successful_count"] == 2
            assert data["failed_count"] == 1
    
    def test_batch_summarize_empty_list(self, client: TestClient):
        """Test batch summarization with empty text list."""
        request_data = {
            "texts": [],
            "max_length": 30
        }
        
        response = client.post("/api/v1/text/batch-summarize", json=request_data)
        assert response.status_code == 422  # Validation error


class TestTextServiceInfoRoute:
    """Test cases for text service information endpoints."""
    
    def test_get_text_models_info(self, client: TestClient):
        """Test getting text models information."""
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.get_model_info = Mock(return_value={
                "model_name": "test-summarizer",
                "model_type": "transformer",
                "device": "cpu",
                "memory_usage_mb": 512,
                "is_loaded": True,
                "supported_languages": ["en", "es", "fr"]
            })
            
            response = client.get("/api/v1/text/models/info")
            
            assert response.status_code == 200
            data = response.json()
            assert data["model_name"] == "test-summarizer"
            assert data["is_loaded"] is True
    
    def test_get_text_service_stats(self, client: TestClient):
        """Test getting text service statistics."""
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.get_stats = Mock(return_value={
                "total_requests": 150,
                "successful_requests": 145,
                "failed_requests": 5,
                "average_processing_time": 0.8,
                "total_processing_time": 120.0,
                "uptime_seconds": 3600
            })
            
            response = client.get("/api/v1/text/stats")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_requests"] == 150
            assert data["successful_requests"] == 145
    
    def test_text_service_health_check(self, client: TestClient):
        """Test text service health check."""
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.health_check = AsyncMock(return_value={
                "status": "healthy",
                "model_loaded": True,
                "memory_usage_mb": 256,
                "last_request_time": time.time(),
                "response_time_ms": 15
            })
            
            response = client.get("/api/v1/text/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["model_loaded"] is True


class TestTextRouteErrorHandling:
    """Test error handling in text routes."""
    
    def test_service_unavailable_error(self, client: TestClient, text_summarization_request_data: dict):
        """Test handling of service unavailable errors."""
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.summarize_text = AsyncMock(side_effect=Exception("Service unavailable"))
            
            response = client.post("/api/v1/text/summarize", json=text_summarization_request_data)
            
            assert response.status_code == 500
    
    def test_timeout_error(self, client: TestClient, text_summarization_request_data: dict):
        """Test handling of timeout errors."""
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.summarize_text = AsyncMock(side_effect=TimeoutError("Request timeout"))
            
            response = client.post("/api/v1/text/summarize", json=text_summarization_request_data)
            
            assert response.status_code == 500
    
    def test_invalid_json_format(self, client: TestClient):
        """Test handling of invalid JSON format."""
        response = client.post(
            "/api/v1/text/summarize",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422


class TestTextRoutePerformance:
    """Performance tests for text routes."""
    
    @pytest.mark.performance
    def test_summarization_performance(self, client: TestClient, performance_threshold: dict):
        """Test that text summarization meets performance requirements."""
        request_data = {
            "text": "A" * 1000,  # Large text
            "max_length": 100
        }
        
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.summarize_text = AsyncMock(return_value={
                "summary": "Performance test summary.",
                "processing_time": 0.5
            })
            
            start_time = time.time()
            response = client.post("/api/v1/text/summarize", json=request_data)
            end_time = time.time()
            
            assert response.status_code == 200
            assert (end_time - start_time) < performance_threshold["text_summarization_max_time"]
    
    @pytest.mark.performance
    def test_batch_processing_performance(self, client: TestClient):
        """Test batch processing performance with multiple texts."""
        request_data = {
            "texts": [f"Text number {i}" for i in range(10)],
            "max_length": 50
        }
        
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.batch_summarize = AsyncMock(return_value={
                "summaries": [{"summary": f"Summary {i}"} for i in range(10)],
                "total_processing_time": 2.0,
                "successful_count": 10,
                "failed_count": 0
            })
            
            start_time = time.time()
            response = client.post("/api/v1/text/batch-summarize", json=request_data)
            end_time = time.time()
            
            assert response.status_code == 200
            assert (end_time - start_time) < 5.0  # Should complete within 5 seconds


# Integration tests
class TestTextRouteIntegration:
    """Integration tests for text routes."""
    
    @pytest.mark.integration
    def test_full_text_processing_workflow(self, client: TestClient):
        """Test complete text processing workflow."""
        # First, check service health
        health_response = client.get("/api/v1/text/health")
        assert health_response.status_code == 200
        
        # Then, get model info
        info_response = client.get("/api/v1/text/models/info")
        assert info_response.status_code == 200
        
        # Finally, process text
        with patch('app.routes.text.text_service') as mock_service:
            mock_service.health_check = AsyncMock(return_value={"status": "healthy"})
            mock_service.get_model_info = Mock(return_value={"model_name": "test"})
            mock_service.summarize_text = AsyncMock(return_value={"summary": "Test"})
            
            process_response = client.post("/api/v1/text/summarize", json={
                "text": "Sample text for processing",
                "max_length": 50
            })
            assert process_response.status_code == 200