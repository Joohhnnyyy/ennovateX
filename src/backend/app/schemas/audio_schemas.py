"""Pydantic schemas for audio processing endpoints.

Defines request and response models for speech-to-text and audio translation.
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime
import base64


class AudioUploadRequest(BaseModel):
    """Request schema for audio upload validation."""
    
    audio_data: str = Field(
        ...,
        description="Base64 encoded audio data"
    )
    filename: Optional[str] = Field(
        default=None,
        description="Original filename of the audio file"
    )
    validate_only: bool = Field(
        default=False,
        description="Whether to only validate the audio without processing"
    )
    
    @validator('audio_data')
    def validate_audio_data(cls, v):
        try:
            # Basic validation of base64 data
            base64.b64decode(v)
        except Exception:
            raise ValueError('Invalid base64 audio data')
        return v


class AudioProperties(BaseModel):
    """Schema for audio properties analysis."""
    
    duration_seconds: float = Field(
        description="Audio duration in seconds"
    )
    sample_rate: int = Field(
        description="Sample rate in Hz"
    )
    channels: int = Field(
        description="Number of audio channels"
    )
    format: str = Field(
        description="Audio format (WAV, MP3, etc.)"
    )
    file_size_bytes: int = Field(
        description="File size in bytes"
    )
    bit_depth: Optional[int] = Field(
        default=None,
        description="Bit depth (for uncompressed formats)"
    )
    bitrate: Optional[int] = Field(
        default=None,
        description="Bitrate in kbps (for compressed formats)"
    )
    rms_level: float = Field(
        description="Root Mean Square level (volume)"
    )
    peak_level: float = Field(
        description="Peak audio level"
    )
    silence_ratio: float = Field(
        description="Ratio of silence in the audio (0-1)"
    )
    speech_ratio: float = Field(
        description="Ratio of speech in the audio (0-1)"
    )


class SpeechToTextRequest(BaseModel):
    """Request schema for speech-to-text transcription."""
    
    audio_data: str = Field(
        ...,
        description="Base64 encoded audio data"
    )
    language: Optional[str] = Field(
        default=None,
        description="Language code for transcription (auto-detect if None)"
    )
    task: str = Field(
        default="transcribe",
        description="Task type (transcribe or translate)"
    )
    return_timestamps: bool = Field(
        default=False,
        description="Whether to return word-level timestamps"
    )
    include_analysis: bool = Field(
        default=False,
        description="Whether to include audio analysis in the response"
    )
    use_lora: bool = Field(
        default=False,
        description="Whether to use LoRA adapter for fine-tuned transcription"
    )
    lora_adapter: Optional[str] = Field(
        default=None,
        description="Specific LoRA adapter name to use"
    )
    
    @validator('audio_data')
    def validate_audio_data(cls, v):
        try:
            base64.b64decode(v)
        except Exception:
            raise ValueError('Invalid base64 audio data')
        return v
    
    @validator('task')
    def validate_task(cls, v):
        if v not in ['transcribe', 'translate']:
            raise ValueError('task must be either "transcribe" or "translate"')
        return v


class WordTimestamp(BaseModel):
    """Schema for word-level timestamps."""
    
    word: str = Field(
        description="The transcribed word"
    )
    start: float = Field(
        description="Start time in seconds"
    )
    end: float = Field(
        description="End time in seconds"
    )
    confidence: float = Field(
        description="Confidence score for this word (0-1)"
    )


class SpeechToTextResponse(BaseModel):
    """Response schema for speech-to-text transcription."""
    
    text: str = Field(
        description="Transcribed text"
    )
    original_text: str = Field(
        description="Original transcription before postprocessing"
    )
    language: str = Field(
        description="Detected or specified language"
    )
    confidence: float = Field(
        description="Overall confidence score for the transcription (0-1)"
    )
    task: str = Field(
        description="Task performed (transcribe or translate)"
    )
    text_length: int = Field(
        description="Length of transcribed text in characters"
    )
    word_count: int = Field(
        description="Number of words in the transcription"
    )
    processing_time_seconds: float = Field(
        description="Time taken to process the request in seconds"
    )
    timestamp: str = Field(
        description="ISO timestamp of when the processing completed"
    )
    word_timestamps: Optional[List[WordTimestamp]] = Field(
        default=None,
        description="Word-level timestamps (if requested)"
    )
    audio_properties: Optional[AudioProperties] = Field(
        default=None,
        description="Optional audio properties analysis"
    )


class AudioTranslationRequest(BaseModel):
    """Request schema for audio translation."""
    
    audio_data: str = Field(
        ...,
        description="Base64 encoded audio data"
    )
    source_language: Optional[str] = Field(
        default=None,
        description="Source language code (auto-detect if None)"
    )
    target_language: str = Field(
        default="en",
        description="Target language code for translation"
    )
    return_timestamps: bool = Field(
        default=False,
        description="Whether to return word-level timestamps"
    )
    include_transcription: bool = Field(
        default=False,
        description="Whether to include original transcription"
    )
    use_lora: bool = Field(
        default=False,
        description="Whether to use LoRA adapter"
    )
    lora_adapter: Optional[str] = Field(
        default=None,
        description="Specific LoRA adapter name to use"
    )
    
    @validator('audio_data')
    def validate_audio_data(cls, v):
        try:
            base64.b64decode(v)
        except Exception:
            raise ValueError('Invalid base64 audio data')
        return v


class AudioTranslationResponse(BaseModel):
    """Response schema for audio translation."""
    
    translated_text: str = Field(
        description="Translated text"
    )
    source_language: str = Field(
        description="Detected or specified source language"
    )
    target_language: str = Field(
        description="Target language for translation"
    )
    confidence: float = Field(
        description="Overall confidence score for the translation (0-1)"
    )
    translation_length: int = Field(
        description="Length of translated text in characters"
    )
    word_count: int = Field(
        description="Number of words in the translation"
    )
    processing_time_seconds: float = Field(
        description="Time taken to process the request"
    )
    timestamp: str = Field(
        description="ISO timestamp of processing completion"
    )
    original_transcription: Optional[str] = Field(
        default=None,
        description="Original transcription (if requested)"
    )
    word_timestamps: Optional[List[WordTimestamp]] = Field(
        default=None,
        description="Word-level timestamps (if requested)"
    )


class BatchAudioRequest(BaseModel):
    """Request schema for batch audio processing."""
    
    audio_files: List[Dict[str, Any]] = Field(
        ...,
        min_items=1,
        max_items=10,
        description="List of audio files with their data and optional metadata"
    )
    language: Optional[str] = Field(
        default=None,
        description="Language code for transcription (auto-detect if None)"
    )
    task: str = Field(
        default="transcribe",
        description="Task type (transcribe or translate)"
    )
    return_timestamps: bool = Field(
        default=False,
        description="Whether to return word-level timestamps"
    )
    use_lora: bool = Field(
        default=False,
        description="Whether to use LoRA adapter"
    )
    lora_adapter: Optional[str] = Field(
        default=None,
        description="Specific LoRA adapter name to use"
    )
    
    @validator('audio_files')
    def validate_audio_files(cls, v):
        for i, audio in enumerate(v):
            if 'audio_data' not in audio:
                raise ValueError(f'Audio file at index {i} missing "audio_data" field')
            try:
                base64.b64decode(audio['audio_data'])
            except Exception:
                raise ValueError(f'Invalid base64 audio data at index {i}')
        return v
    
    @validator('task')
    def validate_task(cls, v):
        if v not in ['transcribe', 'translate']:
            raise ValueError('task must be either "transcribe" or "translate"')
        return v


class BatchAudioResult(BaseModel):
    """Schema for individual batch audio processing result."""
    
    index: int = Field(
        description="Index of the audio file in the original batch"
    )
    status: str = Field(
        description="Processing status (success or failed)"
    )
    text: Optional[str] = Field(
        default=None,
        description="Transcribed/translated text (if successful)"
    )
    language: Optional[str] = Field(
        default=None,
        description="Detected or specified language (if successful)"
    )
    confidence: Optional[float] = Field(
        default=None,
        description="Confidence score (if successful)"
    )
    text_length: Optional[int] = Field(
        default=None,
        description="Length of transcribed text"
    )
    word_count: Optional[int] = Field(
        default=None,
        description="Number of words in transcription"
    )
    processing_time_seconds: Optional[float] = Field(
        default=None,
        description="Processing time for this audio file"
    )
    audio_properties: Optional[AudioProperties] = Field(
        default=None,
        description="Audio properties (if analyzed)"
    )
    word_timestamps: Optional[List[WordTimestamp]] = Field(
        default=None,
        description="Word-level timestamps (if requested)"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message (if failed)"
    )


class BatchAudioStats(BaseModel):
    """Schema for batch audio processing statistics."""
    
    total_files: int = Field(
        description="Total number of audio files processed"
    )
    successful_count: int = Field(
        description="Number of successfully processed files"
    )
    failed_count: int = Field(
        description="Number of failed files"
    )
    total_processing_time_seconds: float = Field(
        description="Total processing time for the batch"
    )
    total_audio_duration_seconds: float = Field(
        description="Total duration of all audio files"
    )
    average_processing_time: float = Field(
        description="Average processing time per file"
    )
    average_text_length: float = Field(
        description="Average transcription length"
    )
    average_confidence: float = Field(
        description="Average confidence score"
    )
    throughput_files_per_second: float = Field(
        description="Processing throughput in files per second"
    )
    real_time_factor: float = Field(
        description="Real-time factor (processing_time / audio_duration)"
    )


class BatchAudioResponse(BaseModel):
    """Response schema for batch audio processing."""
    
    results: List[BatchAudioResult] = Field(
        description="Results for each audio file in the batch"
    )
    batch_stats: BatchAudioStats = Field(
        description="Statistics for the entire batch"
    )
    timestamp: str = Field(
        description="ISO timestamp of batch completion"
    )


class SupportedLanguage(BaseModel):
    """Schema for supported language information."""
    
    code: str = Field(
        description="Language code (e.g., 'en', 'es', 'fr')"
    )
    name: str = Field(
        description="Language name (e.g., 'English', 'Spanish', 'French')"
    )
    native_name: str = Field(
        description="Native language name"
    )
    supports_transcription: bool = Field(
        description="Whether transcription is supported for this language"
    )
    supports_translation: bool = Field(
        description="Whether translation is supported for this language"
    )
    quality_score: float = Field(
        description="Quality score for this language (0-1)"
    )


class SupportedLanguagesResponse(BaseModel):
    """Response schema for supported languages."""
    
    languages: List[SupportedLanguage] = Field(
        description="List of supported languages"
    )
    total_languages: int = Field(
        description="Total number of supported languages"
    )
    default_language: str = Field(
        description="Default language code"
    )
    auto_detect_supported: bool = Field(
        description="Whether automatic language detection is supported"
    )


class AudioModelInfo(BaseModel):
    """Schema for audio model information."""
    
    model_name: str = Field(
        description="Name of the audio model"
    )
    model_type: str = Field(
        description="Type of the model (speech-to-text, translation, etc.)"
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
    supported_formats: List[str] = Field(
        description="Supported audio formats"
    )
    max_audio_length_seconds: int = Field(
        description="Maximum audio length in seconds"
    )
    max_batch_size: int = Field(
        description="Maximum batch size for processing"
    )
    supported_sample_rates: List[int] = Field(
        description="Supported sample rates in Hz"
    )


class AudioServiceStats(BaseModel):
    """Schema for audio service statistics."""
    
    total_requests: int = Field(
        description="Total number of requests processed"
    )
    successful_requests: int = Field(
        description="Number of successful requests"
    )
    failed_requests: int = Field(
        description="Number of failed requests"
    )
    total_audio_files_processed: int = Field(
        description="Total number of audio files processed"
    )
    total_audio_duration_seconds: float = Field(
        description="Total duration of processed audio"
    )
    total_processing_time: float = Field(
        description="Total processing time in seconds"
    )
    average_processing_time_seconds: float = Field(
        description="Average processing time per request"
    )
    average_text_length: float = Field(
        description="Average transcription length"
    )
    average_confidence: float = Field(
        description="Average confidence score"
    )
    real_time_factor: float = Field(
        description="Average real-time factor"
    )


class AudioServiceConfig(BaseModel):
    """Schema for audio service configuration."""
    
    max_audio_size_mb: float = Field(
        description="Maximum audio file size in MB"
    )
    max_audio_duration_seconds: int = Field(
        description="Maximum audio duration in seconds"
    )
    max_batch_size: int = Field(
        description="Maximum batch size"
    )
    max_concurrent_requests: int = Field(
        description="Maximum concurrent requests"
    )
    supported_formats: List[str] = Field(
        description="Supported audio formats"
    )
    default_language: str = Field(
        description="Default language for transcription"
    )


class AudioServiceStatsResponse(BaseModel):
    """Response schema for audio service statistics."""
    
    processing_stats: AudioServiceStats = Field(
        description="Processing statistics"
    )
    model_info: AudioModelInfo = Field(
        description="Information about the audio model"
    )
    service_config: AudioServiceConfig = Field(
        description="Service configuration"
    )


class AudioHealthCheckResponse(BaseModel):
    """Response schema for audio service health check."""
    
    status: str = Field(
        description="Health status (healthy or unhealthy)"
    )
    test_successful: bool = Field(
        description="Whether the health test was successful"
    )
    test_transcription_length: Optional[int] = Field(
        default=None,
        description="Length of test transcription (if successful)"
    )
    model_loaded: bool = Field(
        description="Whether the model is loaded"
    )
    test_audio_properties: Optional[AudioProperties] = Field(
        default=None,
        description="Properties of test audio (if analyzed)"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message (if unhealthy)"
    )
    timestamp: str = Field(
        description="ISO timestamp of health check"
    )


class AudioUploadResponse(BaseModel):
    """Response schema for audio upload validation."""
    
    status: str = Field(
        description="Validation status (valid or invalid)"
    )
    audio_properties: Optional[AudioProperties] = Field(
        default=None,
        description="Audio properties (if valid)"
    )
    validation_errors: Optional[List[str]] = Field(
        default=None,
        description="List of validation errors (if invalid)"
    )
    processing_time_seconds: float = Field(
        description="Time taken to validate the audio"
    )
    timestamp: str = Field(
        description="ISO timestamp of validation"
    )