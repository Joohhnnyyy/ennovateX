"""Text processing service for the EnnovateX AI platform.

Provides business logic and postprocessing for text summarization and analysis.
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import asyncio
import re
import string
from collections import Counter
from ..models.text_summarizer import TextSummarizer
from ..config import Settings

logger = logging.getLogger(__name__)


class TextService:
    """Service class for text processing operations."""
    
    def __init__(self, summarizer: TextSummarizer, settings: Settings):
        self.summarizer = summarizer
        self.settings = settings
        self.processing_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_text_length": 0,
            "total_processing_time": 0.0
        }
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text before summarization.
        
        Args:
            text: Input text to preprocess
            
        Returns:
            Cleaned and preprocessed text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Normalize quotes
        text = re.sub(r'["''`]', '"', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # Remove excessive punctuation
        text = re.sub(r'[.]{3,}', '...', text)
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        
        # Clean up spacing around punctuation
        text = re.sub(r'\s+([,.!?;:])', r'\1', text)
        text = re.sub(r'([,.!?;:])\s*([,.!?;:])', r'\1 \2', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def postprocess_summary(self, summary: str, original_length: int) -> str:
        """Postprocess generated summary.
        
        Args:
            summary: Generated summary text
            original_length: Length of original text
            
        Returns:
            Cleaned and improved summary
        """
        # Remove leading/trailing whitespace
        summary = summary.strip()
        
        # Ensure proper sentence endings
        if summary and not summary.endswith(('.', '!', '?')):
            summary += '.'
        
        # Remove redundant phrases
        redundant_phrases = [
            "In summary,", "To summarize,", "In conclusion,", 
            "The text discusses", "This article talks about",
            "The main points are", "Key points include"
        ]
        
        for phrase in redundant_phrases:
            if summary.lower().startswith(phrase.lower()):
                summary = summary[len(phrase):].strip()
                if summary and not summary[0].isupper():
                    summary = summary[0].upper() + summary[1:]
                break
        
        # Ensure proper capitalization
        if summary and not summary[0].isupper():
            summary = summary[0].upper() + summary[1:]
        
        return summary
    
    def calculate_readability_score(self, text: str) -> Dict[str, float]:
        """Calculate readability metrics for text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing readability metrics
        """
        # Basic text statistics
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        words = text.split()
        syllables = 0
        
        # Simple syllable counting (approximation)
        for word in words:
            word = word.lower().strip(string.punctuation)
            if word:
                # Count vowel groups
                vowel_groups = re.findall(r'[aeiouy]+', word)
                syllable_count = len(vowel_groups)
                # Adjust for silent 'e'
                if word.endswith('e') and syllable_count > 1:
                    syllable_count -= 1
                syllables += max(1, syllable_count)
        
        # Calculate metrics
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        avg_syllables_per_word = syllables / len(words) if words else 0
        
        # Flesch Reading Ease (approximation)
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        flesch_score = max(0, min(100, flesch_score))  # Clamp to 0-100
        
        # Flesch-Kincaid Grade Level (approximation)
        grade_level = (0.39 * avg_sentence_length) + (11.8 * avg_syllables_per_word) - 15.59
        grade_level = max(0, grade_level)
        
        return {
            "flesch_reading_ease": round(flesch_score, 2),
            "flesch_kincaid_grade": round(grade_level, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "avg_syllables_per_word": round(avg_syllables_per_word, 2),
            "total_sentences": len(sentences),
            "total_words": len(words),
            "total_syllables": syllables
        }
    
    def extract_key_phrases(self, text: str, max_phrases: int = 10) -> List[Dict[str, Any]]:
        """Extract key phrases from text using simple frequency analysis.
        
        Args:
            text: Input text to analyze
            max_phrases: Maximum number of phrases to return
            
        Returns:
            List of key phrases with scores
        """
        # Simple preprocessing
        text_lower = text.lower()
        
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Filter out common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
        }
        
        # Filter words
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count word frequencies
        word_freq = Counter(filtered_words)
        
        # Generate 2-grams and 3-grams
        bigrams = [' '.join(filtered_words[i:i+2]) for i in range(len(filtered_words)-1)]
        trigrams = [' '.join(filtered_words[i:i+3]) for i in range(len(filtered_words)-2)]
        
        # Count phrase frequencies
        phrase_freq = Counter(bigrams + trigrams)
        
        # Combine and score phrases
        all_phrases = []
        
        # Add single words
        for word, freq in word_freq.most_common(max_phrases):
            all_phrases.append({
                "phrase": word,
                "frequency": freq,
                "type": "word",
                "score": freq
            })
        
        # Add multi-word phrases
        for phrase, freq in phrase_freq.most_common(max_phrases):
            if freq > 1:  # Only include phrases that appear more than once
                all_phrases.append({
                    "phrase": phrase,
                    "frequency": freq,
                    "type": "phrase",
                    "score": freq * 1.5  # Boost multi-word phrases
                })
        
        # Sort by score and return top phrases
        all_phrases.sort(key=lambda x: x["score"], reverse=True)
        return all_phrases[:max_phrases]
    
    async def enhanced_summarization(
        self,
        text: str,
        max_length: int = 150,
        min_length: int = 30,
        summary_type: str = "abstractive",
        include_analysis: bool = False,
        use_lora: bool = False,
        lora_adapter: Optional[str] = None
    ) -> Dict[str, Any]:
        """Enhanced text summarization with additional analysis.
        
        Args:
            text: Input text to summarize
            max_length: Maximum summary length
            min_length: Minimum summary length
            summary_type: Type of summary (abstractive or extractive)
            include_analysis: Whether to include text analysis
            use_lora: Whether to use LoRA adapter
            lora_adapter: Specific LoRA adapter name
            
        Returns:
            Enhanced summary with metadata
        """
        try:
            start_time = datetime.utcnow()
            self.processing_stats["total_requests"] += 1
            self.processing_stats["total_text_length"] += len(text)
            
            # Preprocess text
            processed_text = self.preprocess_text(text)
            
            # Generate summary
            if summary_type == "extractive":
                summary = await self.summarizer.extractive_summarization(
                    text=processed_text,
                    max_length=max_length,
                    min_length=min_length,
                    use_lora=use_lora,
                    lora_adapter=lora_adapter
                )
            else:
                summary = await self.summarizer.abstractive_summarization(
                    text=processed_text,
                    max_length=max_length,
                    min_length=min_length,
                    use_lora=use_lora,
                    lora_adapter=lora_adapter
                )
            
            # Postprocess summary
            final_summary = self.postprocess_summary(summary, len(text))
            
            # Calculate processing time
            end_time = datetime.utcnow()
            processing_time = (end_time - start_time).total_seconds()
            self.processing_stats["total_processing_time"] += processing_time
            
            # Build result
            result = {
                "summary": final_summary,
                "original_summary": summary,
                "summary_type": summary_type,
                "original_length": len(text),
                "summary_length": len(final_summary),
                "compression_ratio": len(final_summary) / len(text) if text else 0,
                "processing_time_seconds": processing_time,
                "timestamp": end_time.isoformat()
            }
            
            # Add optional analysis
            if include_analysis:
                result["text_analysis"] = {
                    "readability": self.calculate_readability_score(text),
                    "key_phrases": self.extract_key_phrases(text),
                    "summary_readability": self.calculate_readability_score(final_summary)
                }
            
            self.processing_stats["successful_requests"] += 1
            logger.info(f"Enhanced summarization completed in {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            self.processing_stats["failed_requests"] += 1
            logger.error(f"Enhanced summarization failed: {str(e)}")
            raise
    
    async def batch_summarization(
        self,
        texts: List[str],
        max_length: int = 150,
        min_length: int = 30,
        summary_type: str = "abstractive",
        use_lora: bool = False,
        lora_adapter: Optional[str] = None
    ) -> Dict[str, Any]:
        """Batch text summarization with performance analysis.
        
        Args:
            texts: List of texts to summarize
            max_length: Maximum summary length
            min_length: Minimum summary length
            summary_type: Type of summary (abstractive or extractive)
            use_lora: Whether to use LoRA adapter
            lora_adapter: Specific LoRA adapter name
            
        Returns:
            Batch results with performance metrics
        """
        start_time = datetime.utcnow()
        results = []
        
        # Process texts with concurrency limit
        semaphore = asyncio.Semaphore(self.settings.MAX_CONCURRENT_REQUESTS)
        
        async def process_single_text(index: int, text: str) -> Dict[str, Any]:
            async with semaphore:
                try:
                    result = await self.enhanced_summarization(
                        text=text,
                        max_length=max_length,
                        min_length=min_length,
                        summary_type=summary_type,
                        use_lora=use_lora,
                        lora_adapter=lora_adapter
                    )
                    result["index"] = index
                    result["status"] = "success"
                    return result
                except Exception as e:
                    return {
                        "index": index,
                        "status": "failed",
                        "error": str(e)
                    }
        
        # Execute batch processing
        tasks = [process_single_text(i, text) for i, text in enumerate(texts)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Calculate batch statistics
        end_time = datetime.utcnow()
        total_processing_time = (end_time - start_time).total_seconds()
        
        successful_results = [r for r in results if isinstance(r, dict) and r.get("status") == "success"]
        failed_results = [r for r in results if isinstance(r, dict) and r.get("status") == "failed"]
        
        total_original_length = sum(r.get("original_length", 0) for r in successful_results)
        total_summary_length = sum(r.get("summary_length", 0) for r in successful_results)
        
        return {
            "results": results,
            "batch_stats": {
                "total_texts": len(texts),
                "successful_count": len(successful_results),
                "failed_count": len(failed_results),
                "total_processing_time_seconds": total_processing_time,
                "total_original_length": total_original_length,
                "total_summary_length": total_summary_length,
                "average_compression_ratio": total_summary_length / total_original_length if total_original_length > 0 else 0,
                "average_processing_time": total_processing_time / len(texts) if texts else 0,
                "throughput_texts_per_second": len(texts) / total_processing_time if total_processing_time > 0 else 0
            },
            "timestamp": end_time.isoformat()
        }
    
    def get_service_stats(self) -> Dict[str, Any]:
        """Get service processing statistics.
        
        Returns:
            Dictionary containing service statistics
        """
        avg_processing_time = (
            self.processing_stats["total_processing_time"] / 
            self.processing_stats["successful_requests"]
            if self.processing_stats["successful_requests"] > 0 else 0
        )
        
        avg_text_length = (
            self.processing_stats["total_text_length"] / 
            self.processing_stats["total_requests"]
            if self.processing_stats["total_requests"] > 0 else 0
        )
        
        return {
            "processing_stats": {
                **self.processing_stats,
                "average_processing_time_seconds": avg_processing_time,
                "average_text_length": avg_text_length
            },
            "model_info": self.summarizer.get_model_info(),
            "service_config": {
                "max_text_length": self.settings.MAX_TEXT_LENGTH,
                "max_batch_size": self.settings.MAX_BATCH_SIZE,
                "max_concurrent_requests": self.settings.MAX_CONCURRENT_REQUESTS
            }
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the text service.
        
        Returns:
            Health check results
        """
        try:
            # Test with a simple text
            test_text = "This is a simple test text for health checking. It contains multiple sentences to verify that the summarization model is working correctly."
            
            test_result = await self.summarizer.abstractive_summarization(
                text=test_text,
                max_length=50,
                min_length=10
            )
            
            return {
                "status": "healthy",
                "test_successful": True,
                "test_summary_length": len(test_result),
                "model_loaded": True,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "test_successful": False,
                "error": str(e),
                "model_loaded": False,
                "timestamp": datetime.utcnow().isoformat()
            }