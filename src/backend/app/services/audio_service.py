"""Audio processing service for the EnnovateX AI platform.

Provides business logic and postprocessing for speech-to-text and audio analysis.
"""

import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime
import asyncio
import io
import wave
import numpy as np
from pydub import AudioSegment
from pydub.utils import which
from ..models.audio_asr import AudioASR
from ..config import Settings

logger = logging.getLogger(__name__)


class AudioService:
    """Service class for audio processing operations."""
    
    def __init__(self, asr_model: AudioASR, settings: Settings):
        self.asr_model = asr_model
        self.settings = settings
        self.processing_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_audio_duration_seconds": 0.0,
            "total_processing_time_seconds": 0.0
        }
        
        # Check for ffmpeg availability
        self.ffmpeg_available = which("ffmpeg") is not None
        if not self.ffmpeg_available:
            logger.warning("FFmpeg not found. Some audio format conversions may not work.")
    
    def preprocess_audio(self, audio_data: bytes, target_sample_rate: int = 16000) -> Tuple[np.ndarray, int]:
        """Preprocess audio data for ASR.
        
        Args:
            audio_data: Raw audio bytes
            target_sample_rate: Target sample rate for processing
            
        Returns:
            Tuple of (audio_array, sample_rate)
        """
        try:
            # Load audio using pydub
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
            
            # Convert to mono if stereo
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Resample to target sample rate
            if audio.frame_rate != target_sample_rate:
                audio = audio.set_frame_rate(target_sample_rate)
            
            # Convert to numpy array
            audio_array = np.array(audio.get_array_of_samples(), dtype=np.float32)
            
            # Normalize audio
            if audio_array.max() > 0:
                audio_array = audio_array / np.max(np.abs(audio_array))
            
            return audio_array, target_sample_rate
            
        except Exception as e:
            logger.error(f"Audio preprocessing failed: {str(e)}")
            raise ValueError(f"Failed to preprocess audio: {str(e)}")
    
    def analyze_audio_properties(self, audio_data: bytes) -> Dict[str, Any]:
        """Analyze audio properties for metadata.
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            Dictionary containing audio analysis
        """
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
            
            duration_seconds = len(audio) / 1000.0
            
            # Calculate RMS (volume level)
            rms = audio.rms
            
            # Calculate dynamic range (simplified)
            audio_array = np.array(audio.get_array_of_samples())
            if len(audio_array) > 0:
                dynamic_range = np.max(audio_array) - np.min(audio_array)
                peak_amplitude = np.max(np.abs(audio_array))
            else:
                dynamic_range = 0
                peak_amplitude = 0
            
            # Detect silence periods (simplified)
            silence_threshold = -40  # dB
            silent_chunks = audio.split_on_silence(
                min_silence_len=500,  # 500ms
                silence_thresh=silence_threshold,
                keep_silence=100
            )
            silence_ratio = 1 - (sum(len(chunk) for chunk in silent_chunks) / len(audio))
            
            return {
                "duration_seconds": duration_seconds,
                "sample_rate": audio.frame_rate,
                "channels": audio.channels,
                "bit_depth": audio.sample_width * 8,
                "file_size_bytes": len(audio_data),
                "rms_level": rms,
                "dynamic_range": int(dynamic_range),
                "peak_amplitude": int(peak_amplitude),
                "silence_ratio": round(silence_ratio, 3),
                "estimated_speech_duration": round(duration_seconds * (1 - silence_ratio), 2)
            }
            
        except Exception as e:
            logger.error(f"Audio analysis failed: {str(e)}")
            return {
                "duration_seconds": 0,
                "error": str(e)
            }
    
    def postprocess_transcription(self, transcription: str, confidence: float = None) -> Dict[str, Any]:
        """Postprocess transcription results.
        
        Args:
            transcription: Raw transcription text
            confidence: Confidence score if available
            
        Returns:
            Processed transcription with metadata
        """
        # Clean up transcription
        cleaned_text = transcription.strip()
        
        # Remove excessive whitespace
        import re
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        
        # Basic sentence segmentation
        sentences = re.split(r'[.!?]+', cleaned_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Calculate basic metrics
        word_count = len(cleaned_text.split()) if cleaned_text else 0
        character_count = len(cleaned_text)
        sentence_count = len(sentences)
        
        # Estimate speaking rate (words per minute)
        # This would need actual audio duration for accuracy
        estimated_wpm = 0  # Placeholder
        
        return {
            "text": cleaned_text,
            "original_text": transcription,
            "word_count": word_count,
            "character_count": character_count,
            "sentence_count": sentence_count,
            "sentences": sentences,
            "confidence_score": confidence,
            "estimated_wpm": estimated_wpm,
            "language_detected": None,  # Would be filled by ASR model
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def enhanced_transcription(
        self,
        audio_data: bytes,
        language: Optional[str] = None,
        task: str = "transcribe",
        include_analysis: bool = False,
        chunk_length: int = 30,
        return_timestamps: bool = False
    ) -> Dict[str, Any]:
        """Enhanced audio transcription with additional analysis.
        
        Args:
            audio_data: Raw audio bytes
            language: Target language code
            task: Task type (transcribe or translate)
            include_analysis: Whether to include audio analysis
            chunk_length: Chunk length for long audio
            return_timestamps: Whether to return word timestamps
            
        Returns:
            Enhanced transcription with metadata
        """
        try:
            start_time = datetime.utcnow()
            self.processing_stats["total_requests"] += 1
            
            # Analyze audio properties
            audio_props = self.analyze_audio_properties(audio_data)
            duration = audio_props.get("duration_seconds", 0)
            self.processing_stats["total_audio_duration_seconds"] += duration
            
            # Preprocess audio
            audio_array, sample_rate = self.preprocess_audio(audio_data)
            
            # Perform transcription
            if task == "translate":
                result = await self.asr_model.translate_speech(
                    audio_data=audio_data,
                    target_language="en",
                    chunk_length=chunk_length
                )
            else:
                result = await self.asr_model.transcribe_audio(
                    audio_data=audio_data,
                    language=language,
                    chunk_length=chunk_length,
                    return_timestamps=return_timestamps
                )
            
            # Extract transcription text and metadata
            if isinstance(result, dict):
                transcription_text = result.get("text", "")
                detected_language = result.get("language")
                confidence = result.get("confidence")
                segments = result.get("segments", [])
            else:
                transcription_text = str(result)
                detected_language = None
                confidence = None
                segments = []
            
            # Postprocess transcription
            processed_result = self.postprocess_transcription(transcription_text, confidence)
            processed_result["language_detected"] = detected_language
            
            # Calculate processing metrics
            end_time = datetime.utcnow()
            processing_time = (end_time - start_time).total_seconds()
            self.processing_stats["total_processing_time_seconds"] += processing_time
            
            # Build comprehensive result
            enhanced_result = {
                **processed_result,
                "task": task,
                "processing_time_seconds": processing_time,
                "audio_duration_seconds": duration,
                "real_time_factor": processing_time / duration if duration > 0 else 0,
                "segments": segments if return_timestamps else [],
                "model_info": {
                    "model_name": self.asr_model.model_name,
                    "language_requested": language,
                    "chunk_length": chunk_length
                }
            }
            
            # Add optional audio analysis
            if include_analysis:
                enhanced_result["audio_analysis"] = audio_props
            
            self.processing_stats["successful_requests"] += 1
            logger.info(f"Enhanced transcription completed in {processing_time:.2f}s for {duration:.2f}s audio")
            
            return enhanced_result
            
        except Exception as e:
            self.processing_stats["failed_requests"] += 1
            logger.error(f"Enhanced transcription failed: {str(e)}")
            raise
    
    async def batch_transcribe_with_analysis(
        self,
        audio_files: List[bytes],
        language: Optional[str] = None,
        task: str = "transcribe",
        chunk_length: int = 30
    ) -> Dict[str, Any]:
        """Batch audio transcription with performance analysis.
        
        Args:
            audio_files: List of audio file bytes
            language: Target language code
            task: Task type (transcribe or translate)
            chunk_length: Chunk length for long audio
            
        Returns:
            Batch results with performance metrics
        """
        start_time = datetime.utcnow()
        results = []
        
        # Process audio files with concurrency limit
        semaphore = asyncio.Semaphore(self.settings.MAX_CONCURRENT_REQUESTS)
        
        async def process_single_audio(index: int, audio_data: bytes) -> Dict[str, Any]:
            async with semaphore:
                try:
                    result = await self.enhanced_transcription(
                        audio_data=audio_data,
                        language=language,
                        task=task,
                        chunk_length=chunk_length
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
        tasks = [process_single_audio(i, audio) for i, audio in enumerate(audio_files)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Calculate batch statistics
        end_time = datetime.utcnow()
        total_processing_time = (end_time - start_time).total_seconds()
        
        successful_results = [r for r in results if isinstance(r, dict) and r.get("status") == "success"]
        failed_results = [r for r in results if isinstance(r, dict) and r.get("status") == "failed"]
        
        total_audio_duration = sum(
            r.get("audio_duration_seconds", 0) for r in successful_results
        )
        total_words = sum(
            r.get("word_count", 0) for r in successful_results
        )
        
        return {
            "results": results,
            "batch_stats": {
                "total_files": len(audio_files),
                "successful_count": len(successful_results),
                "failed_count": len(failed_results),
                "total_processing_time_seconds": total_processing_time,
                "total_audio_duration_seconds": total_audio_duration,
                "total_words_transcribed": total_words,
                "average_processing_time": total_processing_time / len(audio_files) if audio_files else 0,
                "real_time_factor": total_processing_time / total_audio_duration if total_audio_duration > 0 else 0,
                "throughput_files_per_second": len(audio_files) / total_processing_time if total_processing_time > 0 else 0
            },
            "timestamp": end_time.isoformat()
        }
    
    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages for transcription.
        
        Returns:
            List of supported language dictionaries
        """
        # Common Whisper supported languages
        languages = [
            {"code": "en", "name": "English", "native_name": "English"},
            {"code": "es", "name": "Spanish", "native_name": "Español"},
            {"code": "fr", "name": "French", "native_name": "Français"},
            {"code": "de", "name": "German", "native_name": "Deutsch"},
            {"code": "it", "name": "Italian", "native_name": "Italiano"},
            {"code": "pt", "name": "Portuguese", "native_name": "Português"},
            {"code": "ru", "name": "Russian", "native_name": "Русский"},
            {"code": "ja", "name": "Japanese", "native_name": "日本語"},
            {"code": "ko", "name": "Korean", "native_name": "한국어"},
            {"code": "zh", "name": "Chinese", "native_name": "中文"},
            {"code": "ar", "name": "Arabic", "native_name": "العربية"},
            {"code": "hi", "name": "Hindi", "native_name": "हिन्दी"},
            {"code": "nl", "name": "Dutch", "native_name": "Nederlands"},
            {"code": "pl", "name": "Polish", "native_name": "Polski"},
            {"code": "tr", "name": "Turkish", "native_name": "Türkçe"}
        ]
        
        return languages
    
    def get_service_stats(self) -> Dict[str, Any]:
        """Get service processing statistics.
        
        Returns:
            Dictionary containing service statistics
        """
        avg_processing_time = (
            self.processing_stats["total_processing_time_seconds"] / 
            self.processing_stats["successful_requests"]
            if self.processing_stats["successful_requests"] > 0 else 0
        )
        
        avg_real_time_factor = (
            self.processing_stats["total_processing_time_seconds"] / 
            self.processing_stats["total_audio_duration_seconds"]
            if self.processing_stats["total_audio_duration_seconds"] > 0 else 0
        )
        
        return {
            "processing_stats": {
                **self.processing_stats,
                "average_processing_time_seconds": avg_processing_time,
                "average_real_time_factor": avg_real_time_factor
            },
            "model_info": self.asr_model.get_model_info(),
            "service_config": {
                "max_file_size": self.settings.MAX_FILE_SIZE,
                "max_batch_size": self.settings.MAX_BATCH_SIZE,
                "max_concurrent_requests": self.settings.MAX_CONCURRENT_REQUESTS,
                "ffmpeg_available": self.ffmpeg_available
            },
            "supported_languages_count": len(self.get_supported_languages())
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the audio service.
        
        Returns:
            Health check results
        """
        try:
            # Create a simple test audio (1 second of silence)
            sample_rate = 16000
            duration = 1.0
            samples = int(sample_rate * duration)
            audio_array = np.zeros(samples, dtype=np.float32)
            
            # Convert to bytes (WAV format)
            audio_segment = AudioSegment(
                audio_array.tobytes(),
                frame_rate=sample_rate,
                sample_width=4,  # 32-bit float
                channels=1
            )
            
            test_audio_bytes = io.BytesIO()
            audio_segment.export(test_audio_bytes, format="wav")
            test_audio_data = test_audio_bytes.getvalue()
            
            # Test transcription
            test_result = await self.asr_model.transcribe_audio(
                audio_data=test_audio_data,
                language="en",
                chunk_length=30
            )
            
            return {
                "status": "healthy",
                "test_successful": True,
                "test_audio_duration": duration,
                "test_result_length": len(str(test_result)),
                "model_loaded": True,
                "ffmpeg_available": self.ffmpeg_available,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "test_successful": False,
                "error": str(e),
                "model_loaded": False,
                "ffmpeg_available": self.ffmpeg_available,
                "timestamp": datetime.utcnow().isoformat()
            }