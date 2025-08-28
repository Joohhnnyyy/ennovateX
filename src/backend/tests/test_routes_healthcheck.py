"""Tests for health check routes.

This module contains tests for all health check and system monitoring endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import Mock, AsyncMock, patch
import json
import time
import psutil


class TestBasicHealthCheckRoute:
    """Test cases for basic health check endpoints."""
    
    def test_ping_endpoint(self, client: TestClient):
        """Test basic ping endpoint."""
        response = client.get("/api/v1/health/ping")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data
        assert "uptime_seconds" in data
    
    def test_readiness_check(self, client: TestClient):
        """Test readiness check endpoint."""
        with patch('app.routes.healthcheck.text_service') as mock_text_service, \
             patch('app.routes.healthcheck.image_service') as mock_image_service, \
             patch('app.routes.healthcheck.audio_service') as mock_audio_service:
            
            # Mock all services as healthy
            mock_text_service.health_check = AsyncMock(return_value={"status": "healthy"})
            mock_image_service.health_check = AsyncMock(return_value={"status": "healthy"})
            mock_audio_service.health_check = AsyncMock(return_value={"status": "healthy"})
            
            response = client.get("/api/v1/health/ready")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ready"
            assert "services" in data
            assert data["services"]["text_service"] == "healthy"
            assert data["services"]["image_service"] == "healthy"
            assert data["services"]["audio_service"] == "healthy"
    
    def test_readiness_check_service_unhealthy(self, client: TestClient):
        """Test readiness check when a service is unhealthy."""
        with patch('app.routes.healthcheck.text_service') as mock_text_service, \
             patch('app.routes.healthcheck.image_service') as mock_image_service, \
             patch('app.routes.healthcheck.audio_service') as mock_audio_service:
            
            # Mock text service as unhealthy
            mock_text_service.health_check = AsyncMock(return_value={"status": "unhealthy"})
            mock_image_service.health_check = AsyncMock(return_value={"status": "healthy"})
            mock_audio_service.health_check = AsyncMock(return_value={"status": "healthy"})
            
            response = client.get("/api/v1/health/ready")
            
            assert response.status_code == 503  # Service Unavailable
            data = response.json()
            assert data["status"] == "not_ready"
            assert data["services"]["text_service"] == "unhealthy"
    
    def test_liveness_check(self, client: TestClient):
        """Test liveness check endpoint."""
        response = client.get("/api/v1/health/live")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"
        assert "timestamp" in data
        assert "process_id" in data


class TestSystemResourcesRoute:
    """Test cases for system resources monitoring."""
    
    def test_get_system_resources(self, client: TestClient):
        """Test getting system resources information."""
        with patch('psutil.cpu_percent') as mock_cpu, \
             patch('psutil.virtual_memory') as mock_memory, \
             patch('psutil.disk_usage') as mock_disk:
            
            # Mock system resource data
            mock_cpu.return_value = 45.2
            mock_memory.return_value = Mock(
                total=16*1024*1024*1024,  # 16GB
                available=8*1024*1024*1024,  # 8GB
                percent=50.0,
                used=8*1024*1024*1024
            )
            mock_disk.return_value = Mock(
                total=500*1024*1024*1024,  # 500GB
                free=200*1024*1024*1024,   # 200GB
                used=300*1024*1024*1024,   # 300GB
                percent=60.0
            )
            
            response = client.get("/api/v1/health/system/resources")
            
            assert response.status_code == 200
            data = response.json()
            assert "cpu" in data
            assert "memory" in data
            assert "disk" in data
            assert data["cpu"]["usage_percent"] == 45.2
            assert data["memory"]["usage_percent"] == 50.0
            assert data["disk"]["usage_percent"] == 60.0
    
    def test_get_gpu_info(self, client: TestClient):
        """Test getting GPU information."""
        with patch('app.routes.healthcheck.get_gpu_info') as mock_gpu_info:
            mock_gpu_info.return_value = {
                "gpu_available": True,
                "gpu_count": 1,
                "gpus": [
                    {
                        "id": 0,
                        "name": "NVIDIA GeForce RTX 3080",
                        "memory_total_mb": 10240,
                        "memory_used_mb": 2048,
                        "memory_free_mb": 8192,
                        "utilization_percent": 25.0,
                        "temperature_celsius": 65
                    }
                ]
            }
            
            response = client.get("/api/v1/health/system/gpu")
            
            assert response.status_code == 200
            data = response.json()
            assert data["gpu_available"] is True
            assert data["gpu_count"] == 1
            assert len(data["gpus"]) == 1
            assert data["gpus"][0]["name"] == "NVIDIA GeForce RTX 3080"
    
    def test_get_gpu_info_no_gpu(self, client: TestClient):
        """Test getting GPU information when no GPU is available."""
        with patch('app.routes.healthcheck.get_gpu_info') as mock_gpu_info:
            mock_gpu_info.return_value = {
                "gpu_available": False,
                "gpu_count": 0,
                "gpus": [],
                "message": "No GPU detected"
            }
            
            response = client.get("/api/v1/health/system/gpu")
            
            assert response.status_code == 200
            data = response.json()
            assert data["gpu_available"] is False
            assert data["gpu_count"] == 0
            assert len(data["gpus"]) == 0


class TestServiceHealthRoute:
    """Test cases for individual service health checks."""
    
    def test_get_all_services_health(self, client: TestClient):
        """Test getting health status of all services."""
        with patch('app.routes.healthcheck.text_service') as mock_text_service, \
             patch('app.routes.healthcheck.image_service') as mock_image_service, \
             patch('app.routes.healthcheck.audio_service') as mock_audio_service:
            
            mock_text_service.health_check = AsyncMock(return_value={
                "status": "healthy",
                "model_loaded": True,
                "memory_usage_mb": 512,
                "response_time_ms": 15
            })
            mock_image_service.health_check = AsyncMock(return_value={
                "status": "healthy",
                "model_loaded": True,
                "memory_usage_mb": 1024,
                "response_time_ms": 25
            })
            mock_audio_service.health_check = AsyncMock(return_value={
                "status": "healthy",
                "model_loaded": True,
                "memory_usage_mb": 768,
                "response_time_ms": 35
            })
            
            response = client.get("/api/v1/health/services")
            
            assert response.status_code == 200
            data = response.json()
            assert "text_service" in data
            assert "image_service" in data
            assert "audio_service" in data
            assert data["text_service"]["status"] == "healthy"
            assert data["image_service"]["status"] == "healthy"
            assert data["audio_service"]["status"] == "healthy"
    
    def test_get_text_service_health(self, client: TestClient):
        """Test getting text service health specifically."""
        with patch('app.routes.healthcheck.text_service') as mock_service:
            mock_service.health_check = AsyncMock(return_value={
                "status": "healthy",
                "model_loaded": True,
                "model_name": "test-summarizer",
                "memory_usage_mb": 512,
                "last_request_time": time.time(),
                "response_time_ms": 15,
                "total_requests": 150
            })
            
            response = client.get("/api/v1/health/services/text")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["model_loaded"] is True
            assert data["model_name"] == "test-summarizer"
    
    def test_get_image_service_health(self, client: TestClient):
        """Test getting image service health specifically."""
        with patch('app.routes.healthcheck.image_service') as mock_service:
            mock_service.health_check = AsyncMock(return_value={
                "status": "healthy",
                "model_loaded": True,
                "model_name": "test-captioner",
                "memory_usage_mb": 1024,
                "gpu_available": False,
                "response_time_ms": 25
            })
            
            response = client.get("/api/v1/health/services/image")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["model_name"] == "test-captioner"
    
    def test_get_audio_service_health(self, client: TestClient):
        """Test getting audio service health specifically."""
        with patch('app.routes.healthcheck.audio_service') as mock_service:
            mock_service.health_check = AsyncMock(return_value={
                "status": "healthy",
                "model_loaded": True,
                "model_name": "test-asr",
                "memory_usage_mb": 768,
                "supported_formats": ["wav", "mp3"],
                "response_time_ms": 35
            })
            
            response = client.get("/api/v1/health/services/audio")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["model_name"] == "test-asr"
            assert "supported_formats" in data


class TestModelStatusRoute:
    """Test cases for model status monitoring."""
    
    def test_get_all_models_status(self, client: TestClient):
        """Test getting status of all loaded models."""
        with patch('app.routes.healthcheck.text_service') as mock_text_service, \
             patch('app.routes.healthcheck.image_service') as mock_image_service, \
             patch('app.routes.healthcheck.audio_service') as mock_audio_service:
            
            mock_text_service.get_model_info = Mock(return_value={
                "model_name": "test-summarizer",
                "is_loaded": True,
                "device": "cpu",
                "memory_usage_mb": 512
            })
            mock_image_service.get_model_info = Mock(return_value={
                "model_name": "test-captioner",
                "is_loaded": True,
                "device": "cpu",
                "memory_usage_mb": 1024
            })
            mock_audio_service.get_model_info = Mock(return_value={
                "model_name": "test-asr",
                "is_loaded": True,
                "device": "cpu",
                "memory_usage_mb": 768
            })
            
            response = client.get("/api/v1/health/models")
            
            assert response.status_code == 200
            data = response.json()
            assert "text_model" in data
            assert "image_model" in data
            assert "audio_model" in data
            assert data["text_model"]["is_loaded"] is True
            assert data["image_model"]["is_loaded"] is True
            assert data["audio_model"]["is_loaded"] is True
    
    def test_get_model_status_unloaded(self, client: TestClient):
        """Test getting model status when models are not loaded."""
        with patch('app.routes.healthcheck.text_service') as mock_text_service:
            mock_text_service.get_model_info = Mock(return_value={
                "model_name": "test-summarizer",
                "is_loaded": False,
                "device": None,
                "memory_usage_mb": 0,
                "error": "Model not initialized"
            })
            
            response = client.get("/api/v1/health/models")
            
            assert response.status_code == 200
            data = response.json()
            assert data["text_model"]["is_loaded"] is False
            assert "error" in data["text_model"]


class TestDetailedHealthRoute:
    """Test cases for detailed health status endpoint."""
    
    def test_get_detailed_health_status(self, client: TestClient):
        """Test getting comprehensive health status."""
        with patch('app.routes.healthcheck.text_service') as mock_text_service, \
             patch('app.routes.healthcheck.image_service') as mock_image_service, \
             patch('app.routes.healthcheck.audio_service') as mock_audio_service, \
             patch('psutil.cpu_percent') as mock_cpu, \
             patch('psutil.virtual_memory') as mock_memory:
            
            # Mock services
            mock_text_service.health_check = AsyncMock(return_value={"status": "healthy"})
            mock_image_service.health_check = AsyncMock(return_value={"status": "healthy"})
            mock_audio_service.health_check = AsyncMock(return_value={"status": "healthy"})
            
            # Mock system resources
            mock_cpu.return_value = 30.0
            mock_memory.return_value = Mock(percent=40.0)
            
            response = client.get("/api/v1/health/detailed")
            
            assert response.status_code == 200
            data = response.json()
            assert "overall_status" in data
            assert "services" in data
            assert "system_resources" in data
            assert "models" in data
            assert "timestamp" in data
            assert data["overall_status"] == "healthy"
    
    def test_get_detailed_health_status_degraded(self, client: TestClient):
        """Test detailed health status when system is degraded."""
        with patch('app.routes.healthcheck.text_service') as mock_text_service, \
             patch('app.routes.healthcheck.image_service') as mock_image_service, \
             patch('app.routes.healthcheck.audio_service') as mock_audio_service, \
             patch('psutil.cpu_percent') as mock_cpu, \
             patch('psutil.virtual_memory') as mock_memory:
            
            # Mock one service as unhealthy
            mock_text_service.health_check = AsyncMock(return_value={"status": "unhealthy"})
            mock_image_service.health_check = AsyncMock(return_value={"status": "healthy"})
            mock_audio_service.health_check = AsyncMock(return_value={"status": "healthy"})
            
            # Mock high resource usage
            mock_cpu.return_value = 95.0
            mock_memory.return_value = Mock(percent=90.0)
            
            response = client.get("/api/v1/health/detailed")
            
            assert response.status_code == 200
            data = response.json()
            assert data["overall_status"] == "degraded"
            assert "alerts" in data
            assert len(data["alerts"]) > 0


class TestHealthCheckErrorHandling:
    """Test error handling in health check routes."""
    
    def test_service_health_check_exception(self, client: TestClient):
        """Test handling of exceptions during service health checks."""
        with patch('app.routes.healthcheck.text_service') as mock_service:
            mock_service.health_check = AsyncMock(side_effect=Exception("Service error"))
            
            response = client.get("/api/v1/health/services/text")
            
            assert response.status_code == 200  # Should still return 200 but with error status
            data = response.json()
            assert data["status"] == "error"
            assert "error" in data
    
    def test_system_resources_exception(self, client: TestClient):
        """Test handling of exceptions when getting system resources."""
        with patch('psutil.cpu_percent') as mock_cpu:
            mock_cpu.side_effect = Exception("System error")
            
            response = client.get("/api/v1/health/system/resources")
            
            assert response.status_code == 500
    
    def test_gpu_info_exception(self, client: TestClient):
        """Test handling of exceptions when getting GPU info."""
        with patch('app.routes.healthcheck.get_gpu_info') as mock_gpu_info:
            mock_gpu_info.side_effect = Exception("GPU error")
            
            response = client.get("/api/v1/health/system/gpu")
            
            assert response.status_code == 500


class TestHealthCheckPerformance:
    """Performance tests for health check routes."""
    
    @pytest.mark.performance
    def test_ping_response_time(self, client: TestClient):
        """Test that ping endpoint responds quickly."""
        start_time = time.time()
        response = client.get("/api/v1/health/ping")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 0.1  # Should respond within 100ms
    
    @pytest.mark.performance
    def test_readiness_check_performance(self, client: TestClient):
        """Test readiness check performance."""
        with patch('app.routes.healthcheck.text_service') as mock_text_service, \
             patch('app.routes.healthcheck.image_service') as mock_image_service, \
             patch('app.routes.healthcheck.audio_service') as mock_audio_service:
            
            mock_text_service.health_check = AsyncMock(return_value={"status": "healthy"})
            mock_image_service.health_check = AsyncMock(return_value={"status": "healthy"})
            mock_audio_service.health_check = AsyncMock(return_value={"status": "healthy"})
            
            start_time = time.time()
            response = client.get("/api/v1/health/ready")
            end_time = time.time()
            
            assert response.status_code == 200
            assert (end_time - start_time) < 1.0  # Should complete within 1 second


# Integration tests
class TestHealthCheckIntegration:
    """Integration tests for health check routes."""
    
    @pytest.mark.integration
    def test_full_health_check_workflow(self, client: TestClient):
        """Test complete health check workflow."""
        # Test basic ping
        ping_response = client.get("/api/v1/health/ping")
        assert ping_response.status_code == 200
        
        # Test liveness
        live_response = client.get("/api/v1/health/live")
        assert live_response.status_code == 200
        
        # Test readiness with mocked services
        with patch('app.routes.healthcheck.text_service') as mock_text_service, \
             patch('app.routes.healthcheck.image_service') as mock_image_service, \
             patch('app.routes.healthcheck.audio_service') as mock_audio_service:
            
            mock_text_service.health_check = AsyncMock(return_value={"status": "healthy"})
            mock_image_service.health_check = AsyncMock(return_value={"status": "healthy"})
            mock_audio_service.health_check = AsyncMock(return_value={"status": "healthy"})
            
            ready_response = client.get("/api/v1/health/ready")
            assert ready_response.status_code == 200
        
        # Test detailed health status
        with patch('app.routes.healthcheck.text_service') as mock_text_service, \
             patch('app.routes.healthcheck.image_service') as mock_image_service, \
             patch('app.routes.healthcheck.audio_service') as mock_audio_service:
            
            mock_text_service.health_check = AsyncMock(return_value={"status": "healthy"})
            mock_image_service.health_check = AsyncMock(return_value={"status": "healthy"})
            mock_audio_service.health_check = AsyncMock(return_value={"status": "healthy"})
            
            detailed_response = client.get("/api/v1/health/detailed")
            assert detailed_response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_async_health_checks(self, async_client: AsyncClient):
        """Test async health check endpoints."""
        with patch('app.routes.healthcheck.text_service') as mock_text_service:
            mock_text_service.health_check = AsyncMock(return_value={"status": "healthy"})
            
            response = await async_client.get("/api/v1/health/services/text")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"