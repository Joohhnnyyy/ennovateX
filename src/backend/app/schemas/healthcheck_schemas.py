"""Pydantic schemas for healthcheck and system monitoring endpoints.

Defines request and response models for system health monitoring.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class PingResponse(BaseModel):
    """Response schema for basic ping endpoint."""
    
    message: str = Field(
        description="Ping response message"
    )
    timestamp: str = Field(
        description="ISO timestamp of the ping"
    )
    uptime_seconds: float = Field(
        description="Service uptime in seconds"
    )
    version: str = Field(
        description="API version"
    )


class SystemResources(BaseModel):
    """Schema for system resource information."""
    
    cpu_usage_percent: float = Field(
        description="Current CPU usage percentage"
    )
    memory_usage_percent: float = Field(
        description="Current memory usage percentage"
    )
    memory_total_gb: float = Field(
        description="Total system memory in GB"
    )
    memory_available_gb: float = Field(
        description="Available system memory in GB"
    )
    memory_used_gb: float = Field(
        description="Used system memory in GB"
    )
    disk_usage_percent: float = Field(
        description="Current disk usage percentage"
    )
    disk_total_gb: float = Field(
        description="Total disk space in GB"
    )
    disk_free_gb: float = Field(
        description="Free disk space in GB"
    )
    load_average: List[float] = Field(
        description="System load average (1, 5, 15 minutes)"
    )


class GPUInfo(BaseModel):
    """Schema for GPU information."""
    
    gpu_id: int = Field(
        description="GPU device ID"
    )
    name: str = Field(
        description="GPU name/model"
    )
    memory_total_mb: float = Field(
        description="Total GPU memory in MB"
    )
    memory_used_mb: float = Field(
        description="Used GPU memory in MB"
    )
    memory_free_mb: float = Field(
        description="Free GPU memory in MB"
    )
    memory_usage_percent: float = Field(
        description="GPU memory usage percentage"
    )
    utilization_percent: float = Field(
        description="GPU utilization percentage"
    )
    temperature_celsius: Optional[float] = Field(
        default=None,
        description="GPU temperature in Celsius"
    )
    power_usage_watts: Optional[float] = Field(
        default=None,
        description="GPU power usage in watts"
    )


class ModelStatus(BaseModel):
    """Schema for individual model status."""
    
    model_name: str = Field(
        description="Name of the model"
    )
    model_type: str = Field(
        description="Type of the model (text, image, audio)"
    )
    status: str = Field(
        description="Model status (loaded, loading, failed, not_loaded)"
    )
    device: str = Field(
        description="Device the model is running on"
    )
    memory_usage_mb: float = Field(
        description="Memory usage of the model in MB"
    )
    load_time_seconds: Optional[float] = Field(
        default=None,
        description="Time taken to load the model"
    )
    last_used: Optional[str] = Field(
        default=None,
        description="ISO timestamp of last model usage"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if model failed to load"
    )


class ServiceHealth(BaseModel):
    """Schema for individual service health status."""
    
    service_name: str = Field(
        description="Name of the service"
    )
    status: str = Field(
        description="Service status (healthy, unhealthy, degraded)"
    )
    response_time_ms: float = Field(
        description="Service response time in milliseconds"
    )
    last_check: str = Field(
        description="ISO timestamp of last health check"
    )
    error_count: int = Field(
        description="Number of recent errors"
    )
    success_rate_percent: float = Field(
        description="Success rate percentage over recent requests"
    )
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional service-specific health details"
    )


class DatabaseHealth(BaseModel):
    """Schema for database health status."""
    
    status: str = Field(
        description="Database status (connected, disconnected, error)"
    )
    connection_pool_size: int = Field(
        description="Current connection pool size"
    )
    active_connections: int = Field(
        description="Number of active connections"
    )
    response_time_ms: float = Field(
        description="Database response time in milliseconds"
    )
    last_check: str = Field(
        description="ISO timestamp of last database check"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if database is unhealthy"
    )


class ExternalServiceHealth(BaseModel):
    """Schema for external service health status."""
    
    service_name: str = Field(
        description="Name of the external service"
    )
    endpoint: str = Field(
        description="Service endpoint URL"
    )
    status: str = Field(
        description="Service status (available, unavailable, timeout)"
    )
    response_time_ms: float = Field(
        description="Response time in milliseconds"
    )
    status_code: Optional[int] = Field(
        default=None,
        description="HTTP status code (if applicable)"
    )
    last_check: str = Field(
        description="ISO timestamp of last check"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if service is unavailable"
    )


class SystemStatusResponse(BaseModel):
    """Response schema for detailed system status."""
    
    overall_status: str = Field(
        description="Overall system status (healthy, degraded, unhealthy)"
    )
    timestamp: str = Field(
        description="ISO timestamp of status check"
    )
    uptime_seconds: float = Field(
        description="Service uptime in seconds"
    )
    version: str = Field(
        description="API version"
    )
    environment: str = Field(
        description="Environment (development, staging, production)"
    )
    system_resources: SystemResources = Field(
        description="System resource information"
    )
    gpu_info: Optional[List[GPUInfo]] = Field(
        default=None,
        description="GPU information (if available)"
    )
    model_status: List[ModelStatus] = Field(
        description="Status of all ML models"
    )
    service_health: List[ServiceHealth] = Field(
        description="Health status of all services"
    )
    database_health: Optional[DatabaseHealth] = Field(
        default=None,
        description="Database health status (if applicable)"
    )
    external_services: Optional[List[ExternalServiceHealth]] = Field(
        default=None,
        description="External service health status"
    )


class ReadinessCheck(BaseModel):
    """Schema for individual readiness check."""
    
    check_name: str = Field(
        description="Name of the readiness check"
    )
    status: str = Field(
        description="Check status (ready, not_ready, error)"
    )
    response_time_ms: float = Field(
        description="Check response time in milliseconds"
    )
    details: Optional[str] = Field(
        default=None,
        description="Additional details about the check"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if check failed"
    )


class ReadinessResponse(BaseModel):
    """Response schema for service readiness check."""
    
    ready: bool = Field(
        description="Whether the service is ready to handle requests"
    )
    timestamp: str = Field(
        description="ISO timestamp of readiness check"
    )
    checks: List[ReadinessCheck] = Field(
        description="Individual readiness checks performed"
    )
    total_checks: int = Field(
        description="Total number of checks performed"
    )
    passed_checks: int = Field(
        description="Number of checks that passed"
    )
    failed_checks: int = Field(
        description="Number of checks that failed"
    )
    overall_response_time_ms: float = Field(
        description="Total time for all readiness checks"
    )


class MetricsSnapshot(BaseModel):
    """Schema for system metrics snapshot."""
    
    timestamp: str = Field(
        description="ISO timestamp of metrics snapshot"
    )
    requests_per_minute: float = Field(
        description="Current requests per minute"
    )
    average_response_time_ms: float = Field(
        description="Average response time in milliseconds"
    )
    error_rate_percent: float = Field(
        description="Current error rate percentage"
    )
    active_connections: int = Field(
        description="Number of active connections"
    )
    queue_size: int = Field(
        description="Current request queue size"
    )
    cache_hit_rate_percent: Optional[float] = Field(
        default=None,
        description="Cache hit rate percentage (if applicable)"
    )


class AlertInfo(BaseModel):
    """Schema for system alert information."""
    
    alert_id: str = Field(
        description="Unique alert identifier"
    )
    severity: str = Field(
        description="Alert severity (low, medium, high, critical)"
    )
    title: str = Field(
        description="Alert title"
    )
    description: str = Field(
        description="Alert description"
    )
    component: str = Field(
        description="System component that triggered the alert"
    )
    timestamp: str = Field(
        description="ISO timestamp when alert was triggered"
    )
    status: str = Field(
        description="Alert status (active, resolved, acknowledged)"
    )
    threshold_value: Optional[float] = Field(
        default=None,
        description="Threshold value that was exceeded"
    )
    current_value: Optional[float] = Field(
        default=None,
        description="Current value that triggered the alert"
    )


class SystemMetricsResponse(BaseModel):
    """Response schema for system metrics and monitoring."""
    
    timestamp: str = Field(
        description="ISO timestamp of metrics collection"
    )
    uptime_seconds: float = Field(
        description="Service uptime in seconds"
    )
    current_metrics: MetricsSnapshot = Field(
        description="Current system metrics snapshot"
    )
    system_resources: SystemResources = Field(
        description="Current system resource usage"
    )
    active_alerts: List[AlertInfo] = Field(
        description="List of active system alerts"
    )
    total_requests_today: int = Field(
        description="Total requests processed today"
    )
    total_errors_today: int = Field(
        description="Total errors encountered today"
    )
    peak_requests_per_minute: float = Field(
        description="Peak requests per minute today"
    )
    average_daily_response_time_ms: float = Field(
        description="Average response time for today"
    )


class HealthCheckConfig(BaseModel):
    """Schema for health check configuration."""
    
    check_interval_seconds: int = Field(
        description="Interval between health checks in seconds"
    )
    timeout_seconds: int = Field(
        description="Timeout for health checks in seconds"
    )
    failure_threshold: int = Field(
        description="Number of failures before marking as unhealthy"
    )
    success_threshold: int = Field(
        description="Number of successes before marking as healthy"
    )
    enabled_checks: List[str] = Field(
        description="List of enabled health check types"
    )


class MaintenanceInfo(BaseModel):
    """Schema for maintenance information."""
    
    maintenance_mode: bool = Field(
        description="Whether the system is in maintenance mode"
    )
    scheduled_maintenance: Optional[str] = Field(
        default=None,
        description="ISO timestamp of next scheduled maintenance"
    )
    maintenance_message: Optional[str] = Field(
        default=None,
        description="Maintenance message for users"
    )
    estimated_duration_minutes: Optional[int] = Field(
        default=None,
        description="Estimated maintenance duration in minutes"
    )


class ComprehensiveHealthResponse(BaseModel):
    """Response schema for comprehensive health check."""
    
    overall_status: str = Field(
        description="Overall system health status"
    )
    timestamp: str = Field(
        description="ISO timestamp of health check"
    )
    system_status: SystemStatusResponse = Field(
        description="Detailed system status information"
    )
    readiness: ReadinessResponse = Field(
        description="Service readiness information"
    )
    metrics: SystemMetricsResponse = Field(
        description="System metrics and monitoring data"
    )
    health_config: HealthCheckConfig = Field(
        description="Health check configuration"
    )
    maintenance_info: MaintenanceInfo = Field(
        description="Maintenance information"
    )
    recommendations: Optional[List[str]] = Field(
        default=None,
        description="System optimization recommendations"
    )