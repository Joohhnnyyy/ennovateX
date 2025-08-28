"""Model Utilities

This module contains utility functions for loading and managing ML models,
including device detection, model caching, and LoRA adapter management.
"""

import torch
import logging
from typing import Optional, Dict, Any, Union
from pathlib import Path
from transformers import AutoModel, AutoTokenizer, AutoProcessor
from peft import PeftModel, PeftConfig
import gc

from ..config import settings, MODEL_CONFIGS

logger = logging.getLogger(__name__)

def get_device() -> str:
    """Automatically detect the best available device."""
    if settings.DEVICE != "auto":
        return settings.DEVICE
    
    if torch.cuda.is_available():
        return "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"

def clear_memory():
    """Clear GPU/CPU memory."""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

class ModelLoader:
    """Centralized model loader and manager."""
    
    def __init__(self):
        self.device = get_device()
        self.models: Dict[str, Any] = {}
        self.tokenizers: Dict[str, Any] = {}
        self.processors: Dict[str, Any] = {}
        # Removed foundation_models dependency
        
        # Create cache directory
        self.cache_dir = Path(settings.MODEL_CACHE_DIR)
        self.cache_dir.mkdir(exist_ok=True)
        
        logger.info(f"ModelLoader initialized with device: {self.device}")
    
    async def initialize_models(self):
        """Initialize all required models."""
        logger.info("Starting model initialization...")
        
        try:
            # Initialize text summarizer
            await self._load_text_summarizer()
            
            # Initialize image captioner
            await self._load_image_captioner()
            
            # Initialize audio ASR
            await self._load_audio_asr()
            
            logger.info("All models initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize models: {e}")
            raise
    
    async def _load_text_summarizer(self):
        """Load text summarization model with optional LoRA adapter."""
        config = MODEL_CONFIGS["text_summarizer"]
        model_name = config["model_name"]
        lora_adapter = config["lora_adapter"]
        
        logger.info(f"Loading text summarizer: {model_name}")
        
        try:
            # Load base model without adapter for now
            from transformers import AutoModelForSeq2SeqLM
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name,
                cache_dir=self.cache_dir,
                torch_dtype=torch.float16 if self.device != "cpu" else torch.float32
            ).to(self.device)
            
            tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                cache_dir=self.cache_dir
            )
            
            self.models["text_summarizer"] = model
            self.tokenizers["text_summarizer"] = tokenizer
            
            logger.info("Text summarizer loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load text summarizer: {e}")
            raise
    
    async def _load_image_captioner(self):
        """Load image captioning model with optional LoRA adapter."""
        config = MODEL_CONFIGS["image_captioner"]
        model_name = config["model_name"]
        lora_adapter = config["lora_adapter"]
        
        logger.info(f"Loading image captioner: {model_name}")
        
        try:
            # Load base model without adapter for now
            from transformers import BlipForConditionalGeneration, BlipProcessor
            model = BlipForConditionalGeneration.from_pretrained(
                model_name,
                cache_dir=self.cache_dir,
                torch_dtype=torch.float16 if self.device != "cpu" else torch.float32
            ).to(self.device)
            
            processor = BlipProcessor.from_pretrained(
                model_name,
                cache_dir=self.cache_dir
            )
            
            self.models["image_captioner"] = model
            self.processors["image_captioner"] = processor
            
            logger.info("Image captioner loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load image captioner: {e}")
            raise
    
    async def _load_audio_asr(self):
        """Load audio ASR model."""
        config = MODEL_CONFIGS["audio_asr"]
        model_name = config["model_name"]
        
        logger.info(f"Loading audio ASR: {model_name}")
        
        try:
            from transformers import WhisperForConditionalGeneration, WhisperProcessor
            
            model = WhisperForConditionalGeneration.from_pretrained(
                model_name,
                cache_dir=self.cache_dir,
                torch_dtype=torch.float16 if self.device != "cpu" else torch.float32
            ).to(self.device)
            
            processor = WhisperProcessor.from_pretrained(
                model_name,
                cache_dir=self.cache_dir
            )
            
            self.models["audio_asr"] = model
            self.processors["audio_asr"] = processor
            
            logger.info("Audio ASR loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load audio ASR: {e}")
            raise
    
    def get_model(self, model_type: str) -> Optional[Any]:
        """Get a loaded model by type."""
        return self.models.get(model_type)
    
    def get_tokenizer(self, model_type: str) -> Optional[Any]:
        """Get a tokenizer by model type."""
        return self.tokenizers.get(model_type)
    
    def get_processor(self, model_type: str) -> Optional[Any]:
        """Get a processor by model type."""
        return self.processors.get(model_type)
    

    
    async def cleanup(self):
        """Clean up models and free memory."""
        logger.info("Cleaning up models...")
        
        # Clear all model references
        self.models.clear()
        self.tokenizers.clear()
        self.processors.clear()
        
        # Clear memory
        clear_memory()
        
        logger.info("Model cleanup completed")
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage statistics."""
        stats = {
            "device": self.device,
            "loaded_models": list(self.models.keys()),
            "model_count": len(self.models)
        }
        
        if torch.cuda.is_available() and self.device == "cuda":
            stats.update({
                "gpu_memory_allocated": torch.cuda.memory_allocated(),
                "gpu_memory_reserved": torch.cuda.memory_reserved(),
                "gpu_memory_cached": torch.cuda.memory_cached()
            })
        
        return stats