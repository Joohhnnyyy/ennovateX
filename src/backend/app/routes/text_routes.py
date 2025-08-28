"""Text processing routes for the EnnovateX AI platform.

Provides endpoints for text summarization and question answering.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any, List
from datetime import datetime
import logging
from ..dependencies import (
    get_text_summarizer,
    validate_text_input,
    check_rate_limit,
    get_settings
)
from ..models.text_summarizer import TextSummarizer
from ..schemas.text_schemas import (
    TextSummarizationRequest,
    TextSummarizationResponse
)
from ..config import Settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/text",
    tags=["text processing"]
)


@router.post("/summarize", response_model=TextSummarizationResponse)
async def summarize_text(
    request: TextSummarizationRequest,
    background_tasks: BackgroundTasks,
    summarizer: TextSummarizer = Depends(get_text_summarizer),
    _: None = Depends(check_rate_limit),
    settings: Settings = Depends(get_settings)
) -> TextSummarizationResponse:
    """Summarize input text using BART model with optional LoRA adapters.
    
    Args:
        request: Summarization request containing text and parameters
        background_tasks: FastAPI background tasks
        summarizer: Text summarizer model instance
        
    Returns:
        TextSummarizationResponse containing the generated summary
        
    Raises:
        HTTPException: If summarization fails
    """
    try:
        # Validate text input
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text input cannot be empty"
            )
        
        logger.info(f"Processing summarization request for text length: {len(request.text)}")
        
        # Validate text length
        if len(request.text) > settings.MAX_TEXT_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Text length exceeds maximum allowed length of {settings.MAX_TEXT_LENGTH} characters"
            )
        
        # Generate summary
        if request.summary_type == "abstractive":
            summary = await summarizer.summarize(
                text=request.text,
                max_length=request.max_length,
                min_length=request.min_length,
                use_lora=request.use_lora,
                lora_adapter=request.lora_adapter
            )
        elif request.summary_type == "extractive":
            summary = await summarizer.extractive_summarize(
                text=request.text,
                num_sentences=3
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid summarization method. Use 'abstractive' or 'extractive'"
            )
        
        # Log successful processing
        background_tasks.add_task(
            logger.info,
            f"Successfully processed summarization request. Summary length: {len(summary)}"
        )
        
        return TextSummarizationResponse(
            summary=summary,
            original_summary=summary,
            summary_type=request.summary_type,
            original_length=len(request.text),
            summary_length=len(summary),
            compression_ratio=round(len(summary) / len(request.text), 3),
            processing_time_seconds=0.0,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in text summarization: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to summarize text: {str(e)}"
        )








@router.get("/model-info")
async def get_model_info(
    summarizer: TextSummarizer = Depends(get_text_summarizer)
) -> Dict[str, Any]:
    """Get information about the current text processing model.
    
    Returns:
        Dict containing model information
    """
    return summarizer.get_model_info()