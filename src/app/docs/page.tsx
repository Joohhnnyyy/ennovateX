"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import NavBar from "@/components/NavBar"

import { 
  Book, 
  Search, 
  ChevronRight, 
  ChevronDown,
  FileText, 
  Code, 
  Zap, 
  Shield, 
  Brain, 
  Database, 
  Globe, 
  Settings, 
  Users, 
  Lightbulb,
  Download,
  ExternalLink,
  Copy,
  Check
} from 'lucide-react';

interface DocSection {
  id: string;
  title: string;
  icon: React.ReactNode;
  subsections?: { id: string; title: string }[];
}

interface CodeExample {
  title: string;
  language: string;
  code: string;
}

const FloatingElement: React.FC<{ delay?: number; children: React.ReactNode; className?: string }> = ({ 
  delay = 0, 
  children, 
  className = "" 
}) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ 
      opacity: 1, 
      y: 0,
      rotate: [0, 2, -2, 0],
    }}
    transition={{ 
      delay,
      duration: 0.8,
      rotate: {
        duration: 8,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }}
    className={className}
  >
    {children}
  </motion.div>
);

const CodeBlock: React.FC<CodeExample> = ({ title, language, code }) => {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-muted/50 rounded-lg border border-border overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2 bg-muted border-b border-border">
        <div className="flex items-center gap-2">
          <Code className="w-4 h-4 text-muted-foreground" />
          <span className="text-sm font-medium text-foreground">{title}</span>
          <span className="text-xs text-muted-foreground bg-background px-2 py-1 rounded">{language}</span>
        </div>
        <button
          onClick={copyToClipboard}
          className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors"
        >
          {copied ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
          {copied ? 'Copied!' : 'Copy'}
        </button>
      </div>
      <pre className="p-4 overflow-x-auto text-sm">
        <code>{code}</code>
      </pre>
    </div>
  );
};

export default function DocsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeSection, setActiveSection] = useState('getting-started');
  const [expandedSections, setExpandedSections] = useState<string[]>(['getting-started', 'api']);

  const docSections: DocSection[] = [
    {
      id: 'getting-started',
      title: 'Getting Started',
      icon: <Lightbulb className="w-5 h-5" />,
      subsections: [
        { id: 'installation', title: 'Installation' },
        { id: 'quick-start', title: 'Quick Start' },
        { id: 'configuration', title: 'Configuration' }
      ]
    },
    {
      id: 'api',
      title: 'API Reference',
      icon: <Code className="w-5 h-5" />,
      subsections: [
        { id: 'endpoints', title: 'Endpoints' },
        { id: 'rate-limits', title: 'Rate Limits' }
      ]
    },
    {
      id: 'ai-models',
      title: 'AI Models',
      icon: <Brain className="w-5 h-5" />,
      subsections: [
        { id: 'model-types', title: 'Model Types' },
        { id: 'training', title: 'Training' },
        { id: 'inference', title: 'Inference' }
      ]
    },
    {
      id: 'data',
      title: 'Data Management',
      icon: <Database className="w-5 h-5" />,
      subsections: [
        { id: 'data-sources', title: 'Data Sources' },
        { id: 'preprocessing', title: 'Preprocessing' },
        { id: 'storage', title: 'Storage' }
      ]
    },
    {
      id: 'security',
      title: 'Security',
      icon: <Shield className="w-5 h-5" />,
      subsections: [
        { id: 'encryption', title: 'Encryption' },
        { id: 'access-control', title: 'Access Control' },
        { id: 'compliance', title: 'Compliance' }
      ]
    },
    {
      id: 'performance',
      title: 'Performance',
      icon: <Zap className="w-5 h-5" />,
      subsections: [
        { id: 'optimization', title: 'Optimization' },
        { id: 'monitoring', title: 'Monitoring' },
        { id: 'scaling', title: 'Scaling' }
      ]
    },
    {
      id: 'collaboration',
      title: 'Team Collaboration',
      icon: <Users className="w-5 h-5" />,
      subsections: [
        { id: 'workspaces', title: 'Workspaces' },
        { id: 'permissions', title: 'Permissions' },
        { id: 'sharing', title: 'Sharing' }
      ]
    },
    {
      id: 'integrations',
      title: 'Integrations',
      icon: <Globe className="w-5 h-5" />,
      subsections: [
        { id: 'webhooks', title: 'Webhooks' },
        { id: 'third-party', title: 'Third-party APIs' },
        { id: 'sdks', title: 'SDKs' }
      ]
    }
  ];

  const codeExamples: CodeExample[] = [
    {
      title: 'Initialize AI Client',
      language: 'javascript',
      code: `import { EnnovateXAI } from '@ennovatex/ai-sdk';

const client = new EnnovateXAI({
  apiKey: 'your-api-key',
  endpoint: 'https://api.ennovatex.ai/v1'
});

// Initialize a new AI model
const model = await client.models.create({
  type: 'neural-network',
  name: 'my-custom-model',
  config: {
    layers: 3,
    neurons: 128
  }
});`
    },
    {
      title: 'Train Model',
      language: 'python',
      code: `from ennovatex_ai import EnnovateXAI

client = EnnovateXAI(api_key="your-api-key")

# Prepare training data
training_data = {
    "features": your_features,
    "labels": your_labels
}

# Start training
training_job = client.models.train(
    model_id="model-123",
    data=training_data,
    epochs=100,
    batch_size=32
)

print(f"Training started: {training_job.id}")`
    },
    {
      title: 'Make Predictions',
      language: 'curl',
      code: `curl -X POST https://api.ennovatex.ai/v1/predict \\
  -H "Content-Type: application/json" \\
  -d '{
    "model_id": "model-123",
    "input_data": {
      "features": [1.2, 3.4, 5.6, 7.8]
    }
  }'`
    }
  ];

  const toggleSection = (sectionId: string) => {
    setExpandedSections(prev => 
      prev.includes(sectionId) 
        ? prev.filter(id => id !== sectionId)
        : [...prev, sectionId]
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background/95 to-primary/5">

      
      {/* Floating Navigation */}
      <NavBar />
      {/* Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <FloatingElement delay={0.2} className="absolute top-20 right-20">
          <div className="p-4 bg-gradient-to-br from-primary/20 to-accent/20 rounded-2xl backdrop-blur-sm border border-white/10">
            <Book className="w-8 h-8 text-primary" />
          </div>
        </FloatingElement>

        <FloatingElement delay={0.4} className="absolute bottom-32 left-16">
          <div className="p-3 bg-gradient-to-br from-accent/20 to-primary/20 rounded-xl backdrop-blur-sm border border-white/10">
            <Code className="w-6 h-6 text-accent" />
          </div>
        </FloatingElement>

        <FloatingElement delay={0.6} className="absolute top-1/3 left-1/4">
          <div className="p-2 bg-gradient-to-br from-primary/10 to-accent/10 rounded-lg backdrop-blur-sm border border-white/5">
            <FileText className="w-4 h-4 text-muted-foreground" />
          </div>
        </FloatingElement>
      </div>

      {/* Header */}
      <div className="relative z-10 border-b border-border bg-background/80 backdrop-blur-sm">
        <div className="container mx-auto px-6 py-8">
          <div className="max-w-4xl">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-primary/10 rounded-lg">
                  <Book className="w-6 h-6 text-primary" />
                </div>
                <span className="text-sm font-medium text-primary bg-primary/10 px-3 py-1 rounded-full">
                  Documentation
                </span>
              </div>
              
              <h1 className="text-4xl md:text-5xl font-heading font-bold text-foreground mb-4">
                Developer{" "}
                <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                  Documentation
                </span>
              </h1>
              
              <p className="text-xl text-muted-foreground leading-relaxed mb-8">
                Everything you need to integrate and build with EnnovateX AI platform.
                From quick start guides to advanced API references.
              </p>

              {/* Search */}
              <div className="relative max-w-md">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Search documentation..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 bg-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors"
                />
              </div>
            </motion.div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="relative z-10">
        <div className="container mx-auto px-6 py-12">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* Sidebar */}
            <div className="lg:col-span-1">
              <div className="sticky top-8">
                <nav className="space-y-2">
                  {docSections.map((section) => (
                    <div key={section.id}>
                      <button
                        onClick={() => {
                          setActiveSection(section.id);
                          toggleSection(section.id);
                        }}
                        className={`w-full flex items-center justify-between p-3 rounded-lg text-left transition-colors ${
                          activeSection === section.id
                            ? 'bg-primary/10 text-primary border border-primary/20'
                            : 'hover:bg-muted text-muted-foreground hover:text-foreground'
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          {section.icon}
                          <span className="font-medium">{section.title}</span>
                        </div>
                        {section.subsections && (
                          expandedSections.includes(section.id) ? (
                            <ChevronDown className="w-4 h-4" />
                          ) : (
                            <ChevronRight className="w-4 h-4" />
                          )
                        )}
                      </button>
                      
                      {section.subsections && expandedSections.includes(section.id) && (
                        <div className="ml-6 mt-2 space-y-1">
                          {section.subsections.map((subsection) => (
                            <button
                              key={subsection.id}
                              className="block w-full text-left p-2 text-sm text-muted-foreground hover:text-foreground hover:bg-muted rounded transition-colors"
                            >
                              {subsection.title}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </nav>
              </div>
            </div>

            {/* Content */}
            <div className="lg:col-span-3">
              <motion.div
                key={activeSection}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
                className="space-y-8"
              >
                {/* Getting Started Section */}
                {activeSection === 'getting-started' && (
                  <div className="space-y-8">
                    <div>
                      <h2 className="text-3xl font-heading font-bold text-foreground mb-4">
                        Getting Started
                      </h2>
                      <p className="text-lg text-muted-foreground mb-6">
                        Welcome to EnnovateX AI! This guide will help you get up and running quickly.
                      </p>
                    </div>

                    <div className="grid gap-6">
                      <div className="bg-card border border-border rounded-lg p-6">
                        <h3 className="text-xl font-semibold text-foreground mb-3 flex items-center gap-2">
                          <Download className="w-5 h-5 text-primary" />
                          Installation
                        </h3>
                        <p className="text-muted-foreground mb-4">
                          Install the EnnovateX AI SDK using your preferred package manager:
                        </p>
                        <CodeBlock
                          title="Install SDK"
                          language="bash"
                          code={`# Using npm
npm install @ennovatex/ai-sdk

# Using yarn
yarn add @ennovatex/ai-sdk

# Using pnpm
pnpm add @ennovatex/ai-sdk`}
                        />
                      </div>

                      <div className="bg-card border border-border rounded-lg p-6">
                        <h3 className="text-xl font-semibold text-foreground mb-3 flex items-center gap-2">
                          <Zap className="w-5 h-5 text-primary" />
                          Quick Start
                        </h3>
                        <p className="text-muted-foreground mb-4">
                          Get started with a simple example:
                        </p>
                        <CodeBlock {...codeExamples[0]} />
                      </div>

                      <div className="bg-card border border-border rounded-lg p-6">
                        <h3 className="text-xl font-semibold text-foreground mb-3 flex items-center gap-2">
                          <Settings className="w-5 h-5 text-primary" />
                          Configuration
                        </h3>
                        <p className="text-muted-foreground mb-4">
                          Configure your environment variables:
                        </p>
                        <CodeBlock
                          title="Environment Setup"
                          language="bash"
                          code={`# .env file
ENNOVATEX_API_KEY=your_api_key_here
ENNOVATEX_ENDPOINT=https://api.ennovatex.ai/v1
ENNOVATEX_ENVIRONMENT=production`}
                        />
                      </div>
                    </div>
                  </div>
                )}

                {/* API Reference Section */}
                {activeSection === 'api' && (
                  <div className="space-y-8">
                    <div>
                      <h2 className="text-3xl font-heading font-bold text-foreground mb-4">
                        API Reference
                      </h2>
                      <p className="text-lg text-muted-foreground mb-6">
                        Complete reference for the EnnovateX AI API endpoints and methods.
                      </p>
                    </div>

                    <div className="grid gap-6">
                      <div className="bg-card border border-border rounded-lg p-6">
                        <h3 className="text-xl font-semibold text-foreground mb-3">
                          Code Examples
                        </h3>
                        <div className="space-y-4">
                          {codeExamples.map((example, index) => (
                            <CodeBlock key={index} {...example} />
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* AI Models Section */}
                {activeSection === 'ai-models' && (
                  <div className="space-y-8">
                    <div>
                      <h2 className="text-3xl font-heading font-bold text-foreground mb-4">
                        AI Models
                      </h2>
                      <p className="text-lg text-muted-foreground mb-6">
                        Comprehensive guide to AI models available in the EnnovateX platform, including text summarization, image captioning, and audio processing.
                      </p>
                    </div>

                    <div className="grid gap-6">
                      <div className="bg-card border border-border rounded-lg p-6">
                        <h3 className="text-xl font-semibold text-foreground mb-3 flex items-center gap-2">
                          <FileText className="w-5 h-5 text-primary" />
                          Text Summarizer
                        </h3>
                        <p className="text-muted-foreground mb-4">
                          The text summarizer uses the BART (Bidirectional and Auto-Regressive Transformers) model from Facebook to generate concise summaries of long text content.
                        </p>
                        
                        <div className="space-y-4">
                          <div>
                            <h4 className="text-lg font-medium text-foreground mb-2">Model Details</h4>
                            <ul className="list-disc list-inside text-muted-foreground space-y-1">
                              <li><strong>Model:</strong> facebook/bart-large-cnn</li>
                              <li><strong>Type:</strong> Sequence-to-sequence transformer</li>
                              <li><strong>Use Case:</strong> Abstractive text summarization</li>
                              <li><strong>Max Input Length:</strong> 1024 tokens</li>
                              <li><strong>Max Output Length:</strong> 150 tokens</li>
                            </ul>
                          </div>

                          <CodeBlock
                            title="Text Summarization API"
                            language="javascript"
                            code={`// Frontend API call
const response = await fetch('/api/text/summarize', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: 'Your long text content here...',
    max_length: 150,
    min_length: 30
  })
});

const result = await response.json();
console.log('Summary:', result.summary);`}
                          />

                          <CodeBlock
                            title="Backend Implementation"
                            language="python"
                            code={`# text_summariser.py - Core model functions
from transformers import BartForConditionalGeneration, BartTokenizer
import torch

def load_model_and_tokenizer():
    """Load the BART model and tokenizer for text summarization."""
    model_name = "facebook/bart-large-cnn"
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)
    return model, tokenizer

def summarize_text(text, model, tokenizer, max_length=150, min_length=30):
    """Generate a summary of the input text."""
    inputs = tokenizer.encode(
        "summarize: " + text,
        return_tensors="pt",
        max_length=1024,
        truncation=True
    )
    
    with torch.no_grad():
        summary_ids = model.generate(
            inputs,
            max_length=max_length,
            min_length=min_length,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
    
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary`}
                          />

                          <CodeBlock
                            title="API Endpoint Usage"
                            language="curl"
                            code={`curl -X POST http://localhost:8000/api/text/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your long article or document text here. This can be several paragraphs of content that you want to summarize into a shorter, more digestible format.",
    "max_length": 150,
    "min_length": 30
  }'`}
                          />

                          <div>
                            <h4 className="text-lg font-medium text-foreground mb-2">Response Format</h4>
                            <CodeBlock
                              title="API Response"
                              language="json"
                              code={`{
  "summary": "Generated summary of the input text...",
  "original_length": 1250,
  "summary_length": 87,
  "compression_ratio": 0.07,
  "processing_time": 2.34
}`}
                            />
                          </div>

                          <div>
                            <h4 className="text-lg font-medium text-foreground mb-2">Best Practices</h4>
                            <ul className="list-disc list-inside text-muted-foreground space-y-1">
                              <li>Input text should be at least 100 characters for meaningful summaries</li>
                              <li>Optimal input length is between 500-3000 characters</li>
                              <li>Use appropriate max_length based on desired summary size</li>
                              <li>For very long documents, consider chunking the text</li>
                              <li>The model works best with well-structured, coherent text</li>
                            </ul>
                          </div>
                        </div>
                      </div>

                      <div className="bg-card border border-border rounded-lg p-6">
                        <h3 className="text-xl font-semibold text-foreground mb-3 flex items-center gap-2">
                          <Brain className="w-5 h-5 text-primary" />
                          Model Performance
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          <div className="text-center p-4 bg-muted/50 rounded-lg">
                            <div className="text-2xl font-bold text-primary mb-1">~2.5s</div>
                            <div className="text-sm text-muted-foreground">Average Processing Time</div>
                          </div>
                          <div className="text-center p-4 bg-muted/50 rounded-lg">
                            <div className="text-2xl font-bold text-primary mb-1">1024</div>
                            <div className="text-sm text-muted-foreground">Max Input Tokens</div>
                          </div>
                          <div className="text-center p-4 bg-muted/50 rounded-lg">
                            <div className="text-2xl font-bold text-primary mb-1">85%</div>
                            <div className="text-sm text-muted-foreground">Accuracy Score</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Other sections placeholder */}
                {activeSection !== 'getting-started' && activeSection !== 'api' && activeSection !== 'ai-models' && (
                  <div className="space-y-8">
                    <div>
                      <h2 className="text-3xl font-heading font-bold text-foreground mb-4">
                        {docSections.find(s => s.id === activeSection)?.title}
                      </h2>
                      <p className="text-lg text-muted-foreground mb-6">
                        Documentation for this section is coming soon. Check back later for detailed guides and examples.
                      </p>
                    </div>

                    <div className="bg-card border border-border rounded-lg p-8 text-center">
                      <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-4">
                        <FileText className="w-8 h-8 text-muted-foreground" />
                      </div>
                      <h3 className="text-xl font-semibold text-foreground mb-2">
                        Content Coming Soon
                      </h3>
                      <p className="text-muted-foreground mb-4">
                        We're working on comprehensive documentation for this section.
                      </p>
                      <button className="inline-flex items-center gap-2 text-primary hover:text-primary/80 transition-colors">
                        <ExternalLink className="w-4 h-4" />
                        Request Documentation
                      </button>
                    </div>
                  </div>
                )}
              </motion.div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}