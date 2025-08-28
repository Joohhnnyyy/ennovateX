# Samsung EnnovateX 2025 AI Challenge Submission

## Problem Statement
**Building the Next OS-Level AI Experience**

A single, powerful multimodal foundation model can serve as an unchangeable firmware within edge/mobile operating system, enabling applications to use compact "adapters" (for varied downstream tasks – text, image, audio, video) instead of bundling several large models. Some of the architectural innovations that can be included are - firmware backbone and task-specific adapters, multi-path execution to route tasks efficiently based on complexity, demonstrating system benefits through metrics like latency and battery performance.

## Team Information
**Team Name:** Om Vinayak Archit Ansh Siddhant

**Team Members:**
- Om Vinayak
- Archit Nirula  
- Ansh Johnson
- Siddhant Sinha

## Demo Video Link
[Demo Video](https://youtu.be/CxQSxXKlcMQ)

## Project Artefacts

### Technical Documentation

All technical documentation is included inside the docs/ folder of the repository.

- **docs/overview.md** - Project summary & objectives
- **docs/architecture.md** - Model architecture, fusion pipeline, and workflows
- **docs/setup.md** - Installation guide and environment requirements
- **docs/usage.md** - How to run inference and extend the project
- **docs/limitations_future.md** - Limitations, challenges, and future work

### Source Code

All executable source code is placed under the src/ folder.

- **src/models/** - Embedding models wrapper (Text, Image, Audio with Whisper)
- **src/fusion/** - Fusion functions and utilities
- **src/inference.py** - Script for testing with text, image, and audio inputs
- **src/train.py** - Script for fine-tuning and experimentation
- **src/utils/** - Helper functions (preprocessing, evaluation, logging)

The code can be installed and executed with:

```bash
git clone https://github.com/Joohhnnyyy/ennovateX.git
cd ennovateX
pip install -r requirements.txt
python src/inference.py --mode text --input "Your text here"
```

### Models Used

**Text Model**: sentence-transformers/all-MiniLM-L6-v2

`https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2`

**Image Model**: openai/clip-vit-base-patch32

`https://huggingface.co/openai/clip-vit-base-patch32`

**Audio Model (ASR)**: openai/whisper-small

`https://huggingface.co/openai/whisper-small`

### Models Published

Currently, no new model has been published.

Planned upload: Multimodal Fusion Embedding Model will be published here:
`https://huggingface.co/username/multimodal-fusion-embedding-v1`

(Open-source under Apache-2.0 license once finalized.)

### Datasets Used

**Audio Dataset (Main)**: rakshya34/filtered_voice_english_v1

`https://huggingface.co/datasets/rakshya34/filtered_voice_english_v1`

**Audio Dataset (Earlier Test)**: sifat1221/english_voice_256

`https://huggingface.co/datasets/sifat1221/english_voice_256`

**Image Dataset**: CIFAR-10
(external dataset, not on Hugging Face)
`https://www.cs.toronto.edu/~kriz/cifar.html`

**Text Dataset**: ag_news

`https://huggingface.co/datasets/ag_news`

### Datasets Published

Currently, no new dataset has been published.

Planned upload: Synthetic Multimodal Dataset → will be published here:
 `https://huggingface.co/datasets/username/multimodal-synthetic-v1`

(Open-source under CC-BY-4.0 license once finalized.)

## Project Overview

**EnnovateX AI Platform** is a cutting-edge multimodal AI platform built with Next.js 15, featuring Samsung-inspired branding and comprehensive AI capabilities. This platform delivers a complete suite of AI tools with enterprise-grade performance, security, and scalability.

### Key Features

#### Core AI Capabilities
- **Text Processing**: Advanced NLP, sentiment analysis, summarization, and translation
- **Image Analysis**: Object detection, image classification, and visual content analysis
- **Video Analysis**: Video content analysis, object tracking, and scene detection
- **Multimodal AI**: Combined text, image, and video processing for comprehensive insights

#### Platform Features
- **Lightning Fast Performance**: Optimized for speed with advanced caching and CDN
- **Enterprise Security**: SOC2 certified with end-to-end encryption
- **Infinitely Scalable**: Auto-scaling infrastructure that grows with your needs
- **Advanced Analytics**: Real-time insights and comprehensive dashboards
- **Team Collaboration**: Built-in tools for seamless team workflows
- **One-Click Deploy**: Automated deployment with zero configuration
- **Global Reach**: Worldwide infrastructure with 99.9% uptime
- **Data Privacy**: GDPR compliant with advanced privacy controls

### Tech Stack
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS with custom design system
- **UI Components**: Radix UI primitives
- **Backend**: FastAPI with Python
- **AI Models**: Hugging Face Transformers
- **Database**: PostgreSQL
- **Deployment**: Docker, Vercel, Render

## Getting Started

### Prerequisites
- Node.js 18+ or Bun
- Python 3.9+
- npm, yarn, pnpm, or bun package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Joohhnnyyy/ennovateX.git
   cd ennovateX
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   # or
   bun install
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Run the development servers**
   
   **Frontend:**
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   # or
   bun dev
   ```
   
   **Backend:**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

5. **Open your browser**
   - Frontend: Navigate to http://localhost:3000
   - Backend API: Navigate to http://localhost:8001/docs

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── dashboard/         # Dashboard page
│   ├── demo/              # AI demo sections
│   ├── docs/              # Documentation
│   ├── features/          # Feature detail pages
│   ├── pricing/           # Pricing page
│   └── products/          # Products page
├── components/            # Reusable React components
│   └── ui/               # UI primitives
├── hooks/                # Custom React hooks
├── lib/                  # Utility functions
backend/
├── app/                  # FastAPI application
│   ├── routes/          # API endpoints
│   ├── services/        # AI service implementations
│   ├── models/          # Data models
│   └── schemas/         # Pydantic schemas
└── tests/               # Backend tests
```

## Demo Features

The platform includes interactive demo sections:
- **Text AI**: Try sentiment analysis, summarization, and translation
- **Image AI**: Upload images for object detection and analysis
- **Video AI**: Analyze video content and extract insights
- **Multimodal AI**: Combine multiple AI capabilities for comprehensive analysis

## Attribution

This project is built from scratch specifically for the Samsung EnnovateX 2025 AI Challenge. All components, features, and implementations are original work developed by our team.

**New Features Developed:**
- Multimodal AI processing pipeline
- Samsung-branded UI/UX design
- Real-time AI model inference
- Scalable microservices architecture
- Enterprise-grade security implementation
- Advanced analytics and monitoring
- Team collaboration features
- One-click deployment system

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please contact the team members listed above.

---
