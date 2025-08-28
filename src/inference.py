#!/usr/bin/env python3
"""
Multimodal AI Inference Script
EnnovateX AI Platform - Samsung Challenge 2025

This script provides inference capabilities for text, image, and audio processing
using the multimodal fusion pipeline.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import torch
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from transformers import CLIPProcessor, CLIPModel, WhisperProcessor, WhisperForConditionalGeneration
    from PIL import Image
    import librosa
except ImportError as e:
    print(f"Error importing required packages: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

class MultimodalInference:
    """Multimodal AI inference engine for text, image, and audio processing."""
    
    def __init__(self):
        """Initialize the multimodal inference models."""
        print("Initializing multimodal inference models...")
        
        # Text model
        self.text_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Image model
        self.image_model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
        self.image_processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')
        
        # Audio model
        self.audio_model = WhisperForConditionalGeneration.from_pretrained('openai/whisper-small')
        self.audio_processor = WhisperProcessor.from_pretrained('openai/whisper-small')
        
        print("Models loaded successfully!")
    
    def process_text(self, text: str) -> Dict[str, Any]:
        """Process text input and return embeddings."""
        print(f"Processing text: {text[:50]}...")
        
        # Generate text embeddings
        embeddings = self.text_model.encode([text])
        
        return {
            "modality": "text",
            "input": text,
            "embeddings": embeddings[0].tolist(),
            "embedding_dim": len(embeddings[0]),
            "status": "success"
        }
    
    def process_image(self, image_path: str) -> Dict[str, Any]:
        """Process image input and return embeddings."""
        print(f"Processing image: {image_path}")
        
        try:
            # Load and process image
            image = Image.open(image_path).convert('RGB')
            inputs = self.image_processor(images=image, return_tensors="pt")
            
            # Generate image embeddings
            with torch.no_grad():
                image_features = self.image_model.get_image_features(**inputs)
                embeddings = image_features.squeeze().numpy()
            
            return {
                "modality": "image",
                "input": image_path,
                "embeddings": embeddings.tolist(),
                "embedding_dim": len(embeddings),
                "image_size": image.size,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "modality": "image",
                "input": image_path,
                "error": str(e),
                "status": "error"
            }
    
    def process_audio(self, audio_path: str) -> Dict[str, Any]:
        """Process audio input and return transcription and embeddings."""
        print(f"Processing audio: {audio_path}")
        
        try:
            # Load audio file
            audio, sr = librosa.load(audio_path, sr=16000)
            
            # Process audio for Whisper
            inputs = self.audio_processor(audio, sampling_rate=16000, return_tensors="pt")
            
            # Generate transcription
            with torch.no_grad():
                predicted_ids = self.audio_model.generate(inputs["input_features"])
                transcription = self.audio_processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            
            # Generate text embeddings from transcription
            text_embeddings = self.text_model.encode([transcription])
            
            return {
                "modality": "audio",
                "input": audio_path,
                "transcription": transcription,
                "embeddings": text_embeddings[0].tolist(),
                "embedding_dim": len(text_embeddings[0]),
                "audio_duration": len(audio) / sr,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "modality": "audio",
                "input": audio_path,
                "error": str(e),
                "status": "error"
            }
    
    def process_multimodal(self, text: Optional[str] = None, 
                          image_path: Optional[str] = None, 
                          audio_path: Optional[str] = None) -> Dict[str, Any]:
        """Process multiple modalities and fuse embeddings."""
        print("Processing multimodal input...")
        
        results = {}
        embeddings = []
        
        # Process each modality
        if text:
            text_result = self.process_text(text)
            results["text"] = text_result
            if text_result["status"] == "success":
                embeddings.append(np.array(text_result["embeddings"]))
        
        if image_path:
            image_result = self.process_image(image_path)
            results["image"] = image_result
            if image_result["status"] == "success":
                embeddings.append(np.array(image_result["embeddings"]))
        
        if audio_path:
            audio_result = self.process_audio(audio_path)
            results["audio"] = audio_result
            if audio_result["status"] == "success":
                embeddings.append(np.array(audio_result["embeddings"]))
        
        # Fuse embeddings (simple concatenation for now)
        if embeddings:
            # Normalize embeddings to same dimension if needed
            min_dim = min(emb.shape[0] for emb in embeddings)
            normalized_embeddings = [emb[:min_dim] for emb in embeddings]
            
            # Concatenate embeddings
            fused_embeddings = np.concatenate(normalized_embeddings)
            
            results["fusion"] = {
                "fused_embeddings": fused_embeddings.tolist(),
                "fusion_dim": len(fused_embeddings),
                "modalities_count": len(embeddings),
                "status": "success"
            }
        else:
            results["fusion"] = {
                "error": "No valid embeddings to fuse",
                "status": "error"
            }
        
        return results

def main():
    """Main function to handle command line arguments and run inference."""
    parser = argparse.ArgumentParser(description="Multimodal AI Inference")
    parser.add_argument("--mode", choices=["text", "image", "audio", "multimodal", "batch"], 
                       required=True, help="Inference mode")
    parser.add_argument("--input", type=str, help="Input text or file path")
    parser.add_argument("--text", type=str, help="Text input for multimodal mode")
    parser.add_argument("--image", type=str, help="Image path for multimodal mode")
    parser.add_argument("--audio", type=str, help="Audio path for multimodal mode")
    parser.add_argument("--input_dir", type=str, help="Input directory for batch mode")
    parser.add_argument("--output_dir", type=str, help="Output directory for batch mode")
    parser.add_argument("--output", type=str, help="Output file path (optional)")
    
    args = parser.parse_args()
    
    # Initialize inference engine
    inference = MultimodalInference()
    
    # Process based on mode
    if args.mode == "text":
        if not args.input:
            print("Error: --input required for text mode")
            sys.exit(1)
        result = inference.process_text(args.input)
        
    elif args.mode == "image":
        if not args.input or not os.path.exists(args.input):
            print("Error: Valid --input file path required for image mode")
            sys.exit(1)
        result = inference.process_image(args.input)
        
    elif args.mode == "audio":
        if not args.input or not os.path.exists(args.input):
            print("Error: Valid --input file path required for audio mode")
            sys.exit(1)
        result = inference.process_audio(args.input)
        
    elif args.mode == "multimodal":
        if not any([args.text, args.image, args.audio]):
            print("Error: At least one of --text, --image, or --audio required for multimodal mode")
            sys.exit(1)
        result = inference.process_multimodal(args.text, args.image, args.audio)
        
    elif args.mode == "batch":
        if not args.input_dir or not os.path.exists(args.input_dir):
            print("Error: Valid --input_dir required for batch mode")
            sys.exit(1)
        
        # Create output directory if specified
        if args.output_dir:
            os.makedirs(args.output_dir, exist_ok=True)
        
        print("Batch processing not fully implemented yet.")
        print("This would process all files in the input directory.")
        return
    
    # Print results
    print("\n" + "="*50)
    print("INFERENCE RESULTS")
    print("="*50)
    
    if args.mode == "multimodal":
        for modality, data in result.items():
            print(f"\n{modality.upper()}:")
            if data["status"] == "success":
                if "transcription" in data:
                    print(f"  Transcription: {data['transcription']}")
                if "embedding_dim" in data:
                    print(f"  Embedding dimension: {data['embedding_dim']}")
                if "fusion_dim" in data:
                    print(f"  Fusion dimension: {data['fusion_dim']}")
                    print(f"  Modalities fused: {data['modalities_count']}")
            else:
                print(f"  Error: {data.get('error', 'Unknown error')}")
    else:
        if result["status"] == "success":
            print(f"Modality: {result['modality']}")
            if "transcription" in result:
                print(f"Transcription: {result['transcription']}")
            print(f"Embedding dimension: {result['embedding_dim']}")
            print("Processing completed successfully!")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Save output if specified
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nResults saved to: {args.output}")

if __name__ == "__main__":
    main()