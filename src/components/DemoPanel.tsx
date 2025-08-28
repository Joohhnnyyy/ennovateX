"use client"

import { useState, useRef, useCallback } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Slider } from "@/components/ui/slider"
import { Switch } from "@/components/ui/switch"
import { Progress } from "@/components/ui/progress"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { 
  Upload, 
  FileText, 
  Image as ImageIcon, 
  Video,
  Download,
  Copy,
  Play,
  RotateCcw,
  Send,
  Loader2,
  CheckCircle,
  AlertCircle,
  X,
  FileText as SummarizeIcon
} from "lucide-react"
import { toast } from "sonner"

interface DemoResult {
  id: string
  type: "text" | "image" | "video"
  content: string
  title: string
  timestamp: Date
}

interface UploadFile {
  file: File
  preview?: string
  status: "pending" | "uploading" | "success" | "error"
  progress: number
}

interface DemoPanelProps {
  apiEndpoint?: string
  maxFileSize?: number
  allowedFileTypes?: string[]
  className?: string
}

export default function DemoPanel({
  apiEndpoint = "/api/demo",
  maxFileSize = 10 * 1024 * 1024, // 10MB
  allowedFileTypes = ["image/*", "text/*", "video/*"],
  className
}: DemoPanelProps) {
  const [activeTab, setActiveTab] = useState("text")
  const [textInput, setTextInput] = useState("")
  const [textProcessingType, setTextProcessingType] = useState("summarize")
  const [isLoading, setIsLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [results, setResults] = useState<DemoResult[]>([])
  const [uploadFile, setUploadFile] = useState<UploadFile | null>(null)
  const [isDragOver, setIsDragOver] = useState(false)
  
  // Live demo controls
  const [temperature, setTemperature] = useState([0.7])
  const [modelSize, setModelSize] = useState([2])
  const [steps, setSteps] = useState([20])
  const [useAdvanced, setUseAdvanced] = useState(false)

  const fileInputRef = useRef<HTMLInputElement>(null)
  const abortControllerRef = useRef<AbortController | null>(null)

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes"
    const k = 1024
    const sizes = ["Bytes", "KB", "MB", "GB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
  }

  const getFileIcon = (type: string) => {
    if (type.startsWith("image/")) return <ImageIcon className="h-6 w-6" />
    if (type.startsWith("video/")) return <Video className="h-6 w-6" />
    return <FileText className="h-6 w-6" />
  }

  const handleSubmit = async (type: "text" | "upload" | "live") => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    abortControllerRef.current = new AbortController()
    setIsLoading(true)
    setProgress(0)

    try {
      let payload: any = { type }
      
      if (type === "text") {
        payload.text = textInput
      } else if (type === "upload" && uploadFile) {
        const formData = new FormData()
        formData.append("file", uploadFile.file)
        payload = formData
      } else if (type === "live") {
        payload.config = {
          temperature: temperature[0],
          modelSize: modelSize[0],
          steps: steps[0],
          useAdvanced
        }
      }

      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress(prev => Math.min(prev + Math.random() * 20, 90))
      }, 200)

      let result: any
      
      if (type === "text") {
        // Call backend API for text summarization
        const response = await fetch('http://localhost:8001/api/v1/text/text/summarize', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text: textInput,
            summary_type: textProcessingType === 'summarize' ? 'abstractive' : 'extractive'
          }),
          signal: abortControllerRef.current.signal
        })
        
        if (!response.ok) {
          throw new Error(`API request failed: ${response.status}`)
        }
        
        const data = await response.json()
        
        clearInterval(progressInterval)
        setProgress(100)
        
        result = {
          type: "text" as const,
          content: data.summary,
          title: textProcessingType === 'summarize' ? "Text Summarization Result" : "Text Analysis Result"
        }
      } else {
        // Keep mock responses for upload and live processing
        await new Promise(resolve => setTimeout(resolve, 1500 + Math.random() * 1000))
        
        clearInterval(progressInterval)
        setProgress(100)

        const mockResults = {
          upload: {
            type: "text" as const,
            content: `File "${uploadFile?.file.name}" processed successfully. Detected ${Math.floor(Math.random() * 50) + 10} key features with 94% accuracy.`,
            title: "File Processing Result"
          },
          live: {
            type: "text" as const,
            content: `Live processing completed with temperature: ${temperature[0]}, model size: ${modelSize[0]}, steps: ${steps[0]}. Generated high-quality output with advanced features ${useAdvanced ? 'enabled' : 'disabled'}.`,
            title: "Live Processing Result"
          }
        }
        
        result = mockResults[type]
       }
       
       const newResult: DemoResult = {
         id: Date.now().toString(),
         type: result.type,
         content: result.content,
         title: result.title,
         timestamp: new Date()
       }

      setResults(prev => [newResult, ...prev])
      
      toast.success("Processing completed!", {
        description: "Your result is ready below."
      })

      // Reset form
      if (type === "text") setTextInput("")
      if (type === "upload") setUploadFile(null)

    } catch (error: any) {
      if (error.name === "AbortError") {
        toast.info("Request cancelled")
      } else {
        toast.error("Processing failed", {
          description: error.message || "Please try again.",
          action: {
            label: "Retry",
            onClick: () => handleSubmit(type)
          }
        })
      }
    } finally {
      setIsLoading(false)
      setProgress(0)
      abortControllerRef.current = null
    }
  }

  const handleFileSelect = useCallback((files: File[]) => {
    const file = files[0]
    if (!file) return

    if (file.size > maxFileSize) {
      toast.error("File too large", {
        description: `Maximum file size is ${formatFileSize(maxFileSize)}`
      })
      return
    }

    const uploadFileObj: UploadFile = {
      file,
      status: "pending",
      progress: 0
    }

    // Generate preview for images
    if (file.type.startsWith("image/")) {
      const reader = new FileReader()
      reader.onload = (e) => {
        setUploadFile(prev => prev ? { ...prev, preview: e.target?.result as string } : null)
      }
      reader.readAsDataURL(file)
    }

    setUploadFile(uploadFileObj)
  }, [maxFileSize])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
    const files = Array.from(e.dataTransfer.files)
    handleFileSelect(files)
  }, [handleFileSelect])

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
  }, [])

  const copyToClipboard = async (content: string) => {
    try {
      await navigator.clipboard.writeText(content)
      toast.success("Copied to clipboard")
    } catch (error) {
      toast.error("Failed to copy")
    }
  }

  const downloadResult = (result: DemoResult) => {
    const blob = new Blob([result.content], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `${result.title}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    toast.success("Downloaded")
  }

  const rerunResult = (result: DemoResult) => {
    toast.info("Re-running with previous settings...")
  }

  return (
    <div className={`w-full max-w-4xl mx-auto p-6 ${className}`}>
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3 mb-8 bg-card/50 backdrop-blur-sm border border-border/50">
          <TabsTrigger 
            value="text" 
            className="data-[state=active]:bg-primary/20 data-[state=active]:text-primary relative overflow-hidden"
          >
            <span className="relative z-10">Text → Output</span>
            {activeTab === "text" && (
              <motion.div
                layoutId="activeTab"
                className="absolute inset-0 bg-gradient-to-r from-primary/30 to-primary/20 backdrop-blur-sm"
                style={{ borderRadius: "inherit" }}
                transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
              />
            )}
          </TabsTrigger>
          <TabsTrigger 
            value="upload"
            className="data-[state=active]:bg-primary/20 data-[state=active]:text-primary relative overflow-hidden"
          >
            <span className="relative z-10">Upload</span>
            {activeTab === "upload" && (
              <motion.div
                layoutId="activeTab"
                className="absolute inset-0 bg-gradient-to-r from-primary/30 to-primary/20 backdrop-blur-sm"
                style={{ borderRadius: "inherit" }}
                transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
              />
            )}
          </TabsTrigger>
          <TabsTrigger 
            value="live"
            className="data-[state=active]:bg-primary/20 data-[state=active]:text-primary relative overflow-hidden"
          >
            <span className="relative z-10">Live Demo</span>
            {activeTab === "live" && (
              <motion.div
                layoutId="activeTab"
                className="absolute inset-0 bg-gradient-to-r from-primary/30 to-primary/20 backdrop-blur-sm"
                style={{ borderRadius: "inherit" }}
                transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
              />
            )}
          </TabsTrigger>
        </TabsList>

        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <TabsContent value="text" className="space-y-6">
              <Card className="bg-card/50 backdrop-blur-sm border-border/50">
                <CardHeader>
                  <CardTitle className="text-lg font-heading">Text Processing</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="processing-type">Processing Type</Label>
                    <Select value={textProcessingType} onValueChange={setTextProcessingType} disabled={isLoading}>
                      <SelectTrigger className="bg-input/50 border-border/50">
                        <SelectValue placeholder="Select processing type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="summarize">
                          <div className="flex items-center space-x-2">
                            <SummarizeIcon className="h-4 w-4" />
                            <span>Text Summarization</span>
                          </div>
                        </SelectItem>
                        <SelectItem value="analyze">
                          <div className="flex items-center space-x-2">
                            <FileText className="h-4 w-4" />
                            <span>Text Analysis</span>
                          </div>
                        </SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="text-input">
                      {textProcessingType === "summarize" ? "Enter text to summarize" : "Enter text to analyze"}
                    </Label>
                    <Textarea
                      id="text-input"
                      placeholder={textProcessingType === "summarize" ? "Paste your long text here for summarization..." : "Type your message here for analysis..."}
                      value={textInput}
                      onChange={(e) => setTextInput(e.target.value)}
                      className="min-h-[120px] resize-y bg-input/50 border-border/50"
                      disabled={isLoading}
                    />
                  </div>
                  <Button
                    onClick={() => handleSubmit("text")}
                    disabled={!textInput.trim() || isLoading}
                    className="w-full"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        {textProcessingType === "summarize" ? "Summarizing..." : "Analyzing..."}
                      </>
                    ) : (
                      <>
                        {textProcessingType === "summarize" ? (
                          <SummarizeIcon className="mr-2 h-4 w-4" />
                        ) : (
                          <Send className="mr-2 h-4 w-4" />
                        )}
                        {textProcessingType === "summarize" ? "Summarize Text" : "Analyze Text"}
                      </>
                    )}
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="upload" className="space-y-6">
              <Card className="bg-card/50 backdrop-blur-sm border-border/50">
                <CardHeader>
                  <CardTitle className="text-lg font-heading">File Upload</CardTitle>
                </CardHeader>
                <CardContent>
                  <div
                    className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200 ${
                      isDragOver
                        ? "border-primary bg-primary/5 scale-[1.02]"
                        : "border-border/50 hover:border-primary/50"
                    }`}
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                  >
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept={allowedFileTypes.join(",")}
                      onChange={(e) => e.target.files && handleFileSelect(Array.from(e.target.files))}
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      disabled={isLoading}
                    />
                    
                    {uploadFile ? (
                      <div className="space-y-4">
                        <div className="flex items-center justify-center space-x-3">
                          {getFileIcon(uploadFile.file.type)}
                          <div className="text-left">
                            <p className="font-medium">{uploadFile.file.name}</p>
                            <p className="text-sm text-muted-foreground">
                              {formatFileSize(uploadFile.file.size)}
                            </p>
                          </div>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={(e) => {
                              e.stopPropagation()
                              setUploadFile(null)
                            }}
                            disabled={isLoading}
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </div>
                        
                        {uploadFile.preview && (
                          <img
                            src={uploadFile.preview}
                            alt="Preview"
                            className="mx-auto max-h-32 rounded-lg object-cover"
                          />
                        )}
                        
                        <Button
                          onClick={() => handleSubmit("upload")}
                          disabled={isLoading}
                          className="w-full"
                        >
                          {isLoading ? (
                            <>
                              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                              Uploading...
                            </>
                          ) : (
                            <>
                              <Upload className="mr-2 h-4 w-4" />
                              Process File
                            </>
                          )}
                        </Button>
                      </div>
                    ) : (
                      <div className="space-y-4">
                        <Upload className="mx-auto h-12 w-12 text-muted-foreground" />
                        <div>
                          <p className="text-lg font-medium">
                            {isDragOver ? "Drop your file here" : "Drag & drop your file here"}
                          </p>
                          <p className="text-sm text-muted-foreground mt-2">
                            Or click to browse • Max {formatFileSize(maxFileSize)}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="live" className="space-y-6">
              <Card className="bg-card/50 backdrop-blur-sm border-border/50">
                <CardHeader>
                  <CardTitle className="text-lg font-heading">Live Configuration</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-3">
                      <Label htmlFor="temperature">Temperature: {temperature[0]}</Label>
                      <Slider
                        id="temperature"
                        min={0}
                        max={1}
                        step={0.1}
                        value={temperature}
                        onValueChange={setTemperature}
                        disabled={isLoading}
                        className="w-full"
                      />
                    </div>
                    
                    <div className="space-y-3">
                      <Label htmlFor="model-size">Model Size: {modelSize[0]}B</Label>
                      <Slider
                        id="model-size"
                        min={1}
                        max={10}
                        step={1}
                        value={modelSize}
                        onValueChange={setModelSize}
                        disabled={isLoading}
                        className="w-full"
                      />
                    </div>
                    
                    <div className="space-y-3">
                      <Label htmlFor="steps">Steps: {steps[0]}</Label>
                      <Slider
                        id="steps"
                        min={1}
                        max={100}
                        step={1}
                        value={steps}
                        onValueChange={setSteps}
                        disabled={isLoading}
                        className="w-full"
                      />
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <Switch
                        id="advanced"
                        checked={useAdvanced}
                        onCheckedChange={setUseAdvanced}
                        disabled={isLoading}
                      />
                      <Label htmlFor="advanced">Use Advanced Mode</Label>
                    </div>
                  </div>
                  
                  <Button
                    onClick={() => handleSubmit("live")}
                    disabled={isLoading}
                    className="w-full"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Running...
                      </>
                    ) : (
                      <>
                        <Play className="mr-2 h-4 w-4" />
                        Run Demo
                      </>
                    )}
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>
          </motion.div>
        </AnimatePresence>

        {/* Progress Bar */}
        {isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-6"
          >
            <Card className="bg-card/50 backdrop-blur-sm border-border/50">
              <CardContent className="pt-6">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Processing...</span>
                    <span>{Math.round(progress)}%</span>
                  </div>
                  <Progress value={progress} className="h-2" />
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Results */}
        {results.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-8 space-y-4"
          >
            <h3 className="text-xl font-heading">Results</h3>
            <div className="space-y-4">
              <AnimatePresence>
                {results.map((result, index) => (
                  <motion.div
                    key={result.id}
                    initial={{ opacity: 0, y: 20, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: -20, scale: 0.95 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                  >
                    <Card className="bg-card/70 backdrop-blur-sm border-border/50 shadow-lg">
                      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
                        <div>
                          <CardTitle className="text-base">{result.title}</CardTitle>
                          <p className="text-sm text-muted-foreground">
                            {result.timestamp.toLocaleTimeString()}
                          </p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => copyToClipboard(result.content)}
                          >
                            <Copy className="h-4 w-4" />
                          </Button>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => downloadResult(result)}
                          >
                            <Download className="h-4 w-4" />
                          </Button>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => rerunResult(result)}
                          >
                            <RotateCcw className="h-4 w-4" />
                          </Button>
                        </div>
                      </CardHeader>
                      <CardContent>
                        {result.type === "text" ? (
                          <p className="text-sm whitespace-pre-wrap">{result.content}</p>
                        ) : result.type === "image" ? (
                          <img
                            src={result.content}
                            alt="Generated"
                            className="max-w-full h-auto rounded-lg"
                          />
                        ) : result.type === "video" ? (
                          <video controls className="w-full rounded-lg">
                            <source src={result.content} />
                          </video>
                        ) : null}
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          </motion.div>
        )}
      </Tabs>
    </div>
  )
}