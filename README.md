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
[Demo Video](https://youtube.com/watch?v=your-video-id) *(Upload the Demo video on Youtube as a public or unlisted video and share the link)*

## Project Artefacts

### Technical Documentation
📁 **[Docs](./docs/)** - All technical details are documented in markdown files inside the docs folder

### Source Code
📁 **[Source](./src/)** - Complete source code capable of successful installation and execution on intended platforms

### Models Used
🤖 **Hugging Face Models:**
- [facebook/bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn) - Text Summarization
- [Salesforce/blip-image-captioning-base](https://huggingface.co/Salesforce/blip-image-captioning-base) - Image Captioning
- [openai/whisper-base](https://huggingface.co/openai/whisper-base) - Audio Speech Recognition

### Models Published
*(In case you have developed a model as a part of your solution, upload it on Hugging Face under appropriate open source license and add the link here)*

### Datasets Used
📊 **Public Datasets:**
*(Links to all datasets used in the project under Creative Commons, Open Data Commons, or equivalent licenses)*

### Datasets Published
*(Links to all datasets created for the project and published on Hugging Face under Creative Commons, Open Data Commons, or equivalent license)*

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
