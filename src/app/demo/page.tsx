"use client";

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import NavBar from "@/components/NavBar"

import { 
  Brain, 
  Zap, 
  Sparkles,
  FileText,
  Image,
  Video,
  Layers,
  Upload,
  Download,
  Settings,
  CheckCircle,
  AlertCircle,
  Loader2
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

interface AIResult {
  type: string;
  confidence: number;
  data: any;
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
      rotate: [0, 5, -5, 0],
    }}
    transition={{ 
      delay,
      duration: 0.8,
      rotate: {
        duration: 6,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }}
    className={className}
  >
    {children}
  </motion.div>
);

// Text Section Component
const TextSection: React.FC = () => {
  const [task, setTask] = useState('');
  const [input, setInput] = useState('');
  const [result, setResult] = useState<AIResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleProcess = async () => {
    if (!task || !input) return;
    setLoading(true);
    
    try {
      let response;
      
      if (task === 'summarization') {
        // Call summarization API
        response = await fetch('http://localhost:8001/api/v1/text/text/summarize', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: input }),
        });
      } else {
        // Call other text processing APIs
        const formData = new FormData();
        formData.append('text', input);
        
        response = await fetch('http://localhost:8001/analyze/text/', {
          method: 'POST',
          body: formData,
        });
      }
      
      if (response.ok) {
        const apiResult = await response.json();
        
        // Transform API response to match expected format
        let transformedResult: AIResult;
        if (task === 'summarization') {
          transformedResult = {
            type: 'Text Summarization',
            confidence: 0.95, // Default confidence since API doesn't provide it
            data: { 
              summary: apiResult.summary || apiResult.original_summary || 'No summary available'
            }
          };
        } else {
          transformedResult = apiResult;
        }
        
        setResult(transformedResult);
      } else {
        console.error('API request failed');
        // Fallback to mock data
        let mockResult: AIResult;
        switch (task) {
          case 'generation':
            mockResult = {
              type: 'Text Generation',
              confidence: 0.92,
              data: { text: 'This is a generated response based on your input. The AI has analyzed your prompt and created relevant content.' }
            };
            break;
          case 'classification':
            mockResult = {
              type: 'Text Classification',
              confidence: 0.87,
              data: { categories: [{ label: 'Technology', score: 0.87 }, { label: 'Business', score: 0.65 }, { label: 'Innovation', score: 0.54 }] }
            };
            break;
          case 'embedding':
            mockResult = {
              type: 'Text Embedding',
              confidence: 0.95,
              data: { vector: '[0.234, -0.567, 0.891, ...]', dimensions: 768, model: 'text-embedding-ada-002' }
            };
            break;
          case 'summarization':
            mockResult = {
              type: 'Text Summarization',
              confidence: 0.89,
              data: { summary: 'This is a concise summary of your input text, highlighting the key points and main ideas while maintaining the essential information.' }
            };
            break;
          default:
            mockResult = { type: 'Unknown', confidence: 0, data: {} };
        }
        setResult(mockResult);
      }
    } catch (error) {
      console.error('Error calling API:', error);
      // Fallback to mock data
      let mockResult: AIResult;
      switch (task) {
        case 'generation':
          mockResult = {
            type: 'Text Generation',
            confidence: 0.92,
            data: { text: 'This is a generated response based on your input. The AI has analyzed your prompt and created relevant content.' }
          };
          break;
        case 'classification':
          mockResult = {
            type: 'Text Classification',
            confidence: 0.87,
            data: { categories: [{ label: 'Technology', score: 0.87 }, { label: 'Business', score: 0.65 }, { label: 'Innovation', score: 0.54 }] }
          };
          break;
        case 'embedding':
          mockResult = {
            type: 'Text Embedding',
            confidence: 0.95,
            data: { vector: '[0.234, -0.567, 0.891, ...]', dimensions: 768, model: 'text-embedding-ada-002' }
          };
          break;
        case 'summarization':
          mockResult = {
            type: 'Text Summarization',
            confidence: 0.89,
            data: { summary: 'This is a concise summary of your input text, highlighting the key points and main ideas while maintaining the essential information.' }
          };
          break;
        default:
          mockResult = { type: 'Unknown', confidence: 0, data: {} };
      }
      setResult(mockResult);
    }
    
    setLoading(false);
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="h-5 w-5 text-primary" />
          Text Processing
        </CardTitle>
        <CardDescription>Process text with AI models for generation, classification, embeddings, and summarization</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <label className="text-sm font-medium mb-2 block">Task Selection</label>
          <Select value={task} onValueChange={setTask}>
            <SelectTrigger>
              <SelectValue placeholder="Select a task" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="generation">Text Generation</SelectItem>
              <SelectItem value="classification">Text Classification</SelectItem>
              <SelectItem value="embedding">Text Embedding</SelectItem>
              <SelectItem value="summarization">Text Summarization</SelectItem>
            </SelectContent>
          </Select>
        </div>
        
        <div>
          <label className="text-sm font-medium mb-2 block">Text Input</label>
          <Textarea 
            placeholder="Enter your text here..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            rows={4}
          />
        </div>
        
        <Button onClick={handleProcess} disabled={!task || !input || loading} className="w-full">
          {loading ? 'Processing...' : 'Process Text'}
        </Button>
        
        {loading && <Progress value={33} className="w-full" />}
        
        {result && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 p-4 bg-muted rounded-lg"
          >
            <h4 className="font-semibold mb-2">{result.type} Result</h4>
            <Badge variant="secondary" className="mb-2">Confidence: {(result.confidence * 100).toFixed(1)}%</Badge>
            <div className="text-sm">
              {result.type === 'Text Generation' && <p>{result.data.text}</p>}
              {result.type === 'Text Classification' && (
                <div className="space-y-1">
                  {result.data.categories.map((cat: any, idx: number) => (
                    <div key={idx} className="flex justify-between">
                      <span>{cat.label}</span>
                      <span>{(cat.score * 100).toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              )}
              {result.type === 'Text Embedding' && (
                <div>
                  <p><strong>Vector:</strong> {result.data.vector}</p>
                  <p><strong>Dimensions:</strong> {result.data.dimensions}</p>
                  <p><strong>Model:</strong> {result.data.model}</p>
                </div>
              )}
              {result.type === 'Text Summarization' && (
                <div>
                  <p>{result.data.summary}</p>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </CardContent>
    </Card>
  );
};

// Image Section Component
const ImageSection: React.FC = () => {
  const [task, setTask] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<AIResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type.startsWith('image/')) {
      setFile(droppedFile);
    }
  };

  const handleProcess = async () => {
    if (!file) return;
    setLoading(true);
    
    // Use default task if none selected
    const selectedTask = task || 'classification';
    
    try {
      const formData = new FormData();
       formData.append('file', file);
      
      const response = await fetch('http://localhost:8000/analyze/image/', {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        const result = await response.json();
        setResult(result);
      } else {
        console.error('API request failed');
        // Fallback to mock data
        let mockResult: AIResult;
        switch (selectedTask) {
          case 'classification':
            mockResult = {
              type: 'Image Classification',
              confidence: 0.89,
              data: { labels: [{ name: 'Cat', confidence: 0.89 }, { name: 'Animal', confidence: 0.76 }, { name: 'Pet', confidence: 0.65 }] }
            };
            break;
          case 'detection':
            mockResult = {
              type: 'Object Detection',
              confidence: 0.84,
              data: { objects: [{ label: 'Person', bbox: [120, 80, 200, 300], confidence: 0.84 }, { label: 'Car', bbox: [300, 150, 450, 250], confidence: 0.78 }] }
            };
            break;
          case 'segmentation':
            mockResult = {
              type: 'Image Segmentation',
              confidence: 0.91,
              data: { segments: [{ class: 'Background', confidence: 0.91, mask_percentage: 65.2 }, { class: 'Foreground', confidence: 0.88, mask_percentage: 34.8 }] }
            };
            break;
          default:
            mockResult = { type: 'Unknown', confidence: 0, data: {} };
        }
        setResult(mockResult);
      }
    } catch (error) {
      console.error('Error calling API:', error);
      // Fallback to mock data
      let mockResult: AIResult;
      switch (selectedTask) {
        case 'classification':
          mockResult = {
            type: 'Image Classification',
            confidence: 0.89,
            data: { labels: [{ name: 'Cat', confidence: 0.89 }, { name: 'Animal', confidence: 0.76 }, { name: 'Pet', confidence: 0.65 }] }
          };
          break;
        case 'detection':
          mockResult = {
            type: 'Object Detection',
            confidence: 0.84,
            data: { objects: [{ label: 'Person', bbox: [120, 80, 200, 300], confidence: 0.84 }, { label: 'Car', bbox: [300, 150, 450, 250], confidence: 0.78 }] }
          };
          break;
        case 'segmentation':
          mockResult = {
            type: 'Image Segmentation',
            confidence: 0.91,
            data: { segments: [{ class: 'Background', confidence: 0.91, mask_percentage: 65.2 }, { class: 'Foreground', confidence: 0.88, mask_percentage: 34.8 }] }
          };
          break;
        default:
          mockResult = { type: 'Unknown', confidence: 0, data: {} };
      }
      setResult(mockResult);
    }
    
    setLoading(false);
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Image className="h-5 w-5 text-primary" />
          Image Analysis
        </CardTitle>
        <CardDescription>Analyze images with computer vision models</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <label className="text-sm font-medium mb-2 block">Task Selection</label>
          <Select value={task} onValueChange={setTask}>
            <SelectTrigger>
              <SelectValue placeholder="Select a task" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="classification">Image Classification</SelectItem>
              <SelectItem value="detection">Object Detection</SelectItem>
              <SelectItem value="segmentation">Image Segmentation</SelectItem>
            </SelectContent>
          </Select>
        </div>
        
        <div>
          <label className="text-sm font-medium mb-2 block">Image Upload</label>
          <div 
            className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
              dragOver 
                ? 'border-primary bg-primary/5' 
                : 'border-muted-foreground/25'
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <input
              type="file"
              accept=".jpeg,.jpg,.png,.gif"
              onChange={handleFileUpload}
              className="hidden"
              id="image-upload"
            />
            <label htmlFor="image-upload" className="cursor-pointer">
              <Upload className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-sm text-muted-foreground">
                {file ? file.name : 'Click to upload or drag & drop image (.jpeg, .jpg, .png, .gif)'}
              </p>
            </label>
          </div>
        </div>
        
        <Button onClick={handleProcess} disabled={!file || loading} className="w-full">
          {loading ? 'Analyzing...' : 'Analyze Image'}
        </Button>
        
        {loading && <Progress value={45} className="w-full" />}
        
        {result && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 p-4 bg-muted rounded-lg"
          >
            <h4 className="font-semibold mb-2">{result.type} Result</h4>
            <Badge variant="secondary" className="mb-2">Confidence: {(result.confidence * 100).toFixed(1)}%</Badge>
            <div className="text-sm">
              {result.type === 'Image Classification' && (
                <div className="space-y-1">
                  {result.data.labels.map((label: any, idx: number) => (
                    <div key={idx} className="flex justify-between">
                      <span>{label.name}</span>
                      <span>{(label.confidence * 100).toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              )}
              {result.type === 'Object Detection' && (
                <div className="space-y-2">
                  {result.data.objects.map((obj: any, idx: number) => (
                    <div key={idx} className="border rounded p-2">
                      <p><strong>{obj.label}</strong> - {(obj.confidence * 100).toFixed(1)}%</p>
                      <p className="text-xs text-muted-foreground">Bbox: [{obj.bbox.join(', ')}]</p>
                    </div>
                  ))}
                </div>
              )}
              {result.type === 'Image Segmentation' && (
                <div className="space-y-1">
                  {result.data.segments.map((seg: any, idx: number) => (
                    <div key={idx} className="flex justify-between">
                      <span>{seg.class}</span>
                      <span>{seg.mask_percentage}% ({(seg.confidence * 100).toFixed(1)}%)</span>
                    </div>
                  ))}
                </div>
              )}
              {result.type === 'Image Analysis' && (
                <div className="space-y-2">
                  <div className="p-3 bg-muted rounded-lg">
                    <p className="font-medium mb-1">Description:</p>
                    <p className="text-sm">{result.data.caption}</p>
                  </div>
                  {result.data.objects && result.data.objects.length > 0 && (
                    <div>
                      <p className="font-medium mb-1">Detected Objects:</p>
                      <div className="flex flex-wrap gap-1">
                        {result.data.objects.map((obj: string, idx: number) => (
                          <Badge key={idx} variant="outline" className="text-xs">{obj}</Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </motion.div>
        )}
      </CardContent>
    </Card>
  );
};



// Video Section Component
const VideoSection: React.FC = () => {
  const [task, setTask] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<AIResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleProcess = async () => {
    if (!task || !file) return;
    setLoading(true);
    
    try {
      const formData = new FormData();
       formData.append('file', file);
       formData.append('task', task);
      
      const response = await fetch('http://localhost:8000/analyze/video/', {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        const result = await response.json();
        setResult(result);
      } else {
        console.error('API request failed');
        // Fallback to mock data
        let mockResult: AIResult;
        switch (task) {
          case 'action':
            mockResult = {
              type: 'Action Recognition',
              confidence: 0.86,
              data: { actions: [{ action: 'Walking', timestamp: '0:05-0:12', confidence: 0.86 }, { action: 'Running', timestamp: '0:15-0:22', confidence: 0.79 }] }
            };
            break;
          case 'tracking':
            mockResult = {
              type: 'Object Tracking',
              confidence: 0.91,
              data: { objects: [{ id: 1, label: 'Person', frames: 145, confidence: 0.91 }, { id: 2, label: 'Vehicle', frames: 89, confidence: 0.83 }] }
            };
            break;
          default:
            mockResult = { type: 'Unknown', confidence: 0, data: {} };
        }
        setResult(mockResult);
      }
    } catch (error) {
      console.error('Error calling API:', error);
      // Fallback to mock data
      let mockResult: AIResult;
      switch (task) {
        case 'action':
          mockResult = {
            type: 'Action Recognition',
            confidence: 0.86,
            data: { actions: [{ action: 'Walking', timestamp: '0:05-0:12', confidence: 0.86 }, { action: 'Running', timestamp: '0:15-0:22', confidence: 0.79 }] }
          };
          break;
        case 'tracking':
          mockResult = {
            type: 'Object Tracking',
            confidence: 0.91,
            data: { objects: [{ id: 1, label: 'Person', frames: 145, confidence: 0.91 }, { id: 2, label: 'Vehicle', frames: 89, confidence: 0.83 }] }
          };
          break;
        default:
          mockResult = { type: 'Unknown', confidence: 0, data: {} };
      }
      setResult(mockResult);
    }
    
    setLoading(false);
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Video className="h-5 w-5 text-primary" />
          Video Analysis
        </CardTitle>
        <CardDescription>Analyze video content with computer vision models</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <label className="text-sm font-medium mb-2 block">Task Selection</label>
          <Select value={task} onValueChange={setTask}>
            <SelectTrigger>
              <SelectValue placeholder="Select a task" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="action">Action Recognition</SelectItem>
              <SelectItem value="tracking">Object Tracking</SelectItem>
            </SelectContent>
          </Select>
        </div>
        
        <div>
          <label className="text-sm font-medium mb-2 block">Video Upload</label>
          <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-6 text-center">
            <input
              type="file"
              accept=".mp4,.webm,.mov"
              onChange={handleFileUpload}
              className="hidden"
              id="video-upload"
            />
            <label htmlFor="video-upload" className="cursor-pointer">
              <Upload className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-sm text-muted-foreground">
                {file ? file.name : 'Click to upload video (.mp4, .webm, .mov)'}
              </p>
            </label>
          </div>
        </div>
        
        <Button onClick={handleProcess} disabled={!task || !file || loading} className="w-full">
          {loading ? 'Analyzing...' : 'Analyze Video'}
        </Button>
        
        {loading && <Progress value={75} className="w-full" />}
        
        {result && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 p-4 bg-muted rounded-lg"
          >
            <h4 className="font-semibold mb-2">{result.type} Result</h4>
            <Badge variant="secondary" className="mb-2">Confidence: {(result.confidence * 100).toFixed(1)}%</Badge>
            <div className="text-sm">
              {result.type === 'Action Recognition' && (
                <div className="space-y-2">
                  {result.data.actions.map((action: any, idx: number) => (
                    <div key={idx} className="border rounded p-2">
                      <p><strong>{action.action}</strong> - {(action.confidence * 100).toFixed(1)}%</p>
                      <p className="text-xs text-muted-foreground">Timestamp: {action.timestamp}</p>
                    </div>
                  ))}
                </div>
              )}
              {result.type === 'Object Tracking' && (
                <div className="space-y-2">
                  {result.data.objects.map((obj: any, idx: number) => (
                    <div key={idx} className="border rounded p-2">
                      <p><strong>ID {obj.id}: {obj.label}</strong> - {(obj.confidence * 100).toFixed(1)}%</p>
                      <p className="text-xs text-muted-foreground">Tracked for {obj.frames} frames</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </motion.div>
        )}
      </CardContent>
    </Card>
  );
};

// Multimodal Section Component
const MultimodalSection: React.FC = () => {
  const [textInput, setTextInput] = useState('');
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [result, setResult] = useState<AIResult | null>(null);
  const [loading, setLoading] = useState(false);

  const getModalityCount = () => {
    let count = 0;
    if (textInput.trim()) count++;
    if (imageFile) count++;
    if (videoFile) count++;
    return count;
  };

  const getUsedModalities = () => {
    const modalities = [];
    if (textInput.trim()) modalities.push('Text');
    if (imageFile) modalities.push('Image');
    if (videoFile) modalities.push('Video');
    return modalities;
  };

  const handleProcess = async () => {
    if (getModalityCount() < 2) return;
    setLoading(true);
    
    try {
      const formData = new FormData();
      if (textInput.trim()) formData.append('text', textInput);
      if (imageFile) formData.append('image', imageFile);
      if (videoFile) formData.append('video', videoFile);
      
      const response = await fetch('http://localhost:8000/analyze/multimodal/', {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        const result = await response.json();
        setResult(result);
      } else {
        console.error('API request failed');
        // Fallback to mock data
        const usedModalities = getUsedModalities();
        const mockResult: AIResult = {
          type: 'Multimodal Analysis',
          confidence: 0.89,
          data: {
            summary: 'Combined analysis reveals strong correlation between input modalities. The AI has successfully processed and integrated multiple data types.',
            modalities: usedModalities,
            individual_results: {
              text: textInput.trim() ? 'Text sentiment: Positive (0.87)' : null,
              image: imageFile ? 'Image contains: Person, outdoor scene (0.92)' : null,
              video: videoFile ? 'Video analysis: Motion detected, 2 objects tracked (0.88)' : null
            }
          }
        };
        setResult(mockResult);
      }
    } catch (error) {
      console.error('Error calling API:', error);
      // Fallback to mock data
      const usedModalities = getUsedModalities();
      const mockResult: AIResult = {
        type: 'Multimodal Analysis',
        confidence: 0.89,
        data: {
          summary: 'Combined analysis reveals strong correlation between input modalities. The AI has successfully processed and integrated multiple data types.',
          modalities: usedModalities,
          individual_results: {
            text: textInput.trim() ? 'Text sentiment: Positive (0.87)' : null,
            image: imageFile ? 'Image contains: Person, outdoor scene (0.92)' : null,
            video: videoFile ? 'Video analysis: Motion detected, 2 objects tracked (0.88)' : null
          }
        }
      };
      setResult(mockResult);
    }
    
    setLoading(false);
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Layers className="h-5 w-5 text-primary" />
          Multimodal Analysis
        </CardTitle>
        <CardDescription>Combine multiple input types for comprehensive AI analysis (minimum 2 modalities required)</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <label className="text-sm font-medium mb-2 block">Text Input (Optional)</label>
          <Textarea 
            placeholder="Enter text for analysis..."
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            rows={3}
          />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="text-sm font-medium mb-2 block">Image (Optional)</label>
            <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-4 text-center">
              <input
                type="file"
                accept=".jpeg,.jpg,.png,.gif"
                onChange={(e) => e.target.files && setImageFile(e.target.files[0])}
                className="hidden"
                id="multimodal-image"
              />
              <label htmlFor="multimodal-image" className="cursor-pointer">
                <Image className="h-6 w-6 mx-auto mb-1 text-muted-foreground" />
                <p className="text-xs text-muted-foreground">
                  {imageFile ? imageFile.name : 'Upload image'}
                </p>
              </label>
            </div>
          </div>
          

          
          <div>
            <label className="text-sm font-medium mb-2 block">Video (Optional)</label>
            <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-4 text-center">
              <input
                type="file"
                accept=".mp4,.webm,.mov"
                onChange={(e) => e.target.files && setVideoFile(e.target.files[0])}
                className="hidden"
                id="multimodal-video"
              />
              <label htmlFor="multimodal-video" className="cursor-pointer">
                <Video className="h-6 w-6 mx-auto mb-1 text-muted-foreground" />
                <p className="text-xs text-muted-foreground">
                  {videoFile ? videoFile.name : 'Upload video'}
                </p>
              </label>
            </div>
          </div>
        </div>
        
        <div className="flex items-center justify-between">
          <Badge variant={getModalityCount() >= 2 ? "default" : "secondary"}>
            {getModalityCount()}/4 Modalities Selected
          </Badge>
          {getModalityCount() < 2 && (
            <p className="text-sm text-muted-foreground">Select at least 2 modalities</p>
          )}
        </div>
        
        <Button onClick={handleProcess} disabled={getModalityCount() < 2 || loading} className="w-full">
          {loading ? 'Analyzing...' : 'Analyze Multimodal Input'}
        </Button>
        
        {loading && <Progress value={85} className="w-full" />}
        
        {result && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 p-4 bg-muted rounded-lg"
          >
            <h4 className="font-semibold mb-2">{result.type} Result</h4>
            <Badge variant="secondary" className="mb-2">Confidence: {(result.confidence * 100).toFixed(1)}%</Badge>
            
            <div className="space-y-3 text-sm">
              <div>
                <h5 className="font-medium mb-1">Combined Analysis Summary</h5>
                <p>{result.data.summary}</p>
              </div>
              
              <div>
                <h5 className="font-medium mb-1">Modalities Used</h5>
                <div className="flex gap-1 flex-wrap">
                  {result.data.modalities.map((modality: string, idx: number) => (
                    <Badge key={idx} variant="outline" className="text-xs">{modality}</Badge>
                  ))}
                </div>
              </div>
              
              <div>
                <h5 className="font-medium mb-1">Individual Results</h5>
                <div className="space-y-1">
                  {Object.entries(result.data.individual_results).map(([key, value]: [string, any]) => 
                    value && (
                      <div key={key} className="text-xs">
                        <strong className="capitalize">{key}:</strong> {value}
                      </div>
                    )
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </CardContent>
    </Card>
  );
};

export default function DemoPage() {
  const [activeSection, setActiveSection] = useState('text');

  const sections = [
    { id: 'text', title: 'Text Processing', icon: FileText, component: <TextSection /> },
    { id: 'image', title: 'Image Analysis', icon: Image, component: <ImageSection /> },
    { id: 'video', title: 'Video Analysis', icon: Video, component: <VideoSection /> },
    { id: 'multimodal', title: 'Multimodal Analysis', icon: Layers, component: <MultimodalSection /> }
  ];

  const getCurrentSection = () => {
    return sections.find(section => section.id === activeSection) || sections[0];
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background/95 to-primary/5">

      
      {/* Floating Navigation */}
      <NavBar />
      {/* Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <FloatingElement delay={0.2} className="absolute top-20 right-20">
          <div className="p-4 bg-gradient-to-br from-primary/20 to-accent/20 rounded-2xl backdrop-blur-sm border border-white/10">
            <Sparkles className="w-8 h-8 text-primary" />
          </div>
        </FloatingElement>

        <FloatingElement delay={0.4} className="absolute top-40 left-20">
          <div className="p-4 bg-gradient-to-br from-accent/20 to-primary/20 rounded-2xl backdrop-blur-sm border border-white/10">
            <Zap className="w-8 h-8 text-accent" />
          </div>
        </FloatingElement>

        <FloatingElement delay={0.6} className="absolute bottom-40 right-32">
          <div className="p-4 bg-gradient-to-br from-[#00ADEF]/20 to-[#1428A0]/20 rounded-2xl backdrop-blur-sm border border-white/10">
            <Brain className="w-8 h-8 text-[#00ADEF]" />
          </div>
        </FloatingElement>
      </div>

      <div className="relative z-10 container mx-auto px-6 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <div className="mb-8">
            <svg 
              height="50" 
              width="200" 
              xmlns="http://www.w3.org/2000/svg" 
              viewBox="0 0 120 32"
              className="fill-current"
            >
              <path d="M8 19.651v-1.14h3.994v1.45a1.334 1.334 0 0 0 1.494 1.346 1.3 1.3 0 0 0 1.444-1.007 1.833 1.833 0 0 0-.026-1.113c-.773-1.944-6.055-2.824-6.726-5.854a5.347 5.347 0 0 1-.025-2.02C8.567 8.88 10.705 8 13.359 8c2.113 0 5.025.492 5.025 3.754v1.062h-3.71v-.932a1.275 1.275 0 0 0-1.392-1.347 1.25 1.25 0 0 0-1.365 1.01 2.021 2.021 0 0 0 .026.777c.437 1.734 6.081 2.667 6.7 5.8a6.943 6.943 0 0 1 .025 2.46C18.307 23.068 16.091 24 13.412 24 10.6 24 8 22.99 8 19.651zm48.392-.051v-1.14h3.943v1.424A1.312 1.312 0 0 0 61.8 21.23a1.286 1.286 0 0 0 1.443-.984 1.759 1.759 0 0 0-.025-1.088c-.748-1.915-5.979-2.8-6.648-5.825a5.215 5.215 0 0 1-.026-1.994c.415-2.407 2.556-3.287 5.156-3.287 2.088 0 4.973.518 4.973 3.728v1.036h-3.684v-.906a1.268 1.268 0 0 0-1.365-1.346 1.2 1.2 0 0 0-1.34.984 2.017 2.017 0 0 0 .025.777c.412 1.734 6 2.641 6.623 5.747a6.806 6.806 0 0 1 .025 2.434c-.361 2.486-2.551 3.392-5.2 3.392-2.787.002-5.365-1.011-5.365-4.298zm14.121.545a5.876 5.876 0 0 1-.025-.985V8.44h3.762v11.055a4.111 4.111 0 0 0 .025.57 1.468 1.468 0 0 0 2.835 0 3.97 3.97 0 0 0 .026-.57V8.44H80.9v10.718c0 .285-.026.829-.026.985-.257 2.8-2.448 3.7-5.179 3.7s-4.924-.905-5.182-3.7zm30.974-.156a7.808 7.808 0 0 1-.052-.989v-6.288c0-.259.025-.725.051-.985.335-2.795 2.577-3.675 5.231-3.675 2.629 0 4.947.88 5.206 3.676a7.185 7.185 0 0 1 .025.985v.487h-3.762v-.824a3.1 3.1 0 0 0-.051-.57 1.553 1.553 0 0 0-2.964 0 3.088 3.088 0 0 0-.051.7v6.834a4.17 4.17 0 0 0 .026.57 1.472 1.472 0 0 0 1.571 1.09 1.406 1.406 0 0 0 1.52-1.087 2.09 2.09 0 0 0 .026-.57v-2.178h-1.52V14.99H112V19a7.674 7.674 0 0 1-.052.984c-.257 2.718-2.6 3.676-5.231 3.676s-4.973-.955-5.23-3.673zm-52.438 3.389l-.1-13.825-2.58 13.825h-3.762L40.055 9.553l-.1 13.825h-3.713l.309-14.912h6.056l1.881 11.651 1.881-11.651h6.055l.335 14.912zm-19.79 0l-2.01-13.825-2.062 13.825h-4.019L23.9 8.466h6.623l2.732 14.912zm62.977-.155L88.5 10.822l.206 12.4h-3.66V8.466h5.514l3.5 12.013-.201-12.013h3.685v14.758z" fill="url(#gradient)" />
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#1428A0" />
                  <stop offset="100%" stopColor="#00ADEF" />
                </linearGradient>
              </defs>
            </svg>
            <div className="text-2xl font-heading font-semibold text-primary mt-2">
              EnnovateX AI Demo
            </div>
          </div>

          <h1 className="text-4xl md:text-6xl font-heading font-bold text-foreground mb-6">
            Experience the Future
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Discover how Samsung's cutting-edge AI platform transforms the way you work, 
            analyze data, and make decisions. See it in action.
          </p>
        </motion.div>



        {/* Section Navigation */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="flex flex-wrap justify-center gap-4 mb-8"
        >
          {sections.map((section) => {
            const IconComponent = section.icon;
            return (
              <Button
                key={section.id}
                variant={activeSection === section.id ? "default" : "outline"}
                onClick={() => setActiveSection(section.id)}
                className="flex items-center gap-2"
              >
                <IconComponent className="w-4 h-4" />
                {section.title}
              </Button>
            );
          })}
        </motion.div>

        {/* Demo Container */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="max-w-4xl mx-auto"
        >
          <AnimatePresence mode="wait">
            <motion.div
              key={activeSection}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.5 }}
            >
              {getCurrentSection().component}
            </motion.div>
          </AnimatePresence>
        </motion.div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="text-center mt-16"
        >
          <div className="bg-gradient-to-r from-primary/10 to-accent/10 rounded-2xl p-8 border border-border/50">
            <h3 className="text-2xl font-heading font-bold text-foreground mb-4">
              Ready to Get Started?
            </h3>
            <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
              Experience the full power of Samsung EnnovateX AI platform. 
              Join thousands of organizations already transforming their operations.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-primary hover:bg-primary/90 text-primary-foreground px-8 py-3 rounded-xl font-semibold transition-all duration-200">
                Start Free Trial
              </button>
              <button className="bg-secondary hover:bg-secondary/80 text-secondary-foreground px-8 py-3 rounded-xl font-semibold transition-all duration-200">
                Schedule Demo
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}