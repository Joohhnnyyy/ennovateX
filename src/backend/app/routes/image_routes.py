"""Image processing routes for the EnnovateX AI platform.

Provides endpoints for image captioning and object detection.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File
from typing import Dict, Any, List, Optional
import logging
from PIL import Image
import io
from datetime import datetime
import time
from ..dependencies import (
    validate_image_file,
    check_rate_limit,
    get_settings,
    get_image_captioner
)
from ..models.image_captioning import ImageCaptioner
from ..schemas.image_schemas import (
    ImageCaptioningRequest,
    ImageCaptioningResponse,
    VisualQuestionAnsweringRequest,
    VisualQuestionAnsweringResponse,
    BatchImageRequest,
    BatchImageResponse,
    BatchImageResult,
    BatchImageStats,
    ImageProperties,
    ImageUploadResponse,
    ImageDescriptionResponse
)
from ..config import Settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/image",
    tags=["image processing"]
)


@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    _: None = Depends(check_rate_limit),
    _validated: UploadFile = Depends(validate_image_file),
    settings: Settings = Depends(get_settings)
) -> ImageUploadResponse:
    """Upload and validate an image file.
    
    Args:
        file: Uploaded image file
        
    Returns:
        ImageUploadResponse with file information
        
    Raises:
        HTTPException: If file upload or validation fails
    """
    try:
        # Read and validate image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Get image info
        width, height = image.size
        format_type = image.format or "Unknown"
        mode = image.mode
        
        logger.info(f"Image uploaded successfully: {file.filename}, {width}x{height}, {format_type}")
        
        return ImageUploadResponse(
            filename=file.filename,
            size_bytes=len(contents),
            width=width,
            height=height,
            format=format_type,
            mode=mode,
            message="Image uploaded and validated successfully"
        )
        
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to upload image: {str(e)}"
        )


@router.post("/caption", response_model=ImageCaptioningResponse)
async def caption_image(
    file: UploadFile = File(...),
    max_length: Optional[int] = 50,
    min_length: Optional[int] = 10,
    use_lora: Optional[bool] = False,
    lora_adapter: Optional[str] = None,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    captioner: ImageCaptioner = Depends(get_image_captioner),
    _: None = Depends(check_rate_limit),
    _validated: UploadFile = Depends(validate_image_file),
    settings: Settings = Depends(get_settings)
) -> ImageCaptioningResponse:
    """Generate a caption for an uploaded image.
    
    Args:
        file: Uploaded image file
        max_length: Maximum caption length
        min_length: Minimum caption length
        use_lora: Whether to use LoRA adapter
        lora_adapter: Specific LoRA adapter name
        background_tasks: FastAPI background tasks
        captioner: Image captioner model instance
        
    Returns:
        ImageCaptioningResponse containing the generated caption
        
    Raises:
        HTTPException: If captioning fails
    """
    try:
        logger.info(f"Processing image captioning for file: {file.filename}")
        
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Generate caption
        caption = await captioner.caption_image(
            image=image,
            max_length=max_length,
            min_length=min_length,
            use_lora=use_lora,
            lora_adapter=lora_adapter
        )
        
        # Get image dimensions
        width, height = image.size
        
        # Log successful processing
        background_tasks.add_task(
            logger.info,
            f"Successfully generated caption for {file.filename}: {caption[:50]}..."
        )
        
        return ImageCaptioningResponse(
            caption=caption,
            original_caption=caption,
            confidence=0.85,
            caption_length=len(caption),
            processing_time_seconds=0.5,  # Placeholder
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in image captioning: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to caption image: {str(e)}"
        )


@router.post("/vqa", response_model=VisualQuestionAnsweringResponse)
async def visual_question_answering(
    file: UploadFile = File(...),
    question: str = "",
    max_length: Optional[int] = 50,
    use_lora: Optional[bool] = False,
    lora_adapter: Optional[str] = None,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    captioner: ImageCaptioner = Depends(get_image_captioner),
    _: None = Depends(check_rate_limit),
    _validated: UploadFile = Depends(validate_image_file),
    settings: Settings = Depends(get_settings)
) -> VisualQuestionAnsweringResponse:
    """Answer questions about an uploaded image.
    
    Args:
        file: Uploaded image file
        question: Question about the image
        max_length: Maximum answer length
        use_lora: Whether to use LoRA adapter
        lora_adapter: Specific LoRA adapter name
        background_tasks: FastAPI background tasks
        captioner: Image captioner model instance
        
    Returns:
        VQAResponse containing the answer
        
    Raises:
        HTTPException: If VQA processing fails
    """
    try:
        if not question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )
        
        logger.info(f"Processing VQA for file: {file.filename}, question: {question[:50]}...")
        
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Generate answer using VQA
        answer = await captioner.visual_question_answering(
            image=image,
            question=question,
            max_length=max_length,
            use_lora=use_lora,
            lora_adapter=lora_adapter
        )
        
        # Get image dimensions
        width, height = image.size
        
        # Calculate confidence (simplified)
        confidence = min(0.9, max(0.3, len(answer) / 50))
        
        # Log successful processing
        background_tasks.add_task(
            logger.info,
            f"Successfully answered VQA for {file.filename}: {answer[:50]}..."
        )
        
        return VisualQuestionAnsweringResponse(
            answer=answer,
            confidence=confidence,
            question_length=len(question),
            answer_length=len(answer),
            processing_time_seconds=0.5,  # Placeholder
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in VQA: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process VQA: {str(e)}"
        )


@router.post("/batch-caption", response_model=BatchImageResponse)
async def batch_caption_images(
    files: List[UploadFile] = File(...),
    max_length: Optional[int] = 50,
    min_length: Optional[int] = 10,
    use_lora: Optional[bool] = False,
    lora_adapter: Optional[str] = None,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    captioner: ImageCaptioner = Depends(get_image_captioner),
    _: None = Depends(check_rate_limit),
    settings: Settings = Depends(get_settings)
) -> BatchImageResponse:
    """Generate captions for multiple uploaded images.
    
    Args:
        files: List of uploaded image files
        max_length: Maximum caption length
        min_length: Minimum caption length
        use_lora: Whether to use LoRA adapter
        lora_adapter: Specific LoRA adapter name
        background_tasks: FastAPI background tasks
        captioner: Image captioner model instance
        
    Returns:
        BatchImageResponse containing all captions
        
    Raises:
        HTTPException: If batch processing fails
    """
    try:
        logger.info(f"Processing batch captioning for {len(files)} images")
        
        # Validate batch size
        if len(files) > settings.MAX_BATCH_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Batch size exceeds maximum allowed size of {settings.MAX_BATCH_SIZE}"
            )
        
        captions = []
        failed_indices = []
        
        # Process each image
        for i, file in enumerate(files):
            try:
                # Validate file
                if not file.content_type or not file.content_type.startswith('image/'):
                    raise ValueError(f"Invalid file type: {file.content_type}")
                
                # Read and process image
                contents = await file.read()
                if len(contents) > settings.MAX_FILE_SIZE:
                    raise ValueError(f"File size exceeds maximum allowed size")
                
                image = Image.open(io.BytesIO(contents))
                
                # Generate caption
                caption = await captioner.caption_image(
                    image=image,
                    max_length=max_length,
                    min_length=min_length,
                    use_lora=use_lora,
                    lora_adapter=lora_adapter
                )
                
                width, height = image.size
                
                captions.append({
                    "index": i,
                    "filename": file.filename,
                    "caption": caption,
                    "image_width": width,
                    "image_height": height,
                    "confidence": 0.85
                })
                
            except Exception as e:
                logger.warning(f"Failed to caption image {i+1} ({file.filename}): {str(e)}")
                failed_indices.append(i)
                captions.append({
                    "index": i,
                    "filename": file.filename,
                    "caption": None,
                    "error": str(e),
                    "image_width": 0,
                    "image_height": 0,
                    "confidence": 0
                })
        
        # Log successful processing
        background_tasks.add_task(
            logger.info,
            f"Batch captioning completed. Successful: {len(captions) - len(failed_indices)}, Failed: {len(failed_indices)}"
        )
        
        # Convert captions to BatchImageResult format
        results = []
        total_processing_time = 0.0
        total_caption_length = 0
        total_confidence = 0.0
        successful_count = 0
        
        for caption_data in captions:
            if caption_data.get('caption'):
                result = BatchImageResult(
                    index=caption_data['index'],
                    status="success",
                    caption=caption_data['caption'],
                    confidence=caption_data['confidence'],
                    caption_length=len(caption_data['caption']),
                    processing_time_seconds=1.0,  # Placeholder
                    image_properties=ImageProperties(
                        width=caption_data['image_width'],
                        height=caption_data['image_height'],
                        format="JPEG",  # Placeholder
                        size_bytes=0  # Placeholder
                    )
                )
                total_caption_length += len(caption_data['caption'])
                total_confidence += caption_data['confidence']
                successful_count += 1
            else:
                result = BatchImageResult(
                    index=caption_data['index'],
                    status="failed",
                    error=caption_data.get('error', 'Unknown error')
                )
            results.append(result)
            total_processing_time += 1.0  # Placeholder
        
        # Calculate batch statistics
        batch_stats = BatchImageStats(
            total_images=len(files),
            successful_count=successful_count,
            failed_count=len(failed_indices),
            total_processing_time_seconds=total_processing_time,
            average_processing_time=total_processing_time / len(files) if len(files) > 0 else 0.0,
            average_caption_length=total_caption_length / successful_count if successful_count > 0 else 0.0,
            average_confidence=total_confidence / successful_count if successful_count > 0 else 0.0,
            throughput_images_per_second=len(files) / total_processing_time if total_processing_time > 0 else 0.0
        )
        
        return BatchImageResponse(
            results=results,
            batch_stats=batch_stats,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in batch captioning: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process batch captioning: {str(e)}"
        )


@router.post("/describe", response_model=ImageDescriptionResponse)
async def describe_image(
    file: UploadFile = File(...),
    detail_level: Optional[str] = "medium",
    use_lora: Optional[bool] = False,
    lora_adapter: Optional[str] = None,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    captioner: ImageCaptioner = Depends(get_image_captioner),
    _: None = Depends(check_rate_limit),
    _validated: UploadFile = Depends(validate_image_file)
) -> ImageDescriptionResponse:
    """Generate a detailed description of an uploaded image.
    
    Args:
        file: Uploaded image file
        detail_level: Level of detail (basic, medium, detailed)
        use_lora: Whether to use LoRA adapter
        lora_adapter: Specific LoRA adapter name
        background_tasks: FastAPI background tasks
        captioner: Image captioner model instance
        
    Returns:
        ImageDescriptionResponse containing the detailed description
        
    Raises:
        HTTPException: If description generation fails
    """
    try:
        start_time = time.time()
        logger.info(f"Processing detailed description for file: {file.filename}")
        
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Generate detailed description
        description = await captioner.detailed_description(
            image=image,
            detail_level=detail_level,
            use_lora=use_lora,
            lora_adapter=lora_adapter
        )
        
        # Get image dimensions
        width, height = image.size
        
        # Log successful processing
        background_tasks.add_task(
            logger.info,
            f"Successfully generated detailed description for {file.filename}"
        )
        
        return ImageDescriptionResponse(
            description=description,
            description_type=detail_level,
            description_length=len(description),
            confidence=0.8,
            processing_time_seconds=time.time() - start_time,
            timestamp=datetime.now().isoformat(),
            image_properties=ImageProperties(
                width=width,
                height=height,
                channels=3,
                format=file.content_type
            )
        )
        
    except Exception as e:
        logger.error(f"Error in detailed description: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate description: {str(e)}"
        )


@router.get("/model-info")
async def get_model_info(
    captioner: ImageCaptioner = Depends(get_image_captioner)
) -> Dict[str, Any]:
    """Get information about the current image processing model.
    
    Returns:
        Dict containing model information
    """
    return captioner.get_model_info()