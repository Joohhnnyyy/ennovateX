"use client"

import React, { useState, useEffect, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Calendar,
  ChevronDown,
  Search,
  ExternalLink,
  TrendingUp,
  TrendingDown,
  Play,
  RotateCcw,
  Eye,
  Activity,
  Zap,
  Clock,
  DollarSign,
  Server,
  CheckCircle2,
  XCircle,
  AlertCircle,
  MoreHorizontal
} from 'lucide-react'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'

// Mock data
const mockMetrics = {
  activeModels: { value: 24, change: 12, trend: 'up' as const },
  throughput: { value: 1247, change: -3.2, trend: 'down' as const },
  latency: { value: 89, change: -15.7, trend: 'up' as const },
  cost: { value: 342.50, change: 8.3, trend: 'down' as const }
}

const mockActivities = [
  { id: 1, name: 'GPT-4 Classification', type: 'inference', duration: '2.3s', status: 'success' as const, timestamp: '2 min ago' },
  { id: 2, name: 'BERT Sentiment Analysis', type: 'training', duration: '45m', status: 'running' as const, timestamp: '5 min ago' },
  { id: 3, name: 'Image Recognition', type: 'inference', duration: '1.1s', status: 'success' as const, timestamp: '8 min ago' },
  { id: 4, name: 'Text Summarization', type: 'inference', duration: '3.7s', status: 'error' as const, timestamp: '12 min ago' },
  { id: 5, name: 'Code Generation', type: 'inference', duration: '5.2s', status: 'success' as const, timestamp: '15 min ago' }
]

// Sparkline component
const Sparkline: React.FC<{ data: number[], color: string }> = ({ data, color }) => {
  const width = 60
  const height = 20
  const max = Math.max(...data)
  const min = Math.min(...data)
  const range = max - min || 1

  const points = data.map((value, index) => {
    const x = (index / (data.length - 1)) * width
    const y = height - ((value - min) / range) * height
    return `${x},${y}`
  }).join(' ')

  return (
    <svg width={width} height={height} className="overflow-visible">
      <motion.polyline
        fill="none"
        stroke={color}
        strokeWidth="1.5"
        points={points}
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ duration: 1, ease: "easeInOut" }}
      />
    </svg>
  )
}

// Animated counter
const AnimatedCounter: React.FC<{ value: number, format?: (n: number) => string }> = ({ 
  value, 
  format = (n) => n.toString() 
}) => {
  const [displayValue, setDisplayValue] = useState(0)

  useEffect(() => {
    const duration = 1000
    const steps = 30
    const increment = value / steps
    let current = 0
    
    const timer = setInterval(() => {
      current += increment
      if (current >= value) {
        setDisplayValue(value)
        clearInterval(timer)
      } else {
        setDisplayValue(Math.floor(current))
      }
    }, duration / steps)

    return () => clearInterval(timer)
  }, [value])

  return <span>{format(displayValue)}</span>
}

interface MetricCardProps {
  title: string
  value: number
  change: number
  trend: 'up' | 'down'
  icon: React.ElementType
  format?: (n: number) => string
  onClick: () => void
}

const MetricCard: React.FC<MetricCardProps> = ({ 
  title, 
  value, 
  change, 
  trend, 
  icon: Icon, 
  format,
  onClick 
}) => {
  const sparklineData = Array.from({ length: 12 }, () => Math.random() * 100)
  const isPositive = (trend === 'up' && change > 0) || (trend === 'down' && change < 0)

  return (
    <motion.div
      whileHover={{ y: -2 }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: "spring", stiffness: 400, damping: 25 }}
    >
      <Card 
        className="cursor-pointer bg-card hover:bg-card/80 border-border hover:border-ring/20 transition-all duration-200 group"
        onClick={onClick}
      >
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground group-hover:text-foreground transition-colors">
            {title}
          </CardTitle>
          <Icon className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors" />
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div>
              <div className="text-2xl font-bold text-foreground">
                <AnimatedCounter value={value} format={format} />
              </div>
              <div className="flex items-center space-x-1 mt-1">
                {isPositive ? (
                  <TrendingUp className="h-3 w-3 text-emerald-500" />
                ) : (
                  <TrendingDown className="h-3 w-3 text-red-500" />
                )}
                <Badge 
                  variant="secondary" 
                  className={`text-xs ${isPositive ? 'text-emerald-400 bg-emerald-500/10' : 'text-red-400 bg-red-500/10'}`}
                >
                  {change > 0 ? '+' : ''}{change}%
                </Badge>
              </div>
            </div>
            <div className="opacity-100 transition-opacity">
              <Sparkline 
                data={sparklineData} 
                color={isPositive ? 'rgb(34, 197, 94)' : 'rgb(239, 68, 68)'} 
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

const StatusBadge: React.FC<{ status: 'success' | 'error' | 'running' }> = ({ status }) => {
  const variants = {
    success: { icon: CheckCircle2, className: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' },
    error: { icon: XCircle, className: 'bg-red-500/10 text-red-400 border-red-500/20' },
    running: { icon: AlertCircle, className: 'bg-amber-500/10 text-amber-400 border-amber-500/20' }
  }
  
  const { icon: StatusIcon, className } = variants[status]
  
  return (
    <Badge variant="outline" className={`capitalize ${className}`}>
      <StatusIcon className="w-3 h-3 mr-1" />
      {status}
    </Badge>
  )
}

export default function DashboardPanel() {
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [environment, setEnvironment] = useState('prod')
  const [selectedMetric, setSelectedMetric] = useState<string | null>(null)
  const [hoveredRow, setHoveredRow] = useState<number | null>(null)

  // Simulate loading
  useEffect(() => {
    const timer = setTimeout(() => setIsLoading(false), 1500)
    return () => clearTimeout(timer)
  }, [])

  const filteredActivities = useMemo(() => {
    return mockActivities.filter(activity =>
      activity.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      activity.type.toLowerCase().includes(searchQuery.toLowerCase())
    )
  }, [searchQuery])

  const metricDetails = {
    'Active Models': {
      description: 'Currently deployed and active models across all environments',
      chartData: Array.from({ length: 24 }, (_, i) => ({ 
        time: `${i}:00`, 
        value: Math.floor(Math.random() * 30) + 15 
      }))
    },
    'Throughput': {
      description: 'Requests processed per minute across all model endpoints',
      chartData: Array.from({ length: 24 }, (_, i) => ({ 
        time: `${i}:00`, 
        value: Math.floor(Math.random() * 2000) + 800 
      }))
    },
    'Avg Latency': {
      description: 'Average response time for inference requests',
      chartData: Array.from({ length: 24 }, (_, i) => ({ 
        time: `${i}:00`, 
        value: Math.floor(Math.random() * 150) + 50 
      }))
    },
    'Daily Cost': {
      description: 'Compute and infrastructure costs for model operations',
      chartData: Array.from({ length: 24 }, (_, i) => ({ 
        time: `${i}:00`, 
        value: Math.floor(Math.random() * 500) + 200 
      }))
    }
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        {/* Control Bar Skeleton */}
        <div className="flex flex-col sm:flex-row gap-4 p-4 bg-card rounded-lg border">
          <Skeleton className="h-10 w-full sm:w-48" />
          <Skeleton className="h-10 w-full sm:w-32" />
          <Skeleton className="h-10 flex-1" />
          <Skeleton className="h-10 w-40" />
        </div>

        {/* Metrics Grid Skeleton */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <Card key={i}>
              <CardHeader className="pb-2">
                <Skeleton className="h-4 w-24" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-8 w-16 mb-2" />
                <Skeleton className="h-4 w-20" />
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Table Skeleton */}
        <Card>
          <CardHeader>
            <Skeleton className="h-6 w-32" />
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className="flex items-center space-x-4">
                  <Skeleton className="h-4 w-4" />
                  <Skeleton className="h-4 flex-1" />
                  <Skeleton className="h-4 w-20" />
                  <Skeleton className="h-4 w-16" />
                  <Skeleton className="h-6 w-16" />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Control Bar */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col sm:flex-row gap-4 p-4 bg-card rounded-lg border border-border"
      >
        <div className="flex items-center space-x-2">
          <Calendar className="h-4 w-4 text-muted-foreground" />
          <Button variant="outline" size="sm" className="justify-start">
            Last 7 days
            <ChevronDown className="ml-2 h-4 w-4" />
          </Button>
        </div>

        <Select value={environment} onValueChange={setEnvironment}>
          <SelectTrigger className="w-full sm:w-32">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="dev">Dev</SelectItem>
            <SelectItem value="prod">Prod</SelectItem>
          </SelectContent>
        </Select>

        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search activities..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>

        <Button className="bg-primary hover:bg-primary/90 text-primary-foreground">
          <ExternalLink className="mr-2 h-4 w-4" />
          Open Full Dashboard
        </Button>
      </motion.div>

      {/* Metrics Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
      >
        <MetricCard
          title="Active Models"
          value={mockMetrics.activeModels.value}
          change={mockMetrics.activeModels.change}
          trend={mockMetrics.activeModels.trend}
          icon={Server}
          onClick={() => setSelectedMetric('Active Models')}
        />
        <MetricCard
          title="Throughput"
          value={mockMetrics.throughput.value}
          change={mockMetrics.throughput.change}
          trend={mockMetrics.throughput.trend}
          icon={Activity}
          format={(n) => `${n}/min`}
          onClick={() => setSelectedMetric('Throughput')}
        />
        <MetricCard
          title="Avg Latency"
          value={mockMetrics.latency.value}
          change={mockMetrics.latency.change}
          trend={mockMetrics.latency.trend}
          icon={Clock}
          format={(n) => `${n}ms`}
          onClick={() => setSelectedMetric('Avg Latency')}
        />
        <MetricCard
          title="Daily Cost"
          value={mockMetrics.cost.value}
          change={mockMetrics.cost.change}
          trend={mockMetrics.cost.trend}
          icon={DollarSign}
          format={(n) => `$${n.toFixed(2)}`}
          onClick={() => setSelectedMetric('Daily Cost')}
        />
      </motion.div>

      {/* Activity Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Zap className="mr-2 h-5 w-5" />
              Recent Activity
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-1">
              {filteredActivities.map((activity, index) => (
                <motion.div
                  key={activity.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="flex items-center justify-between p-3 rounded-lg hover:bg-muted/50 transition-colors group cursor-pointer"
                  onMouseEnter={() => setHoveredRow(activity.id)}
                  onMouseLeave={() => setHoveredRow(null)}
                >
                  <div className="flex items-center space-x-3 flex-1">
                    <div className="flex-shrink-0">
                      {activity.type === 'inference' ? (
                        <Play className="h-4 w-4 text-primary" />
                      ) : (
                        <RotateCcw className="h-4 w-4 text-amber-500" />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-foreground truncate">
                        {activity.name}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {activity.type} • {activity.duration} • {activity.timestamp}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <StatusBadge status={activity.status} />
                    
                    <AnimatePresence>
                      {hoveredRow === activity.id && (
                        <motion.div
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          exit={{ opacity: 0, scale: 0.8 }}
                          className="flex items-center space-x-1"
                        >
                          <Button size="sm" variant="ghost" className="h-7 w-7 p-0">
                            <Eye className="h-3 w-3" />
                          </Button>
                          <Button size="sm" variant="ghost" className="h-7 w-7 p-0">
                            <RotateCcw className="h-3 w-3" />
                          </Button>
                          <Button size="sm" variant="ghost" className="h-7 w-7 p-0">
                            <MoreHorizontal className="h-3 w-3" />
                          </Button>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Metric Detail Modal */}
      <Dialog open={!!selectedMetric} onOpenChange={() => setSelectedMetric(null)}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>{selectedMetric || 'Metric Details'}</DialogTitle>
          </DialogHeader>
          
          <AnimatePresence mode="wait">
            {selectedMetric && (
              <motion.div
                key={selectedMetric}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                <p className="text-muted-foreground">
                  {metricDetails[selectedMetric as keyof typeof metricDetails]?.description}
                </p>
                
                <div className="h-64 bg-muted/20 rounded-lg flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-4xl font-bold text-primary mb-2">
                      {selectedMetric === 'Active Models' && mockMetrics.activeModels.value}
                      {selectedMetric === 'Throughput' && `${mockMetrics.throughput.value}/min`}
                      {selectedMetric === 'Avg Latency' && `${mockMetrics.latency.value}ms`}
                      {selectedMetric === 'Daily Cost' && `$${mockMetrics.cost.value}`}
                    </div>
                    <p className="text-muted-foreground">Detailed chart would go here</p>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </DialogContent>
      </Dialog>
    </div>
  )
}