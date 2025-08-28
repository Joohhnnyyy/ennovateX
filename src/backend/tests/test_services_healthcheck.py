"""Tests for healthcheck service.

This module contains tests for system monitoring and health check functionality.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import asyncio
import psutil
from app.services.healthcheck_service import HealthCheckService


class TestHealthCheckServiceInitialization:
    """Test cases for HealthCheckService initialization."""
    
    def test_healthcheck_service_init(self):
        """Test HealthCheckService initialization."""
        service = HealthCheckService()
        
        assert hasattr(service, 'start_time')
        assert service.start_time is not None
        assert hasattr(service, 'alerts')
        assert isinstance(service.alerts, list)


class TestBasicHealthChecks:
    """Test cases for basic health check methods."""
    
    def test_ping(self, healthcheck_service):
        """Test basic ping functionality."""
        result = healthcheck_service.ping()
        
        assert result["status"] == "ok"
        assert "timestamp" in result
        assert "uptime_seconds" in result
        assert isinstance(result["uptime_seconds"], float)
    
    @pytest.mark.asyncio
    async def test_readiness_check_all_healthy(self, healthcheck_service):
        """Test readiness check when all services are healthy."""
        # Mock all service health checks to return healthy
        with patch.object(healthcheck_service, '_check_text_service_health') as mock_text, \
             patch.object(healthcheck_service, '_check_image_service_health') as mock_image, \
             patch.object(healthcheck_service, '_check_audio_service_health') as mock_audio:
            
            mock_text.return_value = {"status": "healthy", "model_loaded": True}
            mock_image.return_value = {"status": "healthy", "model_loaded": True}
            mock_audio.return_value = {"status": "healthy", "model_loaded": True}
            
            result = await healthcheck_service.readiness_check()
        
        assert result["ready"] is True
        assert result["status"] == "ready"
        assert "services" in result
        assert len(result["services"]) == 3
    
    @pytest.mark.asyncio
    async def test_readiness_check_service_unhealthy(self, healthcheck_service):
        """Test readiness check when a service is unhealthy."""
        with patch.object(healthcheck_service, '_check_text_service_health') as mock_text, \
             patch.object(healthcheck_service, '_check_image_service_health') as mock_image, \
             patch.object(healthcheck_service, '_check_audio_service_health') as mock_audio:
            
            mock_text.return_value = {"status": "unhealthy", "model_loaded": False}
            mock_image.return_value = {"status": "healthy", "model_loaded": True}
            mock_audio.return_value = {"status": "healthy", "model_loaded": True}
            
            result = await healthcheck_service.readiness_check()
        
        assert result["ready"] is False
        assert result["status"] == "not_ready"
        assert "unhealthy_services" in result
        assert "text" in result["unhealthy_services"]
    
    @pytest.mark.asyncio
    async def test_liveness_check_healthy(self, healthcheck_service):
        """Test liveness check when system is healthy."""
        with patch('psutil.cpu_percent', return_value=45.0), \
             patch('psutil.virtual_memory') as mock_memory:
            
            mock_memory.return_value.percent = 60.0
            
            result = await healthcheck_service.liveness_check()
        
        assert result["alive"] is True
        assert result["status"] == "alive"
        assert "system_resources" in result
        assert result["system_resources"]["cpu_usage_percent"] == 45.0
        assert result["system_resources"]["memory_usage_percent"] == 60.0
    
    @pytest.mark.asyncio
    async def test_liveness_check_high_resource_usage(self, healthcheck_service):
        """Test liveness check with high resource usage."""
        with patch('psutil.cpu_percent', return_value=95.0), \
             patch('psutil.virtual_memory') as mock_memory:
            
            mock_memory.return_value.percent = 98.0
            
            result = await healthcheck_service.liveness_check()
        
        assert result["alive"] is False
        assert result["status"] == "critical"
        assert "alerts" in result
        assert len(result["alerts"]) > 0


class TestSystemResourceMonitoring:
    """Test cases for system resource monitoring."""
    
    def test_get_system_resources(self, healthcheck_service):
        """Test system resource information retrieval."""
        with patch('psutil.cpu_percent', return_value=35.5), \
             patch('psutil.virtual_memory') as mock_memory, \
             patch('psutil.disk_usage') as mock_disk:
            
            # Mock memory info
            mock_memory.return_value.total = 16 * 1024**3  # 16GB
            mock_memory.return_value.available = 8 * 1024**3  # 8GB
            mock_memory.return_value.percent = 50.0
            
            # Mock disk info
            mock_disk.return_value.total = 500 * 1024**3  # 500GB
            mock_disk.return_value.free = 200 * 1024**3  # 200GB
            mock_disk.return_value.percent = 60.0
            
            resources = healthcheck_service.get_system_resources()
        
        assert "cpu" in resources
        assert "memory" in resources
        assert "disk" in resources
        
        assert resources["cpu"]["usage_percent"] == 35.5
        assert resources["memory"]["usage_percent"] == 50.0
        assert resources["disk"]["usage_percent"] == 60.0
        
        assert "total_gb" in resources["memory"]
        assert "available_gb" in resources["memory"]
        assert "total_gb" in resources["disk"]
        assert "free_gb" in resources["disk"]
    
    def test_get_gpu_info_available(self, healthcheck_service):
        """Test GPU information when GPU is available."""
        mock_gpu_info = {
            "gpu_count": 1,
            "gpus": [
                {
                    "id": 0,
                    "name": "NVIDIA RTX 4090",
                    "memory_total_mb": 24576,
                    "memory_used_mb": 8192,
                    "memory_free_mb": 16384,
                    "utilization_percent": 75.0,
                    "temperature_c": 65
                }
            ]
        }
        
        with patch.object(healthcheck_service, '_get_gpu_info', return_value=mock_gpu_info):
            gpu_info = healthcheck_service.get_gpu_info()
        
        assert gpu_info["gpu_count"] == 1
        assert len(gpu_info["gpus"]) == 1
        assert gpu_info["gpus"][0]["name"] == "NVIDIA RTX 4090"
        assert gpu_info["gpus"][0]["utilization_percent"] == 75.0
    
    def test_get_gpu_info_not_available(self, healthcheck_service):
        """Test GPU information when GPU is not available."""
        with patch.object(healthcheck_service, '_get_gpu_info', return_value=None):
            gpu_info = healthcheck_service.get_gpu_info()
        
        assert gpu_info["gpu_count"] == 0
        assert gpu_info["gpus"] == []
        assert "error" in gpu_info
    
    def test_check_resource_thresholds_normal(self, healthcheck_service):
        """Test resource threshold checking with normal usage."""
        resources = {
            "cpu": {"usage_percent": 45.0},
            "memory": {"usage_percent": 60.0},
            "disk": {"usage_percent": 70.0}
        }
        
        alerts = healthcheck_service._check_resource_thresholds(resources)
        
        assert len(alerts) == 0
    
    def test_check_resource_thresholds_high_usage(self, healthcheck_service):
        """Test resource threshold checking with high usage."""
        resources = {
            "cpu": {"usage_percent": 95.0},
            "memory": {"usage_percent": 90.0},
            "disk": {"usage_percent": 95.0}
        }
        
        alerts = healthcheck_service._check_resource_thresholds(resources)
        
        assert len(alerts) == 3
        assert any("CPU usage" in alert["message"] for alert in alerts)
        assert any("Memory usage" in alert["message"] for alert in alerts)
        assert any("Disk usage" in alert["message"] for alert in alerts)


class TestServiceHealthChecks:
    """Test cases for individual service health checks."""
    
    @pytest.mark.asyncio
    async def test_check_text_service_health_healthy(self, healthcheck_service):
        """Test text service health check when healthy."""
        mock_health = {
            "status": "healthy",
            "model_loaded": True,
            "response_time_ms": 150.0
        }
        
        with patch('app.services.text_service.TextService.health_check', 
                  new_callable=AsyncMock, return_value=mock_health):
            
            health = await healthcheck_service._check_text_service_health()
        
        assert health["status"] == "healthy"
        assert health["model_loaded"] is True
        assert "response_time_ms" in health
    
    @pytest.mark.asyncio
    async def test_check_text_service_health_error(self, healthcheck_service):
        """Test text service health check when error occurs."""
        with patch('app.services.text_service.TextService.health_check', 
                  new_callable=AsyncMock, side_effect=Exception("Service error")):
            
            health = await healthcheck_service._check_text_service_health()
        
        assert health["status"] == "error"
        assert "error" in health
        assert "Service error" in health["error"]
    
    @pytest.mark.asyncio
    async def test_check_image_service_health_healthy(self, healthcheck_service):
        """Test image service health check when healthy."""
        mock_health = {
            "status": "healthy",
            "model_loaded": True,
            "memory_usage_mb": 2048
        }
        
        with patch('app.services.image_service.ImageService.health_check', 
                  new_callable=AsyncMock, return_value=mock_health):
            
            health = await healthcheck_service._check_image_service_health()
        
        assert health["status"] == "healthy"
        assert health["model_loaded"] is True
        assert "memory_usage_mb" in health
    
    @pytest.mark.asyncio
    async def test_check_audio_service_health_healthy(self, healthcheck_service):
        """Test audio service health check when healthy."""
        mock_health = {
            "status": "healthy",
            "model_loaded": True,
            "supported_languages": ["en", "es", "fr"]
        }
        
        with patch('app.services.audio_service.AudioService.health_check', 
                  new_callable=AsyncMock, return_value=mock_health):
            
            health = await healthcheck_service._check_audio_service_health()
        
        assert health["status"] == "healthy"
        assert health["model_loaded"] is True
        assert "supported_languages" in health


class TestModelStatusMonitoring:
    """Test cases for model status monitoring."""
    
    @pytest.mark.asyncio
    async def test_get_model_status_all_loaded(self, healthcheck_service):
        """Test model status when all models are loaded."""
        mock_text_info = {"model_name": "text-model", "is_loaded": True, "device": "cuda"}
        mock_image_info = {"model_name": "image-model", "is_loaded": True, "device": "cuda"}
        mock_audio_info = {"model_name": "audio-model", "is_loaded": True, "device": "cpu"}
        
        with patch('app.services.text_service.TextService.get_model_info', return_value=mock_text_info), \
             patch('app.services.image_service.ImageService.get_model_info', return_value=mock_image_info), \
             patch('app.services.audio_service.AudioService.get_model_info', return_value=mock_audio_info):
            
            status = await healthcheck_service.get_model_status()
        
        assert status["all_models_loaded"] is True
        assert len(status["models"]) == 3
        assert status["models"]["text"]["is_loaded"] is True
        assert status["models"]["image"]["is_loaded"] is True
        assert status["models"]["audio"]["is_loaded"] is True
    
    @pytest.mark.asyncio
    async def test_get_model_status_partial_loaded(self, healthcheck_service):
        """Test model status when some models are not loaded."""
        mock_text_info = {"model_name": "text-model", "is_loaded": True, "device": "cuda"}
        mock_image_info = {"error": "Model not loaded", "is_loaded": False}
        mock_audio_info = {"model_name": "audio-model", "is_loaded": True, "device": "cpu"}
        
        with patch('app.services.text_service.TextService.get_model_info', return_value=mock_text_info), \
             patch('app.services.image_service.ImageService.get_model_info', return_value=mock_image_info), \
             patch('app.services.audio_service.AudioService.get_model_info', return_value=mock_audio_info):
            
            status = await healthcheck_service.get_model_status()
        
        assert status["all_models_loaded"] is False
        assert status["models"]["text"]["is_loaded"] is True
        assert status["models"]["image"]["is_loaded"] is False
        assert status["models"]["audio"]["is_loaded"] is True
        assert "unloaded_models" in status
        assert "image" in status["unloaded_models"]


class TestDetailedHealthStatus:
    """Test cases for detailed health status."""
    
    @pytest.mark.asyncio
    async def test_get_detailed_health_status_healthy(self, healthcheck_service):
        """Test detailed health status when system is healthy."""
        # Mock all components to be healthy
        with patch.object(healthcheck_service, 'get_system_resources') as mock_resources, \
             patch.object(healthcheck_service, 'get_gpu_info') as mock_gpu, \
             patch.object(healthcheck_service, 'get_model_status') as mock_models, \
             patch.object(healthcheck_service, '_check_text_service_health') as mock_text, \
             patch.object(healthcheck_service, '_check_image_service_health') as mock_image, \
             patch.object(healthcheck_service, '_check_audio_service_health') as mock_audio:
            
            mock_resources.return_value = {
                "cpu": {"usage_percent": 45.0},
                "memory": {"usage_percent": 60.0},
                "disk": {"usage_percent": 70.0}
            }
            mock_gpu.return_value = {"gpu_count": 1, "gpus": []}
            mock_models.return_value = {"all_models_loaded": True, "models": {}}
            mock_text.return_value = {"status": "healthy"}
            mock_image.return_value = {"status": "healthy"}
            mock_audio.return_value = {"status": "healthy"}
            
            status = await healthcheck_service.get_detailed_health_status()
        
        assert status["overall_status"] == "healthy"
        assert "system_resources" in status
        assert "gpu_info" in status
        assert "model_status" in status
        assert "services" in status
        assert "alerts" in status
        assert "timestamp" in status
    
    @pytest.mark.asyncio
    async def test_get_detailed_health_status_with_issues(self, healthcheck_service):
        """Test detailed health status with system issues."""
        with patch.object(healthcheck_service, 'get_system_resources') as mock_resources, \
             patch.object(healthcheck_service, 'get_gpu_info') as mock_gpu, \
             patch.object(healthcheck_service, 'get_model_status') as mock_models, \
             patch.object(healthcheck_service, '_check_text_service_health') as mock_text, \
             patch.object(healthcheck_service, '_check_image_service_health') as mock_image, \
             patch.object(healthcheck_service, '_check_audio_service_health') as mock_audio:
            
            # High resource usage
            mock_resources.return_value = {
                "cpu": {"usage_percent": 95.0},
                "memory": {"usage_percent": 90.0},
                "disk": {"usage_percent": 85.0}
            }
            mock_gpu.return_value = {"gpu_count": 0, "gpus": []}
            mock_models.return_value = {"all_models_loaded": False, "models": {}}
            mock_text.return_value = {"status": "unhealthy"}
            mock_image.return_value = {"status": "healthy"}
            mock_audio.return_value = {"status": "error"}
            
            status = await healthcheck_service.get_detailed_health_status()
        
        assert status["overall_status"] in ["degraded", "unhealthy"]
        assert len(status["alerts"]) > 0


class TestSystemMetrics:
    """Test cases for system metrics collection."""
    
    def test_get_system_metrics(self, healthcheck_service):
        """Test system metrics collection."""
        with patch('psutil.cpu_percent', return_value=55.0), \
             patch('psutil.virtual_memory') as mock_memory, \
             patch('psutil.disk_usage') as mock_disk, \
             patch('psutil.boot_time', return_value=1640995200.0):  # Mock boot time
            
            mock_memory.return_value.percent = 65.0
            mock_disk.return_value.percent = 75.0
            
            metrics = healthcheck_service.get_system_metrics()
        
        assert "cpu_usage_percent" in metrics
        assert "memory_usage_percent" in metrics
        assert "disk_usage_percent" in metrics
        assert "uptime_seconds" in metrics
        assert "timestamp" in metrics
        
        assert metrics["cpu_usage_percent"] == 55.0
        assert metrics["memory_usage_percent"] == 65.0
        assert metrics["disk_usage_percent"] == 75.0
    
    def test_get_system_metrics_with_history(self, healthcheck_service):
        """Test system metrics with historical data."""
        # Add some historical metrics
        healthcheck_service.metrics_history = [
            {"timestamp": 1640995200.0, "cpu_usage_percent": 50.0},
            {"timestamp": 1640995260.0, "cpu_usage_percent": 55.0},
            {"timestamp": 1640995320.0, "cpu_usage_percent": 60.0}
        ]
        
        with patch('psutil.cpu_percent', return_value=65.0), \
             patch('psutil.virtual_memory') as mock_memory, \
             patch('psutil.disk_usage') as mock_disk:
            
            mock_memory.return_value.percent = 70.0
            mock_disk.return_value.percent = 80.0
            
            metrics = healthcheck_service.get_system_metrics(include_history=True)
        
        assert "current" in metrics
        assert "history" in metrics
        assert len(metrics["history"]) == 3
        assert "trends" in metrics


class TestAlertManagement:
    """Test cases for alert management."""
    
    def test_add_alert(self, healthcheck_service):
        """Test adding an alert."""
        alert = {
            "level": "warning",
            "message": "High CPU usage detected",
            "component": "system"
        }
        
        healthcheck_service._add_alert(alert)
        
        assert len(healthcheck_service.alerts) == 1
        assert healthcheck_service.alerts[0]["message"] == "High CPU usage detected"
        assert "timestamp" in healthcheck_service.alerts[0]
    
    def test_get_alerts(self, healthcheck_service):
        """Test getting alerts."""
        # Add some test alerts
        healthcheck_service.alerts = [
            {"level": "warning", "message": "Alert 1", "timestamp": 1640995200.0},
            {"level": "critical", "message": "Alert 2", "timestamp": 1640995260.0}
        ]
        
        alerts = healthcheck_service.get_alerts()
        
        assert len(alerts) == 2
        assert alerts[0]["message"] == "Alert 1"
        assert alerts[1]["message"] == "Alert 2"
    
    def test_get_alerts_filtered_by_level(self, healthcheck_service):
        """Test getting alerts filtered by level."""
        healthcheck_service.alerts = [
            {"level": "warning", "message": "Warning alert", "timestamp": 1640995200.0},
            {"level": "critical", "message": "Critical alert", "timestamp": 1640995260.0},
            {"level": "info", "message": "Info alert", "timestamp": 1640995320.0}
        ]
        
        critical_alerts = healthcheck_service.get_alerts(level="critical")
        
        assert len(critical_alerts) == 1
        assert critical_alerts[0]["message"] == "Critical alert"
    
    def test_clear_alerts(self, healthcheck_service):
        """Test clearing alerts."""
        # Add some test alerts
        healthcheck_service.alerts = [
            {"level": "warning", "message": "Alert 1", "timestamp": 1640995200.0},
            {"level": "critical", "message": "Alert 2", "timestamp": 1640995260.0}
        ]
        
        healthcheck_service.clear_alerts()
        
        assert len(healthcheck_service.alerts) == 0


class TestMaintenanceMode:
    """Test cases for maintenance mode functionality."""
    
    def test_enable_maintenance_mode(self, healthcheck_service):
        """Test enabling maintenance mode."""
        healthcheck_service.enable_maintenance_mode("System upgrade in progress")
        
        assert healthcheck_service.maintenance_mode is True
        assert "System upgrade" in healthcheck_service.maintenance_message
    
    def test_disable_maintenance_mode(self, healthcheck_service):
        """Test disabling maintenance mode."""
        healthcheck_service.enable_maintenance_mode("Test maintenance")
        healthcheck_service.disable_maintenance_mode()
        
        assert healthcheck_service.maintenance_mode is False
        assert healthcheck_service.maintenance_message is None
    
    def test_get_maintenance_info(self, healthcheck_service):
        """Test getting maintenance information."""
        healthcheck_service.enable_maintenance_mode("Scheduled maintenance")
        
        info = healthcheck_service.get_maintenance_info()
        
        assert info["maintenance_mode"] is True
        assert info["message"] == "Scheduled maintenance"
        assert "enabled_at" in info
    
    @pytest.mark.asyncio
    async def test_health_check_during_maintenance(self, healthcheck_service):
        """Test health check response during maintenance mode."""
        healthcheck_service.enable_maintenance_mode("System maintenance")
        
        result = await healthcheck_service.liveness_check()
        
        assert "maintenance" in result
        assert result["maintenance"]["enabled"] is True
        assert "System maintenance" in result["maintenance"]["message"]


# Performance and integration tests
class TestHealthCheckPerformance:
    """Performance tests for health check service."""
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_detailed_health_check_performance(self, healthcheck_service):
        """Test detailed health check performance."""
        import time
        
        start_time = time.time()
        
        # Mock all dependencies to avoid actual system calls
        with patch.object(healthcheck_service, 'get_system_resources'), \
             patch.object(healthcheck_service, 'get_gpu_info'), \
             patch.object(healthcheck_service, 'get_model_status'), \
             patch.object(healthcheck_service, '_check_text_service_health'), \
             patch.object(healthcheck_service, '_check_image_service_health'), \
             patch.object(healthcheck_service, '_check_audio_service_health'):
            
            await healthcheck_service.get_detailed_health_status()
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Health check should be fast
        assert processing_time < 1.0
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_full_health_check_workflow(self, healthcheck_service):
        """Test complete health check workflow."""
        # Test the full workflow: ping -> readiness -> liveness -> detailed status
        
        # 1. Basic ping
        ping_result = healthcheck_service.ping()
        assert ping_result["status"] == "ok"
        
        # 2. Readiness check
        with patch.object(healthcheck_service, '_check_text_service_health'), \
             patch.object(healthcheck_service, '_check_image_service_health'), \
             patch.object(healthcheck_service, '_check_audio_service_health'):
            
            readiness_result = await healthcheck_service.readiness_check()
            assert "ready" in readiness_result
        
        # 3. Liveness check
        with patch('psutil.cpu_percent'), \
             patch('psutil.virtual_memory'):
            
            liveness_result = await healthcheck_service.liveness_check()
            assert "alive" in liveness_result
        
        # 4. Detailed status
        with patch.object(healthcheck_service, 'get_system_resources'), \
             patch.object(healthcheck_service, 'get_gpu_info'), \
             patch.object(healthcheck_service, 'get_model_status'), \
             patch.object(healthcheck_service, '_check_text_service_health'), \
             patch.object(healthcheck_service, '_check_image_service_health'), \
             patch.object(healthcheck_service, '_check_audio_service_health'):
            
            detailed_result = await healthcheck_service.get_detailed_health_status()
            assert "overall_status" in detailed_result