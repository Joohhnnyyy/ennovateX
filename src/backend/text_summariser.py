"""Model loading and wrapping for LoRA-enhanced BART summarization.

This module provides functionality to load and use a BART model with LoRA adapters
for text summarization tasks.
"""

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import get_peft_model, LoraConfig
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Force CPU (or GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")

# Model configuration
MODEL_NAME = "facebook/bart-large-cnn"
LORA_PATH = "./lora-bart-summarizer"

# Global model and tokenizer variables
tokenizer: Optional[AutoTokenizer] = None
model: Optional[AutoModelForSeq2SeqLM] = None


def load_model_and_tokenizer(model_name: str = MODEL_NAME, lora_path: str = LORA_PATH) -> tuple:
    """Load tokenizer and model with LoRA adapter.
    
    Args:
        model_name: Name of the base model to load
        lora_path: Path to the LoRA adapter
        
    Returns:
        Tuple of (tokenizer, model)
        
    Raises:
        Exception: If model or LoRA adapter loading fails
    """
    global tokenizer, model
    
    try:
        logger.info(f"Loading tokenizer from {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        logger.info(f"Loading base model from {model_name}")
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        model.to(device)
        
        # Check if LoRA adapter exists
        lora_path_obj = Path(lora_path)
        if lora_path_obj.exists():
            logger.info(f"Loading LoRA adapter from {lora_path}")
            lora_config = LoraConfig.from_pretrained(lora_path)
            model = get_peft_model(model, lora_config)
            logger.info("LoRA adapter loaded successfully")
        else:
            logger.warning(f"LoRA adapter not found at {lora_path}. Using base model only.")
        
        logger.info("Model and tokenizer loaded successfully")
        return tokenizer, model
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise


def get_model_info() -> Dict[str, Any]:
    """Get information about the loaded model.
    
    Returns:
        Dictionary containing model information
    """
    global model, tokenizer
    
    if model is None or tokenizer is None:
        return {
            "loaded": False,
            "error": "Model not loaded"
        }
    
    try:
        # Get model parameters count
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        return {
            "loaded": True,
            "model_name": MODEL_NAME,
            "device": str(device),
            "total_parameters": total_params,
            "trainable_parameters": trainable_params,
            "has_lora": hasattr(model, 'peft_config'),
            "vocab_size": tokenizer.vocab_size if tokenizer else None
        }
    except Exception as e:
        return {
            "loaded": True,
            "error": f"Error getting model info: {str(e)}"
        }


def summarize_text(
    text: str, 
    max_input_length: int = 512, 
    max_output_length: int = 150,
    num_beams: int = 5,
    length_penalty: float = 1.2,
    early_stopping: bool = True
) -> str:
    """Summarize input text using the loaded model.
    
    Args:
        text: Input text to summarize
        max_input_length: Maximum length of input tokens
        max_output_length: Maximum length of output summary
        num_beams: Number of beams for beam search
        length_penalty: Length penalty for generation
        early_stopping: Whether to use early stopping
        
    Returns:
        Generated summary text
        
    Raises:
        ValueError: If model is not loaded or text is empty
        Exception: If summarization fails
    """
    global model, tokenizer
    
    if model is None or tokenizer is None:
        raise ValueError("Model and tokenizer must be loaded first. Call load_model_and_tokenizer().")
    
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")
    
    try:
        logger.info(f"Summarizing text of length: {len(text)}")
        
        # Prepare input with summarization prompt
        input_text = "summarize: " + text.strip()
        
        # Tokenize input
        inputs = tokenizer(
            input_text,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=max_input_length
        )
        
        # Move inputs to device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate summary
        with torch.no_grad():
            summary_ids = model.generate(
                **inputs,
                max_length=max_output_length,
                num_beams=num_beams,
                length_penalty=length_penalty,
                early_stopping=early_stopping,
                do_sample=False,  # Use deterministic generation
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
        
        # Decode summary
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        logger.info(f"Generated summary of length: {len(summary)}")
        return summary.strip()
        
    except Exception as e:
        logger.error(f"Error during summarization: {str(e)}")
        raise Exception(f"Summarization failed: {str(e)}")


def batch_summarize(
    texts: list[str],
    max_input_length: int = 512,
    max_output_length: int = 150,
    batch_size: int = 4
) -> list[str]:
    """Summarize multiple texts in batches.
    
    Args:
        texts: List of input texts to summarize
        max_input_length: Maximum length of input tokens
        max_output_length: Maximum length of output summary
        batch_size: Number of texts to process in each batch
        
    Returns:
        List of generated summaries
        
    Raises:
        ValueError: If model is not loaded or texts list is empty
    """
    if not texts:
        raise ValueError("Texts list cannot be empty")
    
    summaries = []
    
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        batch_summaries = []
        
        for text in batch_texts:
            try:
                summary = summarize_text(
                    text,
                    max_input_length=max_input_length,
                    max_output_length=max_output_length
                )
                batch_summaries.append(summary)
            except Exception as e:
                logger.error(f"Error summarizing text in batch: {str(e)}")
                batch_summaries.append(f"Error: {str(e)}")
        
        summaries.extend(batch_summaries)
        logger.info(f"Processed batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
    
    return summaries


def cleanup_model():
    """Clean up model and tokenizer from memory."""
    global model, tokenizer
    
    if model is not None:
        del model
        model = None
        logger.info("Model cleaned up")
    
    if tokenizer is not None:
        del tokenizer
        tokenizer = None
        logger.info("Tokenizer cleaned up")
    
    # Clear CUDA cache if using GPU
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        logger.info("CUDA cache cleared")


# Initialize model and tokenizer on module import
if __name__ == "__main__":
    try:
        load_model_and_tokenizer()
        logger.info("Model initialization completed")
    except Exception as e:
        logger.error(f"Failed to initialize model: {str(e)}")


# Example usage
if __name__ == "__main__":
    # Test the summarization
    test_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, 
    in contrast to the natural intelligence displayed by humans and animals. 
    Leading AI textbooks define the field as the study of "intelligent agents": 
    any device that perceives its environment and takes actions that maximize 
    its chance of successfully achieving its goals. Colloquially, the term 
    "artificial intelligence" is often used to describe machines that mimic 
    "cognitive" functions that humans associate with the human mind, such as 
    "learning" and "problem solving".
    """
    
    try:
        summary = summarize_text(test_text)
        print(f"Original text length: {len(test_text)}")
        print(f"Summary length: {len(summary)}")
        print(f"Summary: {summary}")
        
        # Print model info
        info = get_model_info()
        print(f"\nModel info: {info}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        cleanup_model()