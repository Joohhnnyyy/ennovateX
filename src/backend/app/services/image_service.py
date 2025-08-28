"""Image processing service for the EnnovateX AI platform.

Provides business logic and postprocessing for image captioning and analysis.
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import asyncio
from PIL import Image, ImageEnhance, ImageFilter
import io
from ..models.image_captioning import ImageCaptioner
from ..config import Settings

logger = logging.getLogger(__name__)


class ImageService:
    """Service class for image processing operations."""
    
    def __init__(self, captioner: ImageCaptioner, settings: Settings):
        self.captioner = captioner
        self.settings = settings
        self.processing_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_images_processed": 0
        }
    
    def preprocess_image(self, image: Image.Image, enhance: bool = True) -> Image.Image:
        """Preprocess image before captioning.
        
        Args:
            image: PIL Image object
            enhance: Whether to apply image enhancements
            
        Returns:
            Preprocessed PIL Image
        """
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large
        max_size = (1024, 1024)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        if enhance:
            # Enhance contrast slightly
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.1)
            
            # Enhance sharpness slightly
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.1)
        
        return image
    
    def postprocess_caption(self, caption: str, image_size: tuple) -> str:
        """Postprocess generated caption.
        
        Args:
            caption: Generated caption
            image_size: Original image dimensions (width, height)
            
        Returns:
            Cleaned and improved caption
        """
        # Remove common artifacts
        caption = caption.strip()
        
        # Remove redundant phrases
        redundant_phrases = [
            "a picture of", "an image of", "a photo of", "this image shows",
            "the image contains", "in this image", "the picture shows"
        ]
        
        caption_lower = caption.lower()
        for phrase in redundant_phrases:
            if caption_lower.startswith(phrase):
                caption = caption[len(phrase):].strip()
                break
        
        # Ensure proper capitalization
        if caption and not caption[0].isupper():
            caption = caption[0].upper() + caption[1:]
        
        # Ensure proper ending
        if caption and not caption.endswith(('.', '!', '?')):
            caption += '.'
        
        return caption
    
    def analyze_image_properties(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze image properties for metadata.
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary containing image analysis
        """
        width, height = image.size
        aspect_ratio = width / height
        
        # Calculate image complexity (simplified)
        grayscale = image.convert('L')
        edges = grayscale.filter(ImageFilter.FIND_EDGES)
        edge_pixels = sum(1 for pixel in edges.getdata() if pixel > 50)
        complexity = edge_pixels / (width * height)
        
        # Determine orientation
        if aspect_ratio > 1.3:
            orientation = "landscape"
        elif aspect_ratio < 0.7:
            orientation = "portrait"
        else:
            orientation = "square"
        
        # Estimate dominant colors (simplified)
        colors = image.getcolors(maxcolors=256*256*256)
        if colors:
            dominant_color = max(colors, key=lambda x: x[0])[1]
        else:
            dominant_color = (128, 128, 128)  # Default gray
        
        return {
            "width": width,
            "height": height,
            "aspect_ratio": round(aspect_ratio, 2),
            "orientation": orientation,
            "complexity_score": round(complexity, 3),
            "dominant_color_rgb": dominant_color,
            "file_size_estimate": width * height * 3  # RGB estimate
        }
    
    async def enhanced_caption(
        self,
        image: Union[Image.Image, bytes],
        max_length: int = 50,
        min_length: int = 10,
        detail_level: str = "medium",
        include_analysis: bool = False,
        use_lora: bool = False,
        lora_adapter: Optional[str] = None
    ) -> Dict[str, Any]:
        """Enhanced image captioning with additional analysis.
        
        Args:
            image: PIL Image or image bytes
            max_length: Maximum caption length
            min_length: Minimum caption length
            detail_level: Level of detail (basic, medium, detailed)
            include_analysis: Whether to include image analysis
            use_lora: Whether to use LoRA adapter
            lora_adapter: Specific LoRA adapter name
            
        Returns:
            Enhanced caption with additional metadata
        """
        try:
            self.processing_stats["total_requests"] += 1
            self.processing_stats["total_images_processed"] += 1
            
            # Convert bytes to PIL Image if necessary
            if isinstance(image, bytes):
                image = Image.open(io.BytesIO(image))
            
            # Store original size
            original_size = image.size
            
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Generate caption based on detail level
            if detail_level == "detailed":
                caption = await self.captioner.detailed_description(
                    image=processed_image,
                    detail_level=detail_level,
                    use_lora=use_lora,
                    lora_adapter=lora_adapter
                )
            else:
                caption = await self.captioner.caption_image(
                    image=processed_image,
                    max_length=max_length,
                    min_length=min_length,
                    use_lora=use_lora,
                    lora_adapter=lora_adapter
                )
            
            # Postprocess caption
            final_caption = self.postprocess_caption(caption, original_size)
            
            # Prepare result
            result = {
                "caption": final_caption,
                "original_caption": caption,
                "detail_level": detail_level,
                "image_width": original_size[0],
                "image_height": original_size[1],
                "processed_size": processed_image.size,
                "caption_length": len(final_caption),
                "confidence": 0.85,  # Placeholder confidence
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Add optional analysis
            if include_analysis:
                result["image_analysis"] = self.analyze_image_properties(image)
            
            self.processing_stats["successful_requests"] += 1
            logger.info(f"Enhanced captioning completed successfully")
            
            return result
            
        except Exception as e:
            self.processing_stats["failed_requests"] += 1
            logger.error(f"Enhanced captioning failed: {str(e)}")
            raise
    
    async def batch_caption_with_analysis(
        self,
        images: List[Union[Image.Image, bytes]],
        max_length: int = 50,
        min_length: int = 10,
        use_lora: bool = False,
        lora_adapter: Optional[str] = None
    ) -> Dict[str, Any]:
        """Batch image captioning with performance analysis.
        
        Args:
            images: List of PIL Images or image bytes
            max_length: Maximum caption length
            min_length: Minimum caption length
            use_lora: Whether to use LoRA adapter
            lora_adapter: Specific LoRA adapter name
            
        Returns:
            Batch results with performance metrics
        """
        start_time = datetime.utcnow()
        results = []
        
        # Process images concurrently (with limit)
        semaphore = asyncio.Semaphore(self.settings.MAX_CONCURRENT_REQUESTS)
        
        async def process_single_image(index: int, image: Union[Image.Image, bytes]) -> Dict[str, Any]:
            async with semaphore:
                try:
                    result = await self.enhanced_caption(
                        image=image,
                        max_length=max_length,
                        min_length=min_length,
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
        tasks = [process_single_image(i, img) for i, img in enumerate(images)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Calculate batch statistics
        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()
        
        successful_results = [r for r in results if isinstance(r, dict) and r.get("status") == "success"]
        failed_results = [r for r in results if isinstance(r, dict) and r.get("status") == "failed"]
        
        total_pixels = 0
        for result in successful_results:
            if "image_width" in result and "image_height" in result:
                total_pixels += result["image_width"] * result["image_height"]
        
        return {
            "results": results,
            "batch_stats": {
                "total_images": len(images),
                "successful_count": len(successful_results),
                "failed_count": len(failed_results),
                "processing_time_seconds": processing_time,
                "total_pixels_processed": total_pixels,
                "average_processing_time": processing_time / len(images) if images else 0,
                "throughput_images_per_second": len(images) / processing_time if processing_time > 0 else 0
            },
            "timestamp": end_time.isoformat()
        }
    
    def get_service_stats(self) -> Dict[str, Any]:
        """Get service processing statistics.
        
        Returns:
            Dictionary containing service statistics
        """
        return {
            "processing_stats": self.processing_stats.copy(),
            "model_info": self.captioner.get_model_info(),
            "service_config": {
                "max_file_size": self.settings.MAX_FILE_SIZE,
                "max_batch_size": self.settings.MAX_BATCH_SIZE,
                "max_concurrent_requests": self.settings.MAX_CONCURRENT_REQUESTS
            }
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the image service.
        
        Returns:
            Health check results
        """
        try:
            # Create a simple test image
            test_image = Image.new('RGB', (100, 100), color='red')
            
            # Test captioning
            test_result = await self.captioner.caption_image(
                image=test_image,
                max_length=20,
                min_length=5
            )
            
            return {
                "status": "healthy",
                "test_successful": True,
                "test_caption_length": len(test_result),
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