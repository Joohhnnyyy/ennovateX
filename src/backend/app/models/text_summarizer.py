"""Text Summarization Model

This module contains the TextSummarizer class for BART-based text summarization
with LoRA adapter support using the custom model implementation.
"""

import logging
from typing import List, Dict, Any, Optional
import sys
import os

# Add the backend directory to the path to import model.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from text_summariser import (
        load_model_and_tokenizer,
        get_model_info,
        summarize_text,
        batch_summarize,
        cleanup_model
    )
except ImportError:
    # Fallback if text_summariser.py is not available
    load_model_and_tokenizer = None
    get_model_info = None
    summarize_text = None
    batch_summarize = None
    cleanup_model = None

from ..config import settings

logger = logging.getLogger(__name__)

class TextSummarizer:
    """BART-based text summarizer with LoRA adapter support."""
    
    def __init__(self):
        self.model_loaded = False
        self.max_length = getattr(settings, 'MAX_SUMMARY_LENGTH', 150)
        self.max_input_length = getattr(settings, 'MAX_TEXT_LENGTH', 1024)
        self._ensure_model_loaded()
        
    def _ensure_model_loaded(self):
        """Ensure the model is loaded."""
        if not self.model_loaded and load_model_and_tokenizer:
            try:
                load_model_and_tokenizer()
                self.model_loaded = True
                logger.info("LoRA BART model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load LoRA BART model: {e}")
                raise RuntimeError(f"Failed to load text summarizer model: {e}")
        elif not load_model_and_tokenizer:
            raise RuntimeError("Custom model functions not available")
    
    async def summarize(
        self,
        text: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        num_beams: int = 4,
        length_penalty: float = 2.0,
        early_stopping: bool = True,
        use_lora: bool = True,
        lora_adapter: Optional[str] = None
    ) -> str:
        """Summarize input text using LoRA BART model.
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            num_beams: Number of beams for beam search
            length_penalty: Length penalty for beam search
            early_stopping: Whether to stop early in beam search
            use_lora: Whether to use LoRA adapter (always True for this implementation)
            lora_adapter: LoRA adapter name (not used in current implementation)
            
        Returns:
            Generated summary text
        """
        try:
            self._ensure_model_loaded()
            
            # Set default lengths
            if max_length is None:
                max_length = min(self.max_length, len(text.split()) // 2)
            
            # Validate input length
            if len(text) > self.max_input_length:
                logger.warning(f"Input text truncated from {len(text)} to {self.max_input_length} characters")
                text = text[:self.max_input_length]
            
            # Use the custom summarize_text function
            if not summarize_text:
                raise RuntimeError("Summarize function not available")
            
            summary = summarize_text(
                text=text,
                max_input_length=512,
                max_output_length=max_length,
                num_beams=num_beams,
                length_penalty=length_penalty,
                early_stopping=early_stopping
            )
            
            logger.info(f"Successfully generated summary of length {len(summary)} from input of length {len(text)}")
            return summary
            
        except Exception as e:
            logger.error(f"Error in text summarization: {e}")
            raise

    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        try:
            model, tokenizer = self._get_model_and_tokenizer()
            
            # Check if using LoRA adapter
            foundation_model = None
            if self.model_loader:
                foundation_model = self.model_loader.get_foundation_model("text_summarizer")
            
            return {
                "model_type": "text_summarizer",
                "base_model": settings.TEXT_SUMMARIZER_MODEL,
                "lora_adapter": settings.TEXT_SUMMARIZER_LORA,
                "using_lora": foundation_model is not None,
                "device": self.device,
                "max_input_length": self.max_input_length,
                "max_summary_length": self.max_length,
                "vocab_size": tokenizer.vocab_size if hasattr(tokenizer, 'vocab_size') else None
            }
            
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {"error": str(e)}