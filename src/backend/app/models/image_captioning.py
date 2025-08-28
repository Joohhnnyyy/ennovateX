"""Image Captioning Model

This module contains the ImageCaptioner class for BLIP-based image captioning
with optional LoRA adapter support for fine-tuned image understanding.
"""

import torch
import logging
from typing import List, Dict, Any, Optional, Union
from PIL import Image
import io
import base64
from transformers import BlipForConditionalGeneration, BlipProcessor

from ..config import settings
from .utils import get_device, clear_memory

logger = logging.getLogger(__name__)

class ImageCaptioner:
    """BLIP-based image captioner with LoRA adapter support."""
    
    def __init__(self, model_loader=None):
        self.model_loader = model_loader
        self.device = get_device()
        self.max_length = settings.MAX_CAPTION_LENGTH
        
    def _get_model_and_processor(self):
        """Get model and processor from model loader."""
        if not self.model_loader:
            raise RuntimeError("Model loader not available")
        
        model = self.model_loader.get_model("image_captioner")
        processor = self.model_loader.get_processor("image_captioner")
        
        if not model or not processor:
            raise RuntimeError("Image captioner model not loaded")
        
        return model, processor
    
    def _process_image_input(self, image_input: Union[Image.Image, bytes, str]) -> Image.Image:
        """Process various image input formats into PIL Image.
        
        Args:
            image_input: PIL Image, bytes, or base64 string
            
        Returns:
            PIL Image object
        """
        if isinstance(image_input, Image.Image):
            return image_input.convert('RGB')
        elif isinstance(image_input, bytes):
            return Image.open(io.BytesIO(image_input)).convert('RGB')
        elif isinstance(image_input, str):
            # Assume base64 encoded image
            try:
                image_data = base64.b64decode(image_input)
                return Image.open(io.BytesIO(image_data)).convert('RGB')
            except Exception as e:
                raise ValueError(f"Invalid base64 image data: {e}")
        else:
            raise ValueError(f"Unsupported image input type: {type(image_input)}")
    
    async def caption_image(
        self,
        image_input: Union[Image.Image, bytes, str],
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        num_beams: int = 5,
        length_penalty: float = 1.0,
        repetition_penalty: float = 1.2,
        do_sample: bool = False,
        temperature: float = 1.0,
        top_p: float = 0.9,
        prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate caption for input image using BLIP model.
        
        Args:
            image_input: Input image (PIL Image, bytes, or base64 string)
            max_length: Maximum length of caption
            min_length: Minimum length of caption
            num_beams: Number of beams for beam search
            length_penalty: Length penalty for beam search
            repetition_penalty: Repetition penalty
            do_sample: Whether to use sampling
            temperature: Temperature for sampling
            top_p: Top-p value for nucleus sampling
            prompt: Optional text prompt to guide captioning
            
        Returns:
            Dictionary containing caption and metadata
        """
        try:
            model, processor = self._get_model_and_processor()
            
            # Process image
            image = self._process_image_input(image_input)
            
            # Set default lengths
            if max_length is None:
                max_length = self.max_length
            if min_length is None:
                min_length = max(5, max_length // 4)
            
            # Prepare inputs
            if prompt:
                # Conditional captioning with prompt
                inputs = processor(
                    images=image,
                    text=prompt,
                    return_tensors="pt",
                    padding=True
                ).to(self.device)
            else:
                # Unconditional captioning
                inputs = processor(
                    images=image,
                    return_tensors="pt"
                ).to(self.device)
            
            # Generate caption
            with torch.no_grad():
                caption_ids = model.generate(
                    **inputs,
                    max_length=max_length,
                    min_length=min_length,
                    num_beams=num_beams,
                    length_penalty=length_penalty,
                    repetition_penalty=repetition_penalty,
                    do_sample=do_sample,
                    temperature=temperature if do_sample else 1.0,
                    top_p=top_p if do_sample else 1.0,
                    pad_token_id=processor.tokenizer.pad_token_id,
                    eos_token_id=processor.tokenizer.eos_token_id
                )
            
            # Decode caption
            caption = processor.decode(
                caption_ids[0],
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )
            
            # Remove prompt from caption if it was used
            if prompt and caption.startswith(prompt):
                caption = caption[len(prompt):].strip()
            
            # Get image metadata
            image_info = {
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
                "format": getattr(image, 'format', 'Unknown')
            }
            
            result = {
                "caption": caption,
                "confidence": 1.0,  # BLIP doesn't provide confidence scores directly
                "image_info": image_info,
                "model_used": "image_captioner",
                "prompt_used": prompt,
                "parameters": {
                    "max_length": max_length,
                    "min_length": min_length,
                    "num_beams": num_beams,
                    "length_penalty": length_penalty,
                    "do_sample": do_sample
                }
            }
            
            logger.info(f"Image captioned: {image.width}x{image.height} -> '{caption[:50]}...'")
            return result
            
        except Exception as e:
            logger.error(f"Error in image captioning: {e}")
            raise
    
    async def batch_caption(
        self,
        images: List[Union[Image.Image, bytes, str]],
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Caption multiple images in batch.
        
        Args:
            images: List of input images
            **kwargs: Additional arguments for captioning
            
        Returns:
            List of caption results
        """
        results = []
        
        for i, image in enumerate(images):
            try:
                result = await self.caption_image(image, **kwargs)
                result["batch_index"] = i
                results.append(result)
            except Exception as e:
                logger.error(f"Error captioning image {i}: {e}")
                results.append({
                    "error": str(e),
                    "batch_index": i,
                    "caption": None
                })
        
        return results
    
    async def visual_question_answering(
        self,
        image_input: Union[Image.Image, bytes, str],
        question: str,
        max_length: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Answer questions about an image using BLIP VQA capabilities.
        
        Args:
            image_input: Input image
            question: Question about the image
            max_length: Maximum length of answer
            **kwargs: Additional generation parameters
            
        Returns:
            Dictionary containing answer and metadata
        """
        try:
            # Use the question as a prompt for conditional generation
            result = await self.caption_image(
                image_input=image_input,
                prompt=question,
                max_length=max_length or 50,
                **kwargs
            )
            
            # Rename caption to answer for VQA context
            result["answer"] = result.pop("caption")
            result["question"] = question
            result["task"] = "visual_question_answering"
            
            return result
            
        except Exception as e:
            logger.error(f"Error in visual question answering: {e}")
            raise
    
    async def describe_image_details(
        self,
        image_input: Union[Image.Image, bytes, str],
        focus_areas: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate detailed description of image focusing on specific areas.
        
        Args:
            image_input: Input image
            focus_areas: List of areas to focus on (e.g., ['objects', 'colors', 'scene'])
            
        Returns:
            Dictionary containing detailed descriptions
        """
        try:
            descriptions = {}
            
            # Default focus areas
            if focus_areas is None:
                focus_areas = ['general', 'objects', 'scene', 'colors']
            
            # Generate descriptions for each focus area
            for area in focus_areas:
                if area == 'general':
                    prompt = "Describe this image:"
                elif area == 'objects':
                    prompt = "What objects are in this image?"
                elif area == 'scene':
                    prompt = "Describe the scene in this image:"
                elif area == 'colors':
                    prompt = "What are the main colors in this image?"
                elif area == 'people':
                    prompt = "Describe the people in this image:"
                elif area == 'activities':
                    prompt = "What activities are happening in this image?"
                else:
                    prompt = f"Describe the {area} in this image:"
                
                result = await self.caption_image(
                    image_input=image_input,
                    prompt=prompt,
                    max_length=100
                )
                
                descriptions[area] = result["caption"]
            
            # Get image info from the last result
            image_info = result.get("image_info", {})
            
            return {
                "detailed_descriptions": descriptions,
                "image_info": image_info,
                "focus_areas": focus_areas,
                "model_used": "image_captioner",
                "task": "detailed_description"
            }
            
        except Exception as e:
            logger.error(f"Error in detailed image description: {e}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        try:
            model, processor = self._get_model_and_processor()
            
            # Check if using LoRA adapter
            foundation_model = None
            if self.model_loader:
                foundation_model = self.model_loader.get_foundation_model("image_captioner")
            
            return {
                "model_type": "image_captioner",
                "base_model": settings.IMAGE_CAPTION_MODEL,
                "lora_adapter": settings.IMAGE_CAPTION_LORA,
                "using_lora": foundation_model is not None,
                "device": self.device,
                "max_caption_length": self.max_length,
                "supported_formats": ["JPEG", "PNG", "WebP", "BMP"],
                "capabilities": [
                    "image_captioning",
                    "visual_question_answering",
                    "detailed_description"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {"error": str(e)}