"""Pydantic schemas for text processing endpoints.

Defines request and response models for text summarization and analysis.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


class TextSummarizationRequest(BaseModel):
    """Request schema for text summarization."""
    
    text: str = Field(
        ...,
        min_length=10,
        max_length=50000,
        description="Text to summarize"
    )
    max_length: int = Field(
        default=150,
        ge=10,
        le=500,
        description="Maximum length of the summary"
    )
    min_length: int = Field(
        default=30,
        ge=5,
        le=200,
        description="Minimum length of the summary"
    )
    summary_type: str = Field(
        default="abstractive",
        description="Type of summarization (abstractive or extractive)"
    )
    include_analysis: bool = Field(
        default=False,
        description="Whether to include text analysis in the response"
    )
    use_lora: bool = Field(
        default=False,
        description="Whether to use LoRA adapter for fine-tuned summarization"
    )
    lora_adapter: Optional[str] = Field(
        default=None,
        description="Specific LoRA adapter name to use"
    )
    
    @validator('summary_type')
    def validate_summary_type(cls, v):
        if v not in ['abstractive', 'extractive']:
            raise ValueError('summary_type must be either "abstractive" or "extractive"')
        return v
    
    @validator('min_length', 'max_length')
    def validate_lengths(cls, v, values):
        if 'min_length' in values and 'max_length' in values:
            if values['min_length'] >= values['max_length']:
                raise ValueError('min_length must be less than max_length')
        return v


class ReadabilityMetrics(BaseModel):
    """Schema for text readability metrics."""
    
    flesch_reading_ease: float = Field(
        description="Flesch Reading Ease score (0-100)"
    )
    flesch_kincaid_grade: float = Field(
        description="Flesch-Kincaid Grade Level"
    )
    avg_sentence_length: float = Field(
        description="Average sentence length in words"
    )
    avg_syllables_per_word: float = Field(
        description="Average syllables per word"
    )
    total_sentences: int = Field(
        description="Total number of sentences"
    )
    total_words: int = Field(
        description="Total number of words"
    )
    total_syllables: int = Field(
        description="Total number of syllables"
    )


class KeyPhrase(BaseModel):
    """Schema for key phrase extraction results."""
    
    phrase: str = Field(
        description="The extracted phrase"
    )
    frequency: int = Field(
        description="Frequency of the phrase in the text"
    )
    type: str = Field(
        description="Type of phrase (word or phrase)"
    )
    score: float = Field(
        description="Relevance score of the phrase"
    )


class TextAnalysis(BaseModel):
    """Schema for comprehensive text analysis."""
    
    readability: ReadabilityMetrics = Field(
        description="Readability metrics for the text"
    )
    key_phrases: List[KeyPhrase] = Field(
        description="Extracted key phrases from the text"
    )
    summary_readability: ReadabilityMetrics = Field(
        description="Readability metrics for the summary"
    )


class TextSummarizationResponse(BaseModel):
    """Response schema for text summarization."""
    
    summary: str = Field(
        description="The generated summary"
    )
    original_summary: str = Field(
        description="The original summary before postprocessing"
    )
    summary_type: str = Field(
        description="Type of summarization used"
    )
    original_length: int = Field(
        description="Length of the original text in characters"
    )
    summary_length: int = Field(
        description="Length of the summary in characters"
    )
    compression_ratio: float = Field(
        description="Ratio of summary length to original length"
    )
    processing_time_seconds: float = Field(
        description="Time taken to process the request in seconds"
    )
    timestamp: str = Field(
        description="ISO timestamp of when the processing completed"
    )
    text_analysis: Optional[TextAnalysis] = Field(
        default=None,
        description="Optional text analysis results"
    )


class QuestionAnsweringRequest(BaseModel):
    """Request schema for question answering."""
    
    context: str = Field(
        ...,
        min_length=10,
        max_length=50000,
        description="Context text for answering the question"
    )
    question: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Question to answer based on the context"
    )
    max_answer_length: int = Field(
        default=100,
        ge=10,
        le=300,
        description="Maximum length of the answer"
    )
    use_lora: bool = Field(
        default=False,
        description="Whether to use LoRA adapter"
    )
    lora_adapter: Optional[str] = Field(
        default=None,
        description="Specific LoRA adapter name to use"
    )


class QuestionAnsweringResponse(BaseModel):
    """Response schema for question answering."""
    
    answer: str = Field(
        description="The generated answer"
    )
    confidence: float = Field(
        description="Confidence score for the answer (0-1)"
    )
    context_length: int = Field(
        description="Length of the context text"
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


class BatchTextRequest(BaseModel):
    """Request schema for batch text processing."""
    
    texts: List[str] = Field(
        ...,
        min_items=1,
        max_items=50,
        description="List of texts to process"
    )
    max_length: int = Field(
        default=150,
        ge=10,
        le=500,
        description="Maximum length of each summary"
    )
    min_length: int = Field(
        default=30,
        ge=5,
        le=200,
        description="Minimum length of each summary"
    )
    summary_type: str = Field(
        default="abstractive",
        description="Type of summarization"
    )
    use_lora: bool = Field(
        default=False,
        description="Whether to use LoRA adapter"
    )
    lora_adapter: Optional[str] = Field(
        default=None,
        description="Specific LoRA adapter name to use"
    )
    
    @validator('texts')
    def validate_texts(cls, v):
        for i, text in enumerate(v):
            if len(text) < 10:
                raise ValueError(f'Text at index {i} is too short (minimum 10 characters)')
            if len(text) > 50000:
                raise ValueError(f'Text at index {i} is too long (maximum 50000 characters)')
        return v
    
    @validator('summary_type')
    def validate_summary_type(cls, v):
        if v not in ['abstractive', 'extractive']:
            raise ValueError('summary_type must be either "abstractive" or "extractive"')
        return v


class BatchTextResult(BaseModel):
    """Schema for individual batch processing result."""
    
    index: int = Field(
        description="Index of the text in the original batch"
    )
    status: str = Field(
        description="Processing status (success or failed)"
    )
    summary: Optional[str] = Field(
        default=None,
        description="Generated summary (if successful)"
    )
    original_length: Optional[int] = Field(
        default=None,
        description="Length of original text"
    )
    summary_length: Optional[int] = Field(
        default=None,
        description="Length of summary"
    )
    compression_ratio: Optional[float] = Field(
        default=None,
        description="Compression ratio"
    )
    processing_time_seconds: Optional[float] = Field(
        default=None,
        description="Processing time for this text"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message (if failed)"
    )


class BatchStats(BaseModel):
    """Schema for batch processing statistics."""
    
    total_texts: int = Field(
        description="Total number of texts processed"
    )
    successful_count: int = Field(
        description="Number of successfully processed texts"
    )
    failed_count: int = Field(
        description="Number of failed texts"
    )
    total_processing_time_seconds: float = Field(
        description="Total processing time for the batch"
    )
    total_original_length: int = Field(
        description="Total length of all original texts"
    )
    total_summary_length: int = Field(
        description="Total length of all summaries"
    )
    average_compression_ratio: float = Field(
        description="Average compression ratio across all texts"
    )
    average_processing_time: float = Field(
        description="Average processing time per text"
    )
    throughput_texts_per_second: float = Field(
        description="Processing throughput in texts per second"
    )


class BatchTextResponse(BaseModel):
    """Response schema for batch text processing."""
    
    results: List[BatchTextResult] = Field(
        description="Results for each text in the batch"
    )
    batch_stats: BatchStats = Field(
        description="Statistics for the entire batch"
    )
    timestamp: str = Field(
        description="ISO timestamp of batch completion"
    )


class ModelInfo(BaseModel):
    """Schema for model information."""
    
    model_name: str = Field(
        description="Name of the model"
    )
    model_type: str = Field(
        description="Type of the model"
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
    max_input_length: int = Field(
        description="Maximum input length the model can handle"
    )
    max_output_length: int = Field(
        description="Maximum output length the model can generate"
    )


class ServiceStats(BaseModel):
    """Schema for service statistics."""
    
    total_requests: int = Field(
        description="Total number of requests processed"
    )
    successful_requests: int = Field(
        description="Number of successful requests"
    )
    failed_requests: int = Field(
        description="Number of failed requests"
    )
    total_text_length: int = Field(
        description="Total length of all processed texts"
    )
    total_processing_time: float = Field(
        description="Total processing time in seconds"
    )
    average_processing_time_seconds: float = Field(
        description="Average processing time per request"
    )
    average_text_length: float = Field(
        description="Average text length per request"
    )


class ServiceConfig(BaseModel):
    """Schema for service configuration."""
    
    max_text_length: int = Field(
        description="Maximum allowed text length"
    )
    max_batch_size: int = Field(
        description="Maximum batch size"
    )
    max_concurrent_requests: int = Field(
        description="Maximum concurrent requests"
    )


class TextServiceStatsResponse(BaseModel):
    """Response schema for text service statistics."""
    
    processing_stats: ServiceStats = Field(
        description="Processing statistics"
    )
    model_info: ModelInfo = Field(
        description="Information about the text model"
    )
    service_config: ServiceConfig = Field(
        description="Service configuration"
    )


class HealthCheckResponse(BaseModel):
    """Response schema for health check."""
    
    status: str = Field(
        description="Health status (healthy or unhealthy)"
    )
    test_successful: bool = Field(
        description="Whether the health test was successful"
    )
    test_summary_length: Optional[int] = Field(
        default=None,
        description="Length of test summary (if successful)"
    )
    model_loaded: bool = Field(
        description="Whether the model is loaded"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message (if unhealthy)"
    )
    timestamp: str = Field(
        description="ISO timestamp of health check"
    )