# Installation Guide

## System Requirements

### Hardware Requirements

**Minimum Requirements:**
- CPU: 4 cores, 2.5 GHz
- RAM: 8 GB
- Storage: 10 GB free space
- Network: Stable internet connection for model downloads

**Recommended Requirements:**
- CPU: 8+ cores, 3.0+ GHz
- RAM: 16+ GB
- GPU: NVIDIA GPU with 8+ GB VRAM (for accelerated inference)
- Storage: 20+ GB free space (SSD recommended)
- Network: High-speed internet for faster model downloads

### Software Requirements

- **Operating System**: Linux (Ubuntu 20.04+), macOS (10.15+), or Windows 10+
- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **npm**: 8.0 or higher
- **Git**: Latest version
- **Docker**: Optional, for containerized deployment

## Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ennovatex-ai-platform-redesign
```

### 2. Backend Setup

#### Create Python Virtual Environment

```bash
# Navigate to backend directory
cd src/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# For GPU support (optional)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### Environment Variables

Create a `.env` file in the `src/backend` directory:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8001
API_RELOAD=true

# Model Configuration
MODEL_CACHE_DIR=./models
MAX_UPLOAD_SIZE=50MB

# Performance Settings
BATCH_SIZE=32
MAX_WORKERS=4

# GPU Settings (if available)
CUDA_VISIBLE_DEVICES=0
```

### 3. Frontend Setup

#### Navigate to Frontend Directory

```bash
cd src
```

#### Install Node.js Dependencies

```bash
# Install packages
npm install

# Or using yarn
yarn install
```

#### Environment Configuration

Create a `.env.local` file in the `src` directory:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_APP_NAME=Ennovatex AI Platform

# Development Settings
NEXT_PUBLIC_DEV_MODE=true
```

## Model Downloads

The system will automatically download required models on first run. However, you can pre-download them:

### Text Model
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

### Image Model
```bash
python -c "from transformers import CLIPModel; CLIPModel.from_pretrained('openai/clip-vit-base-patch32')"
```

### Audio Model
```bash
python -c "from transformers import WhisperForConditionalGeneration; WhisperForConditionalGeneration.from_pretrained('openai/whisper-small')"
```

## Running the Application

### Development Mode

#### Start Backend Server

```bash
# From src/backend directory
cd src/backend
source venv/bin/activate  # Activate virtual environment
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

#### Start Frontend Server

```bash
# From src directory
cd src
npm run dev
```

#### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

### Production Deployment

#### Using Docker

```bash
# Build and run with Docker Compose
docker-compose -f src/backend/docker-compose.prod.yml up -d
```

#### Manual Production Setup

```bash
# Backend
cd src/backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001

# Frontend
cd src
npm run build
npm start
```

## Verification

### Test Backend API

```bash
curl -X GET "http://localhost:8001/health"
```

### Test Frontend

Open http://localhost:3000 in your browser and verify the interface loads correctly.

### Run Test Suite

```bash
# Backend tests
cd src/backend
pytest tests/

# Frontend tests
cd src
npm test
```

## Troubleshooting

### Common Issues

1. **Model Download Failures**
   - Check internet connection
   - Verify disk space
   - Try manual model downloads

2. **GPU Not Detected**
   - Install CUDA drivers
   - Verify PyTorch GPU installation
   - Check CUDA_VISIBLE_DEVICES environment variable

3. **Port Conflicts**
   - Change ports in configuration files
   - Kill existing processes using the ports

4. **Memory Issues**
   - Reduce batch size in configuration
   - Close other applications
   - Consider using CPU-only mode

### Getting Help

- Check the logs in `src/backend/logs/`
- Review the API documentation at http://localhost:8001/docs
- Ensure all dependencies are correctly installed
- Verify environment variables are properly set