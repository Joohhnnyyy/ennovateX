"""Pydantic schemas for image processing endpoints.

Defines request and response models for image captioning and visual question answering.
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime
import base64


class ImageUploadRequest(BaseModel):
    """Request schema for image upload validation."""
    
    image_data: str = Field(
        ...,
        description="Base64 encoded image data"
    )
    filename: Optional[str] = Field(
        default=None,
        description="Original filename of the image"
    )
    validate_only: bool = Field(
        default=False,
        description="Whether to only validate the image without processing"
    )
    
    @validator('image_data')
    def validate_image_data(cls, v):
        try:
            # Basic validation of base64 data
            base64.b64decode(v)
        except Exception:
            raise ValueError('Invalid base64 image data')
        return v


class ImageProperties(BaseModel):
    """Schema for image properties analysis."""
    
    width: int = Field(
        description="Image width in pixels"
    )
    height: int = Field(
        description="Image height in pixels"
    )
    channels: int = Field(
        description="Number of color channels"
    )
    format: str = Field(
        description="Image format (JPEG, PNG, etc.)"
    )
    file_size_bytes: int = Field(
        description="File size in bytes"
    )
    aspect_ratio: float = Field(
        description="Aspect ratio (width/height)"
    )
    color_mode: str = Field(
        description="Color mode (RGB, RGBA, L, etc.)"
    )
    has_transparency: bool = Field(
        description="Whether the image has transparency"
    )
    is_animated: bool = Field(
        description="Whether the image is animated"
    )


class ImageCaptioningRequest(BaseModel):
    """Request schema for image captioning."""
    
    image_data: str = Field(
        ...,
        description="Base64 encoded image data"
    )
    max_length: int = Field(
        default=50,
        ge=5,
        le=200,
        description="Maximum length of the caption"
    )
    min_length: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Minimum length of the caption"
    )
    num_beams: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of beams for beam search"
    )
    temperature: float = Field(
        default=1.0,
        ge=0.1,
        le=2.0,
        description="Temperature for generation"
    )
    include_analysis: bool = Field(
        default=False,
        description="Whether to include image analysis in the response"
    )
    use_lora: bool = Field(
        default=False,
        description="Whether to use LoRA adapter for fine-tuned captioning"
    )
    lora_adapter: Optional[str] = Field(
        default=None,
        description="Specific LoRA adapter name to use"
    )
    
    @validator('image_data')
    def validate_image_data(cls, v):
        try:
            base64.b64decode(v)
        except Exception:
            raise ValueError('Invalid base64 image data')
        return v
    
    @validator('min_length', 'max_length')
    def validate_lengths(cls, v, values):
        if 'min_length' in values and 'max_length' in values:
            if values['min_length'] >= values['max_length']:
                raise ValueError('min_length must be less than max_length')
        return v


class ImageCaptioningResponse(BaseModel):
    """Response schema for image captioning."""
    
    caption: str = Field(
        description="Generated caption for the image"
    )
    original_caption: str = Field(
        description="Original caption before postprocessing"
    )
    confidence: float = Field(
        description="Confidence score for the caption (0-1)"
    )
    caption_length: int = Field(
        description="Length of the caption in characters"
    )
    processing_time_seconds: float = Field(
        description="Time taken to process the request in seconds"
    )
    timestamp: str = Field(
        description="ISO timestamp of when the processing completed"
    )
    image_properties: Optional[ImageProperties] = Field(
        default=None,
        description="Optional image properties analysis"
    )


class VisualQuestionAnsweringRequest(BaseModel):
    """Request schema for visual question answering."""
    
    image_data: str = Field(
        ...,
        description="Base64 encoded image data"
    )
    question: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Question about the image"
    )
    max_answer_length: int = Field(
        default=50,
        ge=5,
        le=200,
        description="Maximum length of the answer"
    )
    num_beams: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of beams for beam search"
    )
    temperature: float = Field(
        default=1.0,
        ge=0.1,
        le=2.0,
        description="Temperature for generation"
    )
    use_lora: bool = Field(
        default=False,
        description="Whether to use LoRA adapter"
    )
    lora_adapter: Optional[str] = Field(
        default=None,
        description="Specific LoRA adapter name to use"
    )
    
    @validator('image_data')
    def validate_image_data(cls, v):
        try:
            base64.b64decode(v)
        except Exception:
            raise ValueError('Invalid base64 image data')
        return v


class VisualQuestionAnsweringResponse(BaseModel):
    """Response schema for visual question answering."""
    
    answer: str = Field(
        description="Generated answer to the question"
    )
    confidence: float = Field(
        description="Confidence score for the answer (0-1)"
    )
    question_length: int = Field(
        description="Length of the question"
    )
    answer_length: int = Field(
        description="Length of the answer"
    )
    processing_time_seconds: float = Field(
        description="Time taken to process the request"
    )
    timestamp: str = Field(
        description="ISO timestamp of processing completion"
    )


class BatchImageRequest(BaseModel):
    """Request schema for batch image processing."""
    
    images: List[Dict[str, Any]] = Field(
        ...,
        min_items=1,
        max_items=20,
        description="List of images with their data and optional metadata"
    )
    max_length: int = Field(
        default=50,
        ge=5,
        le=200,
        description="Maximum length of each caption"
    )
    min_length: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Minimum length of each caption"
    )
    num_beams: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of beams for beam search"
    )
    use_lora: bool = Field(
        default=False,
        description="Whether to use LoRA adapter"
    )
    lora_adapter: Optional[str] = Field(
        default=None,
        description="Specific LoRA adapter name to use"
    )
    
    @validator('images')
    def validate_images(cls, v):
        for i, img in enumerate(v):
            if 'image_data' not in img:
                raise ValueError(f'Image at index {i} missing "image_data" field')
            try:
                base64.b64decode(img['image_data'])
            except Exception:
                raise ValueError(f'Invalid base64 image data at index {i}')
        return v


class BatchImageResult(BaseModel):
    """Schema for individual batch image processing result."""
    
    index: int = Field(
        description="Index of the image in the original batch"
    )
    status: str = Field(
        description="Processing status (success or failed)"
    )
    caption: Optional[str] = Field(
        default=None,
        description="Generated caption (if successful)"
    )
    confidence: Optional[float] = Field(
        default=None,
        description="Confidence score (if successful)"
    )
    caption_length: Optional[int] = Field(
        default=None,
        description="Length of caption"
    )
    processing_time_seconds: Optional[float] = Field(
        default=None,
        description="Processing time for this image"
    )
    image_properties: Optional[ImageProperties] = Field(
        default=None,
        description="Image properties (if analyzed)"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message (if failed)"
    )


class BatchImageStats(BaseModel):
    """Schema for batch image processing statistics."""
    
    total_images: int = Field(
        description="Total number of images processed"
    )
    successful_count: int = Field(
        description="Number of successfully processed images"
    )
    failed_count: int = Field(
        description="Number of failed images"
    )
    total_processing_time_seconds: float = Field(
        description="Total processing time for the batch"
    )
    average_processing_time: float = Field(
        description="Average processing time per image"
    )
    average_caption_length: float = Field(
        description="Average caption length"
    )
    average_confidence: float = Field(
        description="Average confidence score"
    )
    throughput_images_per_second: float = Field(
        description="Processing throughput in images per second"
    )


class BatchImageResponse(BaseModel):
    """Response schema for batch image processing."""
    
    results: List[BatchImageResult] = Field(
        description="Results for each image in the batch"
    )
    batch_stats: BatchImageStats = Field(
        description="Statistics for the entire batch"
    )
    timestamp: str = Field(
        description="ISO timestamp of batch completion"
    )


class ImageDescriptionRequest(BaseModel):
    """Request schema for detailed image description."""
    
    image_data: str = Field(
        ...,
        description="Base64 encoded image data"
    )
    description_type: str = Field(
        default="detailed",
        description="Type of description (brief, detailed, comprehensive)"
    )
    max_length: int = Field(
        default=200,
        ge=20,
        le=1000,
        description="Maximum length of the description"
    )
    include_objects: bool = Field(
        default=True,
        description="Whether to include object detection in description"
    )
    include_scene: bool = Field(
        default=True,
        description="Whether to include scene analysis"
    )
    include_colors: bool = Field(
        default=True,
        description="Whether to include color analysis"
    )
    use_lora: bool = Field(
        default=False,
        description="Whether to use LoRA adapter"
    )
    lora_adapter: Optional[str] = Field(
        default=None,
        description="Specific LoRA adapter name to use"
    )
    
    @validator('description_type')
    def validate_description_type(cls, v):
        if v not in ['brief', 'detailed', 'comprehensive']:
            raise ValueError('description_type must be "brief", "detailed", or "comprehensive"')
        return v
    
    @validator('image_data')
    def validate_image_data(cls, v):
        try:
            base64.b64decode(v)
        except Exception:
            raise ValueError('Invalid base64 image data')
        return v


class ImageDescriptionResponse(BaseModel):
    """Response schema for detailed image description."""
    
    description: str = Field(
        description="Generated detailed description"
    )
    description_type: str = Field(
        description="Type of description generated"
    )
    description_length: int = Field(
        description="Length of the description"
    )
    confidence: float = Field(
        description="Confidence score for the description"
    )
    processing_time_seconds: float = Field(
        description="Time taken to process the request"
    )
    timestamp: str = Field(
        description="ISO timestamp of processing completion"
    )
    image_properties: Optional[ImageProperties] = Field(
        default=None,
        description="Optional image properties analysis"
    )


class ImageModelInfo(BaseModel):
    """Schema for image model information."""
    
    model_name: str = Field(
        description="Name of the image model"
    )
    model_type: str = Field(
        description="Type of the model (captioning, vqa, etc.)"
    )
    model_size: str = Field(
        description="Size of the model"
    )
    device: str = Field(
        description="Device the model is running on"
    )
    memory_usage_mb: float = Field(
        description="Memory usage in MB"
    )
    supports_lora: bool = Field(
        description="Whether the model supports LoRA adapters"
    )
    available_adapters: List[str] = Field(
        description="List of available LoRA adapters"
    )
    max_image_size: Dict[str, int] = Field(
        description="Maximum image dimensions (width, height)"
    )
    supported_formats: List[str] = Field(
        description="Supported image formats"
    )
    max_batch_size: int = Field(
        description="Maximum batch size for processing"
    )


class ImageServiceStats(BaseModel):
    """Schema for image service statistics."""
    
    total_requests: int = Field(
        description="Total number of requests processed"
    )
    successful_requests: int = Field(
        description="Number of successful requests"
    )
    failed_requests: int = Field(
        description="Number of failed requests"
    )
    total_images_processed: int = Field(
        description="Total number of images processed"
    )
    total_processing_time: float = Field(
        description="Total processing time in seconds"
    )
    average_processing_time_seconds: float = Field(
        description="Average processing time per request"
    )
    average_caption_length: float = Field(
        description="Average caption length"
    )
    average_confidence: float = Field(
        description="Average confidence score"
    )


class ImageServiceConfig(BaseModel):
    """Schema for image service configuration."""
    
    max_image_size_mb: float = Field(
        description="Maximum image size in MB"
    )
    max_batch_size: int = Field(
        description="Maximum batch size"
    )
    max_concurrent_requests: int = Field(
        description="Maximum concurrent requests"
    )
    supported_formats: List[str] = Field(
        description="Supported image formats"
    )


class ImageServiceStatsResponse(BaseModel):
    """Response schema for image service statistics."""
    
    processing_stats: ImageServiceStats = Field(
        description="Processing statistics"
    )
    model_info: ImageModelInfo = Field(
        description="Information about the image model"
    )
    service_config: ImageServiceConfig = Field(
        description="Service configuration"
    )


class ImageHealthCheckResponse(BaseModel):
    """Response schema for image service health check."""
    
    status: str = Field(
        description="Health status (healthy or unhealthy)"
    )
    test_successful: bool = Field(
        description="Whether the health test was successful"
    )
    test_caption_length: Optional[int] = Field(
        default=None,
        description="Length of test caption (if successful)"
    )
    model_loaded: bool = Field(
        description="Whether the model is loaded"
    )
    test_image_properties: Optional[ImageProperties] = Field(
        default=None,
        description="Properties of test image (if analyzed)"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message (if unhealthy)"
    )
    timestamp: str = Field(
        description="ISO timestamp of health check"
    )


class ImageUploadResponse(BaseModel):
    """Response schema for image upload validation."""
    
    status: str = Field(
        description="Validation status (valid or invalid)"
    )
    image_properties: Optional[ImageProperties] = Field(
        default=None,
        description="Image properties (if valid)"
    )
    validation_errors: Optional[List[str]] = Field(
        default=None,
        description="List of validation errors (if invalid)"
    )
    processing_time_seconds: float = Field(
        description="Time taken to validate the image"
    )
    timestamp: str = Field(
        description="ISO timestamp of validation"
    )