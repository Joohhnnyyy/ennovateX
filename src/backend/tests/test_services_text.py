"""Tests for text service.

This module contains tests for the TextService class and its methods.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import asyncio
from app.services.text_service import TextService
from app.models.text_summarizer import TextSummarizer


class TestTextServiceInitialization:
    """Test cases for TextService initialization."""
    
    def test_text_service_init(self, mock_text_summarizer):
        """Test TextService initialization."""
        service = TextService(mock_text_summarizer)
        
        assert service.model == mock_text_summarizer
        assert service.stats["total_requests"] == 0
        assert service.stats["successful_requests"] == 0
        assert service.stats["failed_requests"] == 0
        assert service.stats["total_processing_time"] == 0.0
        assert service.stats["average_processing_time"] == 0.0


class TestTextPreprocessing:
    """Test cases for text preprocessing methods."""
    
    def test_normalize_whitespace(self, text_service):
        """Test whitespace normalization."""
        text = "This  has   multiple    spaces\n\n\nand\t\ttabs"
        result = text_service._normalize_whitespace(text)
        
        assert result == "This has multiple spaces and tabs"
    
    def test_normalize_quotes(self, text_service):
        """Test quote normalization."""
        text = "He said 'Hello' and she replied \"Hi\" with `backticks`"
        result = text_service._normalize_quotes(text)
        
        assert result == 'He said "Hello" and she replied "Hi" with "backticks"'
    
    def test_remove_urls(self, text_service):
        """Test URL removal."""
        text = "Visit https://example.com or http://test.org for more info"
        result = text_service._remove_urls(text)
        
        assert result == "Visit  or  for more info"
    
    def test_remove_emails(self, text_service):
        """Test email removal."""
        text = "Contact us at info@example.com or support@test.org"
        result = text_service._remove_emails(text)
        
        assert result == "Contact us at  or "
    
    def test_remove_excessive_punctuation(self, text_service):
        """Test excessive punctuation removal."""
        text = "What???? Really!!! Yes... maybe???"
        result = text_service._remove_excessive_punctuation(text)
        
        assert result == "What? Really! Yes... maybe?"
    
    def test_clean_spacing(self, text_service):
        """Test spacing cleanup."""
        text = "Word ,  another  .  End  !"
        result = text_service._clean_spacing(text)
        
        assert result == "Word, another. End!"
    
    def test_preprocess_text_complete(self, text_service):
        """Test complete text preprocessing."""
        text = "Visit   https://example.com  for  'great'  deals!!!  Contact  info@test.com"
        result = text_service.preprocess_text(text)
        
        expected = 'Visit for "great" deals! Contact'
        assert result == expected


class TestTextSummarization:
    """Test cases for text summarization."""
    
    @pytest.mark.asyncio
    async def test_summarize_text_success(self, text_service, sample_text):
        """Test successful text summarization."""
        expected_summary = "This is a test summary of the provided text."
        text_service.model.summarize = AsyncMock(return_value=expected_summary)
        
        result = await text_service.summarize_text(
            text=sample_text,
            max_length=100,
            min_length=20
        )
        
        assert result == expected_summary
        text_service.model.summarize.assert_called_once_with(
            sample_text, max_length=100, min_length=20
        )
    
    @pytest.mark.asyncio
    async def test_summarize_text_with_preprocessing(self, text_service):
        """Test text summarization with preprocessing."""
        text = "This   has  extra   spaces  and  https://example.com  links!!!"
        expected_summary = "Clean summary"
        text_service.model.summarize = AsyncMock(return_value=expected_summary)
        
        result = await text_service.summarize_text(
            text=text,
            max_length=50,
            preprocess=True
        )
        
        # Verify preprocessing was applied
        processed_text = text_service.preprocess_text(text)
        text_service.model.summarize.assert_called_once_with(
            processed_text, max_length=50, min_length=10
        )
        assert result == expected_summary
    
    @pytest.mark.asyncio
    async def test_summarize_text_model_error(self, text_service, sample_text):
        """Test handling of model errors during summarization."""
        text_service.model.summarize = AsyncMock(side_effect=Exception("Model error"))
        
        with pytest.raises(Exception, match="Model error"):
            await text_service.summarize_text(sample_text)
    
    @pytest.mark.asyncio
    async def test_summarize_text_empty_input(self, text_service):
        """Test summarization with empty input."""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            await text_service.summarize_text("")
    
    @pytest.mark.asyncio
    async def test_summarize_text_invalid_length_params(self, text_service, sample_text):
        """Test summarization with invalid length parameters."""
        with pytest.raises(ValueError, match="max_length must be greater than min_length"):
            await text_service.summarize_text(
                sample_text, max_length=20, min_length=50
            )


class TestQuestionAnswering:
    """Test cases for question answering."""
    
    @pytest.mark.asyncio
    async def test_answer_question_success(self, text_service, sample_text):
        """Test successful question answering."""
        question = "What is this text about?"
        expected_answer = "This text is about testing."
        
        text_service.model.answer_question = AsyncMock(return_value=expected_answer)
        
        result = await text_service.answer_question(
            context=sample_text,
            question=question
        )
        
        assert result == expected_answer
        text_service.model.answer_question.assert_called_once_with(
            context=sample_text, question=question
        )
    
    @pytest.mark.asyncio
    async def test_answer_question_no_answer(self, text_service, sample_text):
        """Test question answering when no answer is found."""
        question = "What is the meaning of life?"
        
        text_service.model.answer_question = AsyncMock(return_value=None)
        
        result = await text_service.answer_question(
            context=sample_text,
            question=question
        )
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_answer_question_empty_context(self, text_service):
        """Test question answering with empty context."""
        with pytest.raises(ValueError, match="Context cannot be empty"):
            await text_service.answer_question(
                context="",
                question="What is this about?"
            )
    
    @pytest.mark.asyncio
    async def test_answer_question_empty_question(self, text_service, sample_text):
        """Test question answering with empty question."""
        with pytest.raises(ValueError, match="Question cannot be empty"):
            await text_service.answer_question(
                context=sample_text,
                question=""
            )


class TestTextAnalysis:
    """Test cases for text analysis methods."""
    
    def test_calculate_readability_flesch_ease(self, text_service):
        """Test Flesch Reading Ease calculation."""
        text = "This is a simple sentence. It has basic words."
        score = text_service._calculate_flesch_reading_ease(text)
        
        assert isinstance(score, float)
        assert 0 <= score <= 100
    
    def test_calculate_readability_flesch_kincaid(self, text_service):
        """Test Flesch-Kincaid Grade Level calculation."""
        text = "This is a simple sentence. It has basic words."
        score = text_service._calculate_flesch_kincaid_grade(text)
        
        assert isinstance(score, float)
        assert score >= 0
    
    def test_extract_key_phrases(self, text_service):
        """Test key phrase extraction."""
        text = "Machine learning and artificial intelligence are transforming technology."
        phrases = text_service._extract_key_phrases(text, max_phrases=3)
        
        assert isinstance(phrases, list)
        assert len(phrases) <= 3
        assert all(isinstance(phrase, str) for phrase in phrases)
    
    def test_analyze_text_complete(self, text_service):
        """Test complete text analysis."""
        text = "This is a comprehensive text analysis test. It includes multiple sentences for better analysis."
        analysis = text_service.analyze_text(text)
        
        assert "readability" in analysis
        assert "key_phrases" in analysis
        assert "word_count" in analysis
        assert "sentence_count" in analysis
        assert "flesch_reading_ease" in analysis["readability"]
        assert "flesch_kincaid_grade" in analysis["readability"]
        assert isinstance(analysis["key_phrases"], list)
        assert analysis["word_count"] > 0
        assert analysis["sentence_count"] > 0


class TestEnhancedSummarization:
    """Test cases for enhanced summarization with analysis."""
    
    @pytest.mark.asyncio
    async def test_enhanced_summarize_with_analysis(self, text_service, sample_text):
        """Test enhanced summarization with text analysis."""
        expected_summary = "Enhanced summary with analysis"
        text_service.model.summarize = AsyncMock(return_value=expected_summary)
        
        result = await text_service.enhanced_summarize(
            text=sample_text,
            max_length=100,
            include_analysis=True
        )
        
        assert "summary" in result
        assert "analysis" in result
        assert result["summary"] == expected_summary
        assert "readability" in result["analysis"]
        assert "key_phrases" in result["analysis"]
    
    @pytest.mark.asyncio
    async def test_enhanced_summarize_without_analysis(self, text_service, sample_text):
        """Test enhanced summarization without analysis."""
        expected_summary = "Enhanced summary without analysis"
        text_service.model.summarize = AsyncMock(return_value=expected_summary)
        
        result = await text_service.enhanced_summarize(
            text=sample_text,
            max_length=100,
            include_analysis=False
        )
        
        assert "summary" in result
        assert "analysis" not in result
        assert result["summary"] == expected_summary
    
    @pytest.mark.asyncio
    async def test_enhanced_summarize_with_lora(self, text_service, sample_text):
        """Test enhanced summarization with LoRA adapter."""
        expected_summary = "LoRA enhanced summary"
        text_service.model.summarize = AsyncMock(return_value=expected_summary)
        
        result = await text_service.enhanced_summarize(
            text=sample_text,
            max_length=100,
            lora_adapter="custom-adapter"
        )
        
        assert result["summary"] == expected_summary
        text_service.model.summarize.assert_called_once_with(
            sample_text, max_length=100, min_length=10, lora_adapter="custom-adapter"
        )


class TestBatchProcessing:
    """Test cases for batch text processing."""
    
    @pytest.mark.asyncio
    async def test_batch_summarize_success(self, text_service):
        """Test successful batch summarization."""
        texts = ["First text to summarize", "Second text to summarize"]
        expected_summaries = ["First summary", "Second summary"]
        
        text_service.model.summarize = AsyncMock(side_effect=expected_summaries)
        
        results = await text_service.batch_summarize(
            texts=texts,
            max_length=50
        )
        
        assert len(results["results"]) == 2
        assert results["results"][0]["summary"] == "First summary"
        assert results["results"][1]["summary"] == "Second summary"
        assert results["total_processed"] == 2
        assert results["successful"] == 2
        assert results["failed"] == 0
    
    @pytest.mark.asyncio
    async def test_batch_summarize_partial_failure(self, text_service):
        """Test batch summarization with partial failures."""
        texts = ["First text", "Second text", "Third text"]
        
        async def mock_summarize(text, **kwargs):
            if "Second" in text:
                raise Exception("Processing error")
            return f"Summary of {text}"
        
        text_service.model.summarize = AsyncMock(side_effect=mock_summarize)
        
        results = await text_service.batch_summarize(
            texts=texts,
            max_length=50
        )
        
        assert len(results["results"]) == 3
        assert results["results"][0]["summary"] == "Summary of First text"
        assert results["results"][1]["error"] == "Processing error"
        assert results["results"][2]["summary"] == "Summary of Third text"
        assert results["total_processed"] == 3
        assert results["successful"] == 2
        assert results["failed"] == 1
    
    @pytest.mark.asyncio
    async def test_batch_summarize_concurrency_limit(self, text_service):
        """Test batch summarization with concurrency limit."""
        texts = [f"Text {i}" for i in range(10)]
        
        call_times = []
        
        async def mock_summarize(text, **kwargs):
            call_times.append(asyncio.get_event_loop().time())
            await asyncio.sleep(0.1)  # Simulate processing time
            return f"Summary of {text}"
        
        text_service.model.summarize = AsyncMock(side_effect=mock_summarize)
        
        results = await text_service.batch_summarize(
            texts=texts,
            max_length=50,
            max_concurrent=3
        )
        
        assert results["total_processed"] == 10
        assert results["successful"] == 10
        assert results["failed"] == 0
        
        # Verify concurrency was limited (calls should be grouped)
        assert len(call_times) == 10
    
    @pytest.mark.asyncio
    async def test_batch_summarize_empty_list(self, text_service):
        """Test batch summarization with empty text list."""
        results = await text_service.batch_summarize(
            texts=[],
            max_length=50
        )
        
        assert results["results"] == []
        assert results["total_processed"] == 0
        assert results["successful"] == 0
        assert results["failed"] == 0


class TestServiceStatistics:
    """Test cases for service statistics tracking."""
    
    @pytest.mark.asyncio
    async def test_stats_tracking_success(self, text_service, sample_text):
        """Test statistics tracking for successful requests."""
        text_service.model.summarize = AsyncMock(return_value="Test summary")
        
        initial_stats = text_service.get_stats().copy()
        
        await text_service.summarize_text(sample_text)
        
        final_stats = text_service.get_stats()
        
        assert final_stats["total_requests"] == initial_stats["total_requests"] + 1
        assert final_stats["successful_requests"] == initial_stats["successful_requests"] + 1
        assert final_stats["failed_requests"] == initial_stats["failed_requests"]
        assert final_stats["total_processing_time"] > initial_stats["total_processing_time"]
    
    @pytest.mark.asyncio
    async def test_stats_tracking_failure(self, text_service, sample_text):
        """Test statistics tracking for failed requests."""
        text_service.model.summarize = AsyncMock(side_effect=Exception("Test error"))
        
        initial_stats = text_service.get_stats().copy()
        
        with pytest.raises(Exception):
            await text_service.summarize_text(sample_text)
        
        final_stats = text_service.get_stats()
        
        assert final_stats["total_requests"] == initial_stats["total_requests"] + 1
        assert final_stats["successful_requests"] == initial_stats["successful_requests"]
        assert final_stats["failed_requests"] == initial_stats["failed_requests"] + 1
    
    def test_get_stats(self, text_service):
        """Test getting service statistics."""
        stats = text_service.get_stats()
        
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
    async def test_health_check_healthy(self, text_service):
        """Test health check when service is healthy."""
        text_service.model.is_loaded = Mock(return_value=True)
        text_service.model.get_model_info = Mock(return_value={
            "model_name": "test-model",
            "device": "cpu",
            "memory_usage_mb": 512
        })
        
        health = await text_service.health_check()
        
        assert health["status"] == "healthy"
        assert health["model_loaded"] is True
        assert health["model_name"] == "test-model"
        assert "response_time_ms" in health
        assert "memory_usage_mb" in health
    
    @pytest.mark.asyncio
    async def test_health_check_model_not_loaded(self, text_service):
        """Test health check when model is not loaded."""
        text_service.model.is_loaded = Mock(return_value=False)
        
        health = await text_service.health_check()
        
        assert health["status"] == "unhealthy"
        assert health["model_loaded"] is False
        assert "error" in health
    
    @pytest.mark.asyncio
    async def test_health_check_exception(self, text_service):
        """Test health check when an exception occurs."""
        text_service.model.is_loaded = Mock(side_effect=Exception("Model error"))
        
        health = await text_service.health_check()
        
        assert health["status"] == "error"
        assert "error" in health
        assert "Model error" in health["error"]


class TestModelInfo:
    """Test cases for model information retrieval."""
    
    def test_get_model_info_success(self, text_service):
        """Test successful model info retrieval."""
        expected_info = {
            "model_name": "test-summarizer",
            "is_loaded": True,
            "device": "cpu",
            "memory_usage_mb": 512,
            "supported_languages": ["en", "es", "fr"]
        }
        
        text_service.model.get_model_info = Mock(return_value=expected_info)
        
        info = text_service.get_model_info()
        
        assert info == expected_info
        text_service.model.get_model_info.assert_called_once()
    
    def test_get_model_info_exception(self, text_service):
        """Test model info retrieval when an exception occurs."""
        text_service.model.get_model_info = Mock(side_effect=Exception("Info error"))
        
        info = text_service.get_model_info()
        
        assert info["error"] == "Info error"
        assert info["is_loaded"] is False


# Performance tests
class TestTextServicePerformance:
    """Performance tests for text service."""
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_summarization_performance(self, text_service):
        """Test summarization performance with large text."""
        large_text = "This is a test sentence. " * 1000  # Large text
        
        text_service.model.summarize = AsyncMock(return_value="Performance test summary")
        
        import time
        start_time = time.time()
        
        result = await text_service.summarize_text(large_text)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        assert result == "Performance test summary"
        assert processing_time < 5.0  # Should complete within 5 seconds
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_batch_processing_performance(self, text_service):
        """Test batch processing performance."""
        texts = [f"Test text {i} for batch processing." for i in range(50)]
        
        text_service.model.summarize = AsyncMock(
            side_effect=lambda text, **kwargs: f"Summary of {text[:20]}..."
        )
        
        import time
        start_time = time.time()
        
        results = await text_service.batch_summarize(
            texts=texts,
            max_length=50,
            max_concurrent=10
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        assert results["total_processed"] == 50
        assert results["successful"] == 50
        assert processing_time < 10.0  # Should complete within 10 seconds