# Usage Guide

## Running Inference

### Web Interface

The easiest way to test the system is through the web interface:

1. **Access the Dashboard**: Navigate to http://localhost:3000
2. **Select Input Type**: Choose text, image, or audio input
3. **Upload/Enter Data**: Provide your input data
4. **Run Analysis**: Click the analyze button to process
5. **View Results**: Review the generated embeddings and analysis

### API Usage

#### Text Processing

```bash
curl -X POST "http://localhost:8001/api/text/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text content here"}'
```

```python
import requests

response = requests.post(
    "http://localhost:8001/api/text/analyze",
    json={"text": "Your text content here"}
)
result = response.json()
print(result["embedding"])
```

#### Image Processing

```bash
curl -X POST "http://localhost:8001/api/image/analyze" \
  -F "file=@path/to/your/image.jpg"
```

```python
import requests

with open("path/to/your/image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8001/api/image/analyze",
        files={"file": f}
    )
result = response.json()
print(result["embedding"])
```

#### Audio Processing

```bash
curl -X POST "http://localhost:8001/api/audio/analyze" \
  -F "file=@path/to/your/audio.wav"
```

```python
import requests

with open("path/to/your/audio.wav", "rb") as f:
    response = requests.post(
        "http://localhost:8001/api/audio/analyze",
        files={"file": f}
    )
result = response.json()
print(result["transcription"])
print(result["embedding"])
```

#### Multimodal Fusion

```python
import requests

# Process multiple modalities
text_response = requests.post(
    "http://localhost:8001/api/text/analyze",
    json={"text": "A beautiful sunset over the ocean"}
)

with open("sunset.jpg", "rb") as f:
    image_response = requests.post(
        "http://localhost:8001/api/image/analyze",
        files={"file": f}
    )

# Combine embeddings
fusion_response = requests.post(
    "http://localhost:8001/api/fusion/combine",
    json={
        "embeddings": {
            "text": text_response.json()["embedding"],
            "image": image_response.json()["embedding"]
        },
        "strategy": "concatenate"  # or "weighted_average", "attention"
    }
)

fused_embedding = fusion_response.json()["fused_embedding"]
```

### Command Line Interface

#### Direct Script Usage

```bash
# Text inference
cd src
python inference.py --mode text --input "Your text here"

# Image inference
python inference.py --mode image --input path/to/image.jpg

# Audio inference
python inference.py --mode audio --input path/to/audio.wav

# Multimodal inference
python inference.py --mode multimodal --text "Description" --image path/to/image.jpg
```

#### Batch Processing

```bash
# Process multiple files
python inference.py --mode batch --input_dir data/inputs/ --output_dir data/outputs/
```

## Extending the Project

### Adding New Models

#### 1. Create Model Wrapper

Create a new file in `src/models/`:

```python
# src/models/new_model.py
from typing import Any, List
import torch
from transformers import AutoModel, AutoTokenizer

class NewModelWrapper:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = AutoModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
    def encode(self, inputs: List[str]) -> torch.Tensor:
        """Encode inputs to embeddings"""
        encoded = self.tokenizer(inputs, return_tensors="pt", padding=True)
        with torch.no_grad():
            outputs = self.model(**encoded)
        return outputs.last_hidden_state.mean(dim=1)
        
    def preprocess(self, raw_input: Any) -> List[str]:
        """Preprocess raw input for the model"""
        # Implement preprocessing logic
        pass
```

#### 2. Register Model

Add to `src/models/__init__.py`:

```python
from .new_model import NewModelWrapper

MODEL_REGISTRY = {
    "text": TextModelWrapper,
    "image": ImageModelWrapper,
    "audio": AudioModelWrapper,
    "new_model": NewModelWrapper,  # Add your model
}
```

#### 3. Update API Endpoints

Add new endpoint in `src/backend/app/routers/`:

```python
# src/backend/app/routers/new_model.py
from fastapi import APIRouter, UploadFile
from ..models import MODEL_REGISTRY

router = APIRouter(prefix="/new_model", tags=["new_model"])
model = MODEL_REGISTRY["new_model"]()

@router.post("/analyze")
async def analyze_new_model(data: dict):
    embedding = model.encode([data["input"]])
    return {"embedding": embedding.tolist()}
```

### Adding New Fusion Strategies

#### 1. Implement Fusion Function

```python
# src/fusion/custom_fusion.py
import torch
from typing import Dict, List

def custom_fusion_strategy(
    embeddings: Dict[str, torch.Tensor],
    weights: Dict[str, float] = None
) -> torch.Tensor:
    """Custom fusion strategy implementation"""
    # Implement your fusion logic
    if weights is None:
        weights = {k: 1.0 for k in embeddings.keys()}
    
    weighted_embeddings = []
    for modality, embedding in embeddings.items():
        weighted_embeddings.append(embedding * weights[modality])
    
    return torch.stack(weighted_embeddings).mean(dim=0)
```

#### 2. Register Fusion Strategy

```python
# src/fusion/__init__.py
from .custom_fusion import custom_fusion_strategy

FUSION_STRATEGIES = {
    "concatenate": concatenate_fusion,
    "weighted_average": weighted_average_fusion,
    "attention": attention_fusion,
    "custom": custom_fusion_strategy,  # Add your strategy
}
```

### Adding New Preprocessing

#### 1. Create Preprocessor

```python
# src/utils/custom_preprocessor.py
from typing import Any

class CustomPreprocessor:
    def __init__(self, config: dict):
        self.config = config
        
    def preprocess(self, data: Any) -> Any:
        """Custom preprocessing logic"""
        # Implement preprocessing steps
        processed_data = data  # Your processing here
        return processed_data
        
    def postprocess(self, results: Any) -> Any:
        """Custom postprocessing logic"""
        # Implement postprocessing steps
        return results
```

#### 2. Integrate Preprocessor

```python
# In your model wrapper or API endpoint
from ..utils.custom_preprocessor import CustomPreprocessor

preprocessor = CustomPreprocessor(config)
processed_input = preprocessor.preprocess(raw_input)
results = model.process(processed_input)
final_results = preprocessor.postprocess(results)
```

### Custom Training Scripts

#### 1. Create Training Configuration

```python
# configs/custom_training.yaml
model:
  name: "custom_model"
  parameters:
    learning_rate: 0.001
    batch_size: 32
    epochs: 10

data:
  train_path: "data/train"
  val_path: "data/val"
  test_path: "data/test"

training:
  optimizer: "adam"
  scheduler: "cosine"
  early_stopping: true
```

#### 2. Implement Training Loop

```python
# src/train_custom.py
import yaml
from src.models import MODEL_REGISTRY
from src.utils.training import TrainingManager

def main():
    # Load configuration
    with open("configs/custom_training.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    # Initialize model and training
    model = MODEL_REGISTRY[config["model"]["name"]]()
    trainer = TrainingManager(model, config)
    
    # Run training
    trainer.train()
    
    # Save model
    trainer.save_model("models/custom_trained_model")

if __name__ == "__main__":
    main()
```

### Frontend Extensions

#### 1. Add New Component

```tsx
// src/components/CustomAnalyzer.tsx
import React, { useState } from 'react';

interface CustomAnalyzerProps {
  onAnalyze: (data: any) => void;
}

export const CustomAnalyzer: React.FC<CustomAnalyzerProps> = ({ onAnalyze }) => {
  const [input, setInput] = useState('');
  
  const handleSubmit = () => {
    onAnalyze({ input, type: 'custom' });
  };
  
  return (
    <div className="custom-analyzer">
      <input 
        value={input} 
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter custom input"
      />
      <button onClick={handleSubmit}>Analyze</button>
    </div>
  );
};
```

#### 2. Integrate Component

```tsx
// src/app/dashboard/page.tsx
import { CustomAnalyzer } from '@/components/CustomAnalyzer';

export default function Dashboard() {
  const handleCustomAnalysis = async (data: any) => {
    const response = await fetch('/api/custom/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await response.json();
    // Handle results
  };
  
  return (
    <div>
      {/* Other components */}
      <CustomAnalyzer onAnalyze={handleCustomAnalysis} />
    </div>
  );
}
```

## Performance Optimization

### Model Optimization

```python
# Enable model optimization
model.half()  # Use FP16 for faster inference
model.eval()  # Set to evaluation mode

# Use torch.jit for compilation
compiled_model = torch.jit.script(model)
```

### Batch Processing

```python
# Process multiple inputs in batches
def batch_process(inputs: List[str], batch_size: int = 32):
    results = []
    for i in range(0, len(inputs), batch_size):
        batch = inputs[i:i + batch_size]
        batch_results = model.encode(batch)
        results.extend(batch_results)
    return results
```

### Caching

```python
# Implement result caching
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_inference(input_hash: str):
    return model.encode(input_text)
```