"""Audio Automatic Speech Recognition Model

This module contains the AudioASR class for Whisper-based speech-to-text conversion
with support for multiple languages and audio formats.
"""

import torch
import logging
from typing import List, Dict, Any, Optional, Union
import librosa
import numpy as np
import io
import base64
from transformers import WhisperForConditionalGeneration, WhisperProcessor

from ..config import settings
from .utils import get_device, clear_memory

logger = logging.getLogger(__name__)

class AudioASR:
    """Whisper-based automatic speech recognition."""
    
    def __init__(self, model_loader=None):
        self.model_loader = model_loader
        self.device = get_device()
        self.sample_rate = 16000  # Whisper expects 16kHz audio
        
    def _get_model_and_processor(self):
        """Get model and processor from model loader."""
        if not self.model_loader:
            raise RuntimeError("Model loader not available")
        
        model = self.model_loader.get_model("audio_asr")
        processor = self.model_loader.get_processor("audio_asr")
        
        if not model or not processor:
            raise RuntimeError("Audio ASR model not loaded")
        
        return model, processor
    
    def _process_audio_input(self, audio_input: Union[bytes, str, np.ndarray]) -> np.ndarray:
        """Process various audio input formats into numpy array.
        
        Args:
            audio_input: Audio bytes, base64 string, or numpy array
            
        Returns:
            Numpy array of audio samples
        """
        if isinstance(audio_input, np.ndarray):
            audio = audio_input
        elif isinstance(audio_input, bytes):
            # Load audio from bytes
            audio, sr = librosa.load(io.BytesIO(audio_input), sr=self.sample_rate)
        elif isinstance(audio_input, str):
            # Assume base64 encoded audio
            try:
                audio_data = base64.b64decode(audio_input)
                audio, sr = librosa.load(io.BytesIO(audio_data), sr=self.sample_rate)
            except Exception as e:
                raise ValueError(f"Invalid base64 audio data: {e}")
        else:
            raise ValueError(f"Unsupported audio input type: {type(audio_input)}")
        
        # Ensure correct sample rate
        if hasattr(audio, 'shape') and len(audio.shape) > 1:
            # Convert stereo to mono if needed
            audio = librosa.to_mono(audio)
        
        return audio.astype(np.float32)
    
    async def transcribe(
        self,
        audio_input: Union[bytes, str, np.ndarray],
        language: Optional[str] = None,
        task: str = "transcribe",
        return_timestamps: bool = False,
        chunk_length_s: Optional[float] = None,
        stride_length_s: Optional[float] = None
    ) -> Dict[str, Any]:
        """Transcribe audio to text using Whisper model.
        
        Args:
            audio_input: Input audio (bytes, base64 string, or numpy array)
            language: Language code (e.g., 'en', 'es', 'fr') or None for auto-detection
            task: 'transcribe' or 'translate' (translate to English)
            return_timestamps: Whether to return word-level timestamps
            chunk_length_s: Length of audio chunks in seconds for long audio
            stride_length_s: Stride length for overlapping chunks
            
        Returns:
            Dictionary containing transcription and metadata
        """
        try:
            model, processor = self._get_model_and_processor()
            
            # Process audio
            audio = self._process_audio_input(audio_input)
            
            # Handle long audio by chunking if specified
            if chunk_length_s and len(audio) > chunk_length_s * self.sample_rate:
                return await self._transcribe_long_audio(
                    audio, language, task, return_timestamps, chunk_length_s, stride_length_s
                )
            
            # Prepare inputs
            inputs = processor(
                audio,
                sampling_rate=self.sample_rate,
                return_tensors="pt"
            ).to(self.device)
            
            # Set generation parameters
            generate_kwargs = {
                "task": task,
                "return_timestamps": return_timestamps
            }
            
            if language:
                generate_kwargs["language"] = language
            
            # Generate transcription
            with torch.no_grad():
                predicted_ids = model.generate(
                    inputs["input_features"],
                    **generate_kwargs
                )
            
            # Decode transcription
            transcription = processor.batch_decode(
                predicted_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )[0]
            
            # Calculate audio metadata
            duration = len(audio) / self.sample_rate
            
            # Detect language if not specified
            detected_language = language
            if not language:
                # Use Whisper's language detection
                try:
                    with torch.no_grad():
                        # Get language probabilities from the model
                        logits = model.detect_language(inputs["input_features"])
                        detected_language_id = torch.argmax(logits, dim=-1).item()
                        detected_language = processor.tokenizer.convert_ids_to_tokens([detected_language_id])[0]
                        detected_language = detected_language.replace('<|', '').replace('|>', '')
                except:
                    detected_language = "unknown"
            
            result = {
                "transcription": transcription,
                "language": detected_language,
                "task": task,
                "duration": round(duration, 2),
                "sample_rate": self.sample_rate,
                "audio_length": len(audio),
                "model_used": "audio_asr",
                "confidence": 1.0,  # Whisper doesn't provide confidence scores directly
                "parameters": {
                    "language": language,
                    "task": task,
                    "return_timestamps": return_timestamps
                }
            }
            
            # Add timestamps if requested
            if return_timestamps:
                # Note: This is a simplified implementation
                # For full timestamp support, you'd need to use the Whisper timestamp features
                words = transcription.split()
                word_duration = duration / len(words) if words else 0
                timestamps = [
                    {
                        "word": word,
                        "start": round(i * word_duration, 2),
                        "end": round((i + 1) * word_duration, 2)
                    }
                    for i, word in enumerate(words)
                ]
                result["timestamps"] = timestamps
            
            logger.info(f"Audio transcribed: {duration:.2f}s -> '{transcription[:50]}...'")
            return result
            
        except Exception as e:
            logger.error(f"Error in audio transcription: {e}")
            raise
    
    async def _transcribe_long_audio(
        self,
        audio: np.ndarray,
        language: Optional[str],
        task: str,
        return_timestamps: bool,
        chunk_length_s: float,
        stride_length_s: Optional[float]
    ) -> Dict[str, Any]:
        """Transcribe long audio by processing in chunks."""
        chunk_length = int(chunk_length_s * self.sample_rate)
        stride_length = int((stride_length_s or chunk_length_s / 4) * self.sample_rate)
        
        chunks = []
        transcriptions = []
        
        # Split audio into chunks
        for start in range(0, len(audio), chunk_length - stride_length):
            end = min(start + chunk_length, len(audio))
            chunk = audio[start:end]
            chunks.append((start / self.sample_rate, end / self.sample_rate, chunk))
        
        # Transcribe each chunk
        for start_time, end_time, chunk in chunks:
            try:
                result = await self.transcribe(
                    chunk,
                    language=language,
                    task=task,
                    return_timestamps=return_timestamps
                )
                
                chunk_transcription = {
                    "text": result["transcription"],
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration": end_time - start_time
                }
                
                if return_timestamps and "timestamps" in result:
                    # Adjust timestamps to global time
                    adjusted_timestamps = [
                        {
                            "word": ts["word"],
                            "start": ts["start"] + start_time,
                            "end": ts["end"] + start_time
                        }
                        for ts in result["timestamps"]
                    ]
                    chunk_transcription["timestamps"] = adjusted_timestamps
                
                transcriptions.append(chunk_transcription)
                
            except Exception as e:
                logger.error(f"Error transcribing chunk {start_time}-{end_time}: {e}")
                continue
        
        # Combine transcriptions
        full_transcription = " ".join([t["text"] for t in transcriptions])
        total_duration = len(audio) / self.sample_rate
        
        result = {
            "transcription": full_transcription,
            "language": language or "auto",
            "task": task,
            "duration": round(total_duration, 2),
            "sample_rate": self.sample_rate,
            "audio_length": len(audio),
            "model_used": "audio_asr",
            "chunked": True,
            "chunk_count": len(transcriptions),
            "chunk_transcriptions": transcriptions,
            "parameters": {
                "language": language,
                "task": task,
                "chunk_length_s": chunk_length_s,
                "stride_length_s": stride_length_s
            }
        }
        
        # Combine timestamps if requested
        if return_timestamps:
            all_timestamps = []
            for chunk_trans in transcriptions:
                if "timestamps" in chunk_trans:
                    all_timestamps.extend(chunk_trans["timestamps"])
            result["timestamps"] = all_timestamps
        
        return result
    
    async def batch_transcribe(
        self,
        audio_inputs: List[Union[bytes, str, np.ndarray]],
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Transcribe multiple audio files in batch.
        
        Args:
            audio_inputs: List of input audio files
            **kwargs: Additional arguments for transcription
            
        Returns:
            List of transcription results
        """
        results = []
        
        for i, audio in enumerate(audio_inputs):
            try:
                result = await self.transcribe(audio, **kwargs)
                result["batch_index"] = i
                results.append(result)
            except Exception as e:
                logger.error(f"Error transcribing audio {i}: {e}")
                results.append({
                    "error": str(e),
                    "batch_index": i,
                    "transcription": None
                })
        
        return results
    
    async def detect_language(
        self,
        audio_input: Union[bytes, str, np.ndarray]
    ) -> Dict[str, Any]:
        """Detect the language of the input audio.
        
        Args:
            audio_input: Input audio
            
        Returns:
            Dictionary containing detected language and confidence
        """
        try:
            model, processor = self._get_model_and_processor()
            
            # Process audio
            audio = self._process_audio_input(audio_input)
            
            # Take only first 30 seconds for language detection
            max_samples = 30 * self.sample_rate
            if len(audio) > max_samples:
                audio = audio[:max_samples]
            
            # Prepare inputs
            inputs = processor(
                audio,
                sampling_rate=self.sample_rate,
                return_tensors="pt"
            ).to(self.device)
            
            # Detect language
            with torch.no_grad():
                logits = model.detect_language(inputs["input_features"])
                language_probs = torch.softmax(logits, dim=-1)
                
                # Get top 5 languages
                top_probs, top_indices = torch.topk(language_probs, 5)
                
                languages = []
                for prob, idx in zip(top_probs[0], top_indices[0]):
                    lang_token = processor.tokenizer.convert_ids_to_tokens([idx.item()])[0]
                    lang_code = lang_token.replace('<|', '').replace('|>', '')
                    languages.append({
                        "language": lang_code,
                        "confidence": round(prob.item(), 4)
                    })
            
            return {
                "detected_languages": languages,
                "primary_language": languages[0]["language"],
                "confidence": languages[0]["confidence"],
                "duration": len(audio) / self.sample_rate,
                "model_used": "audio_asr"
            }
            
        except Exception as e:
            logger.error(f"Error in language detection: {e}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        try:
            model, processor = self._get_model_and_processor()
            
            return {
                "model_type": "audio_asr",
                "base_model": settings.AUDIO_ASR_MODEL,
                "device": self.device,
                "sample_rate": self.sample_rate,
                "supported_formats": ["WAV", "MP3", "FLAC", "OGG"],
                "supported_tasks": ["transcribe", "translate"],
                "capabilities": [
                    "speech_to_text",
                    "language_detection",
                    "translation_to_english",
                    "timestamp_generation",
                    "long_audio_processing"
                ],
                "max_audio_length": "unlimited (chunked processing)",
                "languages_supported": "99+ languages"
            }
            
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {"error": str(e)}