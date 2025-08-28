"""Audio processing routes for the EnnovateX AI platform.

Provides endpoints for speech-to-text conversion and audio analysis.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File
from typing import Dict, Any, List, Optional
import logging
import io
from ..dependencies import (
    get_audio_asr,
    validate_audio_file,
    check_rate_limit,
    get_settings
)
from ..models.audio_asr import AudioASR
from ..schemas.audio_schemas import (
    SpeechToTextRequest,
    SpeechToTextResponse,
    BatchAudioRequest,
    BatchAudioResponse,
    AudioUploadResponse,
    AudioTranslationRequest,
    AudioTranslationResponse
)
from ..config import Settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/audio",
    tags=["audio processing"]
)


@router.post("/upload", response_model=AudioUploadResponse)
async def upload_audio(
    file: UploadFile = File(...),
    _: None = Depends(check_rate_limit),
    _validated: UploadFile = Depends(validate_audio_file),
    settings: Settings = Depends(get_settings)
) -> AudioUploadResponse:
    """Upload and validate an audio file.
    
    Args:
        file: Uploaded audio file
        
    Returns:
        AudioUploadResponse with file information
        
    Raises:
        HTTPException: If file upload or validation fails
    """
    try:
        # Read file contents
        contents = await file.read()
        
        # Basic audio file validation
        if not file.content_type or not file.content_type.startswith('audio/'):
            raise HTTPException(
                status_code=400,
                detail="Invalid audio file format"
            )
        
        logger.info(f"Audio uploaded successfully: {file.filename}, size: {len(contents)} bytes")
        
        return AudioUploadResponse(
            filename=file.filename,
            size_bytes=len(contents),
            content_type=file.content_type,
            message="Audio file uploaded and validated successfully"
        )
        
    except Exception as e:
        logger.error(f"Error uploading audio: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to upload audio: {str(e)}"
        )


@router.post("/speech-to-text", response_model=SpeechToTextResponse)
async def speech_to_text(
    file: UploadFile = File(...),
    language: Optional[str] = None,
    task: Optional[str] = "transcribe",
    temperature: Optional[float] = 0.0,
    word_timestamps: Optional[bool] = False,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    asr: AudioASR = Depends(get_audio_asr),
    _: None = Depends(check_rate_limit),
    _validated: UploadFile = Depends(validate_audio_file),
    settings: Settings = Depends(get_settings)
) -> SpeechToTextResponse:
    """Convert speech in audio file to text.
    
    Args:
        file: Uploaded audio file
        language: Language code (e.g., 'en', 'es', 'fr')
        task: Task type ('transcribe' or 'translate')
        temperature: Sampling temperature (0.0 to 1.0)
        word_timestamps: Whether to include word-level timestamps
        background_tasks: FastAPI background tasks
        asr: Audio ASR model instance
        
    Returns:
        SpeechToTextResponse containing the transcription
        
    Raises:
        HTTPException: If transcription fails
    """
    try:
        logger.info(f"Processing speech-to-text for file: {file.filename}")
        
        # Read audio file
        contents = await file.read()
        
        # Validate file size
        if len(contents) > settings.MAX_AUDIO_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Audio file size exceeds maximum allowed size of {settings.MAX_AUDIO_SIZE} bytes"
            )
        
        # Convert to audio format that the model can process
        audio_data = io.BytesIO(contents)
        
        # Transcribe audio
        result = await asr.transcribe(
            audio_input=audio_data,
            language=language,
            task=task,
            temperature=temperature,
            word_timestamps=word_timestamps
        )
        
        # Extract transcription and metadata
        if isinstance(result, dict):
            transcription = result.get('text', '')
            detected_language = result.get('language', language or 'unknown')
            confidence = result.get('confidence', 0.0)
            segments = result.get('segments', [])
            words = result.get('words', [])
        else:
            transcription = str(result)
            detected_language = language or 'unknown'
            confidence = 0.8  # Default confidence
            segments = []
            words = []
        
        # Calculate duration estimate (rough)
        duration_estimate = len(contents) / (16000 * 2)  # Assuming 16kHz, 16-bit audio
        
        # Log successful processing
        background_tasks.add_task(
            logger.info,
            f"Successfully transcribed {file.filename}: {len(transcription)} characters"
        )
        
        return SpeechToTextResponse(
            transcription=transcription,
            filename=file.filename,
            detected_language=detected_language,
            confidence=confidence,
            duration_seconds=duration_estimate,
            segments=segments,
            words=words if word_timestamps else [],
            model_info=asr.get_model_info()
        )
        
    except Exception as e:
        logger.error(f"Error in speech-to-text: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to transcribe audio: {str(e)}"
        )


@router.post("/translate", response_model=AudioTranslationResponse)
async def translate_speech(
    file: UploadFile = File(...),
    target_language: Optional[str] = "en",
    temperature: Optional[float] = 0.0,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    asr: AudioASR = Depends(get_audio_asr),
    _: None = Depends(check_rate_limit),
    _validated: UploadFile = Depends(validate_audio_file),
    settings: Settings = Depends(get_settings)
) -> AudioTranslationResponse:
    """Translate speech in audio file to target language.
    
    Args:
        file: Uploaded audio file
        target_language: Target language code (default: 'en')
        temperature: Sampling temperature (0.0 to 1.0)
        background_tasks: FastAPI background tasks
        asr: Audio ASR model instance
        
    Returns:
        AudioTranslationResponse containing the translation
        
    Raises:
        HTTPException: If translation fails
    """
    try:
        logger.info(f"Processing speech translation for file: {file.filename}")
        
        # Read audio file
        contents = await file.read()
        
        # Validate file size
        if len(contents) > settings.MAX_AUDIO_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Audio file size exceeds maximum allowed size of {settings.MAX_AUDIO_SIZE} bytes"
            )
        
        # Convert to audio format
        audio_data = io.BytesIO(contents)
        
        # Translate audio (transcribe + translate)
        result = await asr.transcribe(
            audio_input=audio_data,
            task="translate",
            temperature=temperature
        )
        
        # Extract translation and metadata
        if isinstance(result, dict):
            translation = result.get('text', '')
            detected_language = result.get('language', 'unknown')
            confidence = result.get('confidence', 0.0)
        else:
            translation = str(result)
            detected_language = 'unknown'
            confidence = 0.8
        
        # Calculate duration estimate
        duration_estimate = len(contents) / (16000 * 2)
        
        # Log successful processing
        background_tasks.add_task(
            logger.info,
            f"Successfully translated {file.filename}: {len(translation)} characters"
        )
        
        return AudioTranslationResponse(
            translation=translation,
            filename=file.filename,
            source_language=detected_language,
            target_language=target_language,
            confidence=confidence,
            duration_seconds=duration_estimate,
            model_info=asr.get_model_info()
        )
        
    except Exception as e:
        logger.error(f"Error in speech translation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to translate audio: {str(e)}"
        )


@router.post("/batch-transcribe", response_model=BatchAudioResponse)
async def batch_transcribe(
    files: List[UploadFile] = File(...),
    language: Optional[str] = None,
    task: Optional[str] = "transcribe",
    temperature: Optional[float] = 0.0,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    asr: AudioASR = Depends(get_audio_asr),
    _: None = Depends(check_rate_limit),
    settings: Settings = Depends(get_settings)
) -> BatchAudioResponse:
    """Transcribe multiple audio files in a single request.
    
    Args:
        files: List of uploaded audio files
        language: Language code for all files
        task: Task type ('transcribe' or 'translate')
        temperature: Sampling temperature
        background_tasks: FastAPI background tasks
        asr: Audio ASR model instance
        
    Returns:
        BatchAudioResponse containing all transcriptions
        
    Raises:
        HTTPException: If batch processing fails
    """
    try:
        logger.info(f"Processing batch transcription for {len(files)} audio files")
        
        # Validate batch size
        if len(files) > settings.MAX_BATCH_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Batch size exceeds maximum allowed size of {settings.MAX_BATCH_SIZE}"
            )
        
        transcriptions = []
        failed_indices = []
        
        # Process each audio file
        for i, file in enumerate(files):
            try:
                # Validate file
                if not file.content_type or not file.content_type.startswith('audio/'):
                    raise ValueError(f"Invalid file type: {file.content_type}")
                
                # Read audio file
                contents = await file.read()
                if len(contents) > settings.MAX_AUDIO_SIZE:
                    raise ValueError(f"File size exceeds maximum allowed size")
                
                # Convert to audio format
                audio_data = io.BytesIO(contents)
                
                # Transcribe audio
                result = await asr.transcribe(
                    audio_input=audio_data,
                    language=language,
                    task=task,
                    temperature=temperature
                )
                
                # Extract transcription
                if isinstance(result, dict):
                    transcription = result.get('text', '')
                    detected_language = result.get('language', language or 'unknown')
                    confidence = result.get('confidence', 0.0)
                else:
                    transcription = str(result)
                    detected_language = language or 'unknown'
                    confidence = 0.8
                
                duration_estimate = len(contents) / (16000 * 2)
                
                transcriptions.append({
                    "index": i,
                    "filename": file.filename,
                    "transcription": transcription,
                    "detected_language": detected_language,
                    "confidence": confidence,
                    "duration_seconds": duration_estimate
                })
                
            except Exception as e:
                logger.warning(f"Failed to transcribe audio {i+1} ({file.filename}): {str(e)}")
                failed_indices.append(i)
                transcriptions.append({
                    "index": i,
                    "filename": file.filename,
                    "transcription": None,
                    "error": str(e),
                    "detected_language": "unknown",
                    "confidence": 0,
                    "duration_seconds": 0
                })
        
        # Log successful processing
        background_tasks.add_task(
            logger.info,
            f"Batch transcription completed. Successful: {len(transcriptions) - len(failed_indices)}, Failed: {len(failed_indices)}"
        )
        
        return BatchAudioResponse(
            transcriptions=transcriptions,
            total_processed=len(files),
            successful_count=len(transcriptions) - len(failed_indices),
            failed_count=len(failed_indices),
            failed_indices=failed_indices,
            task=task,
            model_info=asr.get_model_info()
        )
        
    except Exception as e:
        logger.error(f"Error in batch transcription: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process batch transcription: {str(e)}"
        )


@router.get("/supported-languages")
async def get_supported_languages() -> Dict[str, List[str]]:
    """Get list of supported languages for speech recognition.
    
    Returns:
        Dict containing supported language codes and names
    """
    # Common languages supported by Whisper
    languages = {
        "codes": [
            "en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh",
            "ar", "hi", "tr", "pl", "nl", "sv", "da", "no", "fi", "cs"
        ],
        "names": [
            "English", "Spanish", "French", "German", "Italian", "Portuguese",
            "Russian", "Japanese", "Korean", "Chinese", "Arabic", "Hindi",
            "Turkish", "Polish", "Dutch", "Swedish", "Danish", "Norwegian",
            "Finnish", "Czech"
        ]
    }
    return languages


@router.get("/model-info")
async def get_model_info(
    asr: AudioASR = Depends(get_audio_asr)
) -> Dict[str, Any]:
    """Get information about the current audio processing model.
    
    Returns:
        Dict containing model information
    """
    return asr.get_model_info()