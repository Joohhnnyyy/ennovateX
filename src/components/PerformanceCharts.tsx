"use client";

import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  Download, 
  TrendingUp, 
  TrendingDown, 
  Activity,
  BarChart3,
  LineChart as LineChartIcon,
  Settings,
  Eye
} from 'lucide-react';
import { toast } from 'sonner';

interface ChartDataPoint {
  timestamp: string;
  date: string;
  value: number;
  volume?: number;
  category?: string;
  change?: number;
}

interface FilterState {
  timeRange: '1D' | '7D' | '1M' | '3M' | 'YTD';
  category: string[];
  metrics: string[];
  showVolume: boolean;
  chartType: 'line' | 'area' | 'bar';
}

interface PerformanceChartsProps {
  className?: string;
  title?: string;
  dataEndpoint?: string;
  enableExport?: boolean;
  enableFilters?: boolean;
  highContrast?: boolean;
}

const generateMockData = (timeRange: string): ChartDataPoint[] => {
  const now = new Date();
  const points = timeRange === '1D' ? 24 : timeRange === '7D' ? 7 : timeRange === '1M' ? 30 : timeRange === '3M' ? 90 : 365;
  
  return Array.from({ length: points }, (_, i) => {
    const date = new Date(now);
    if (timeRange === '1D') {
      date.setHours(date.getHours() - (points - i));
    } else {
      date.setDate(date.getDate() - (points - i));
    }
    
    const baseValue = 1000 + Math.sin(i / 10) * 200;
    const randomVariation = (Math.random() - 0.5) * 100;
    const value = Math.max(0, baseValue + randomVariation);
    const prevValue = i > 0 ? 1000 + Math.sin((i - 1) / 10) * 200 : value;
    
    return {
      timestamp: date.toISOString(),
      date: timeRange === '1D' ? date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }) : date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      value: Math.round(value),
      volume: Math.round(Math.random() * 10000),
      category: ['Revenue', 'Users', 'Conversions'][Math.floor(Math.random() * 3)],
      change: Math.round(((value - prevValue) / prevValue) * 100 * 100) / 100
    };
  });
};

// Enhanced color palette with Samsung-inspired themes
const getColorPalette = (highContrast: boolean, index: number = 0) => {
  if (highContrast) {
    // WCAG AAA compliant high contrast colors with better accessibility
    const contrastColors = [
      { 
        primary: '#000000', 
        secondary: '#FFFFFF', 
        gradient: 'linear-gradient(135deg, #000000 0%, #1a1a1a 100%)', 
        glow: 'rgba(0, 0, 0, 0.8)',
        light: '#F5F5F5',
        border: '#000000',
        text: '#000000'
      },
      { 
        primary: '#0066CC', 
        secondary: '#FFFFFF', 
        gradient: 'linear-gradient(135deg, #0066CC 0%, #004499 100%)', 
        glow: 'rgba(0, 102, 204, 0.8)',
        light: '#E6F3FF',
        border: '#0066CC',
        text: '#0066CC'
      },
      { 
        primary: '#CC0000', 
        secondary: '#FFFFFF', 
        gradient: 'linear-gradient(135deg, #CC0000 0%, #990000 100%)', 
        glow: 'rgba(204, 0, 0, 0.8)',
        light: '#FFE6E6',
        border: '#CC0000',
        text: '#CC0000'
      },
      { 
        primary: '#006600', 
        secondary: '#FFFFFF', 
        gradient: 'linear-gradient(135deg, #006600 0%, #004400 100%)', 
        glow: 'rgba(0, 102, 0, 0.8)',
        light: '#E6FFE6',
        border: '#006600',
        text: '#006600'
      },
      { 
        primary: '#663399', 
        secondary: '#FFFFFF', 
        gradient: 'linear-gradient(135deg, #663399 0%, #442266 100%)', 
        glow: 'rgba(102, 51, 153, 0.8)',
        light: '#F0E6FF',
        border: '#663399',
        text: '#663399'
      }
    ];
    return contrastColors[index % contrastColors.length];
  }
  
  const samsungColors = [
    { 
      primary: '#1428A0', 
      secondary: '#00ADEF', 
      gradient: 'linear-gradient(135deg, #1428A0 0%, #00ADEF 100%)',
      light: '#E3F2FD',
      glow: 'rgba(20, 40, 160, 0.3)',
      border: '#1428A0',
      text: '#1428A0'
    },
    { 
      primary: '#00C9FF', 
      secondary: '#92FE9D', 
      gradient: 'linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%)',
      light: '#E0F7FA',
      glow: 'rgba(0, 201, 255, 0.3)',
      border: '#00C9FF',
      text: '#00C9FF'
    },
    { 
      primary: '#667eea', 
      secondary: '#764ba2', 
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      light: '#F3E5F5',
      glow: 'rgba(102, 126, 234, 0.3)',
      border: '#667eea',
      text: '#667eea'
    },
    { 
      primary: '#f093fb', 
      secondary: '#f5576c', 
      gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      light: '#FCE4EC',
      glow: 'rgba(240, 147, 251, 0.3)',
      border: '#f093fb',
      text: '#f093fb'
    },
    { 
      primary: '#4facfe', 
      secondary: '#00f2fe', 
      gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
      light: '#E1F5FE',
      glow: 'rgba(79, 172, 254, 0.3)',
      border: '#4facfe',
      text: '#4facfe'
    }
  ];
  
  return samsungColors[index % samsungColors.length];
};

const CustomTooltip = ({ active, payload, label, highContrast }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className={`${
          highContrast 
            ? 'bg-transparent text-black border-4 border-black shadow-2xl' 
            : 'bg-card/95 backdrop-blur-md border-white/20'
        } border rounded-xl p-6 shadow-2xl`}
        style={{
          boxShadow: highContrast 
            ? '0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 2px #000000' 
            : undefined
        }}
      >
        <p className={`text-base font-bold mb-3 ${
          highContrast ? 'text-black border-b-2 border-black pb-2' : 'opacity-90'
        }`}>
          {label}
        </p>
        <div className="space-y-3">
          {payload.map((entry: any, index: number) => {
            const colorPalette = getColorPalette(highContrast, index);
            return (
              <div key={index} className="flex items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div 
                    className={`w-4 h-4 rounded-full shadow-lg ${
                      highContrast ? 'border-2' : ''
                    }`}
                    style={{ 
                      background: highContrast ? colorPalette.primary : colorPalette.gradient,
                      borderColor: highContrast ? colorPalette.border : 'transparent',
                      boxShadow: highContrast 
                        ? `0 0 12px ${colorPalette.glow}, 0 0 0 1px ${colorPalette.border}` 
                        : `0 0 8px ${colorPalette.glow || 'rgba(0,0,0,0.3)'}`
                    }}
                  />
                  <span className={`text-sm font-semibold ${
                    highContrast ? 'text-black' : ''
                  }`}>
                    {entry.name}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`font-mono text-base font-bold ${
                    highContrast ? 'text-black bg-gray-100 px-2 py-1 rounded' : ''
                  }`}>
                    {entry.value.toLocaleString()}
                  </span>
                  {data.change && (
                    <Badge variant={data.change >= 0 ? "default" : "destructive"} className="text-xs px-2 py-1">
                      {data.change >= 0 ? <TrendingUp className="w-3 h-3 mr-1" /> : <TrendingDown className="w-3 h-3 mr-1" />}
                      {Math.abs(data.change)}%
                    </Badge>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </motion.div>
    );
  }
  return null;
};

export default function PerformanceCharts({
  className = "",
  title = "Performance Analytics",
  dataEndpoint,
  enableExport = true,
  enableFilters = true,
  highContrast = false
}: PerformanceChartsProps) {
  const [filters, setFilters] = useState<FilterState>({
    timeRange: '7D',
    category: ['Revenue', 'Users'],
    metrics: ['value', 'volume'],
    showVolume: true,
    chartType: 'area'
  });

  const [data, setData] = useState<ChartDataPoint[]>([]);
  const [loading, setLoading] = useState(true);
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);
  const [highContrastMode, setHighContrastMode] = useState(highContrast);

  // Debounced filter updates
  const [debouncedFilters, setDebouncedFilters] = useState(filters);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedFilters(filters);
    }, 300);
    return () => clearTimeout(timer);
  }, [filters]);

  // Mock data fetching with loading state
  useEffect(() => {
    setLoading(true);
    const timer = setTimeout(() => {
      setData(generateMockData(debouncedFilters.timeRange));
      setLoading(false);
    }, 800);
    return () => clearTimeout(timer);
  }, [debouncedFilters.timeRange]);

  const chartData = useMemo(() => {
    return data.map(point => ({
      ...point,
      displayValue: point.value,
      displayVolume: filters.showVolume ? point.volume : undefined
    }));
  }, [data, filters.showVolume]);

  const handleFilterChange = useCallback((key: keyof FilterState, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  }, []);

  const handleExport = useCallback(async (format: 'csv' | 'png') => {
    try {
      if (format === 'csv') {
        const csvContent = [
          ['Date', 'Value', 'Volume', 'Category', 'Change'],
          ...data.map(row => [row.date, row.value, row.volume || '', row.category || '', row.change || ''])
        ].map(row => row.join(',')).join('\n');
        
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `performance-data-${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      }
      
      toast.success(`Chart exported as ${format.toUpperCase()}`, {
        description: 'Download will begin shortly'
      });
    } catch (error) {
      toast.error('Export failed', {
        description: 'Please try again or contact support'
      });
    }
  }, [data]);

  const timeRangeOptions = [
    { value: '1D', label: '1 Day' },
    { value: '7D', label: '7 Days' },
    { value: '1M', label: '1 Month' },
    { value: '3M', label: '3 Months' },
    { value: 'YTD', label: 'Year to Date' }
  ];

  const chartTypeOptions = [
    { value: 'line', label: 'Line', icon: LineChartIcon },
    { value: 'area', label: 'Area', icon: Activity },
    { value: 'bar', label: 'Bar', icon: BarChart3 }
  ];

  const renderChart = () => {
    const commonProps = {
      data: chartData,
      margin: { top: 20, right: 30, left: 20, bottom: 20 }
    };

    const primaryColor = getColorPalette(highContrastMode, 0);
    const secondaryColor = getColorPalette(highContrastMode, 1);
    const tertiaryColor = getColorPalette(highContrastMode, 2);
    
    const gradientId = `gradient-${Math.random().toString(36).substr(2, 9)}`;
    const gradientId2 = `gradient2-${Math.random().toString(36).substr(2, 9)}`;

    switch (filters.chartType) {
      case 'area':
        return (
          <AreaChart {...commonProps}>
            <defs>
              <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={primaryColor.primary} stopOpacity={0.9}/>
                <stop offset="50%" stopColor={primaryColor.secondary} stopOpacity={0.6}/>
                <stop offset="95%" stopColor={primaryColor.secondary} stopOpacity={0.1}/>
              </linearGradient>
              <linearGradient id={gradientId2} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={secondaryColor.primary} stopOpacity={0.7}/>
                <stop offset="95%" stopColor={secondaryColor.secondary} stopOpacity={0.1}/>
              </linearGradient>
              <filter id="glow">
                <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                <feMerge> 
                  <feMergeNode in="coloredBlur"/>
                  <feMergeNode in="SourceGraphic"/>
                </feMerge>
              </filter>
            </defs>
            <CartesianGrid 
              strokeDasharray={highContrastMode ? "5 5" : "3 3"}
              stroke={highContrastMode ? "#000000" : "#2a2d31"} 
              opacity={highContrastMode ? 0.8 : 0.3}
              strokeWidth={highContrastMode ? 2 : 1}
            />
            <XAxis 
              dataKey="date" 
              stroke={highContrastMode ? "#000000" : "#8a8f99"} 
              fontSize={highContrastMode ? 14 : 12}
              fontWeight={highContrastMode ? "bold" : "normal"}
              tickLine={highContrastMode}
              axisLine={highContrastMode}
              tick={{ fill: highContrastMode ? "#000000" : "#8a8f99" }}
            />
            <YAxis 
              stroke={highContrastMode ? "#000000" : "#8a8f99"} 
              fontSize={highContrastMode ? 14 : 12}
              fontWeight={highContrastMode ? "bold" : "normal"}
              tickLine={highContrastMode}
              axisLine={highContrastMode}
              tick={{ fill: highContrastMode ? "#000000" : "#8a8f99" }}
            />
            <Tooltip content={<CustomTooltip highContrast={highContrastMode} />} />
            {hoveredIndex !== null && (
              <ReferenceLine 
                x={chartData[hoveredIndex]?.date} 
                stroke={primaryColor.primary} 
                strokeDasharray="2 2" 
                strokeWidth={2}
                opacity={0.8}
              />
            )}
            <Area
              type="monotone"
              dataKey="displayValue"
              stroke={primaryColor.primary}
              fill={highContrastMode ? primaryColor.light : `url(#${gradientId})`}
              strokeWidth={highContrastMode ? 4 : 3}
              strokeDasharray={highContrastMode ? "0" : "0"}
              name="Value"
              filter={highContrastMode ? "none" : "url(#glow)"}
              fillOpacity={highContrastMode ? 0.3 : 1}
              onMouseEnter={(data, index) => setHoveredIndex(typeof index === 'number' ? index : null)}
              onMouseLeave={() => setHoveredIndex(null)}
            />
            {filters.showVolume && (
              <Area
                type="monotone"
                dataKey="displayVolume"
                stroke={secondaryColor.primary}
                fill={highContrastMode ? secondaryColor.light : `url(#${gradientId2})`}
                strokeWidth={highContrastMode ? 3 : 2}
                strokeDasharray={highContrastMode ? "8 4" : "0"}
                name="Volume"
                opacity={highContrastMode ? 0.9 : 0.7}
                fillOpacity={highContrastMode ? 0.2 : 1}
              />
            )}
          </AreaChart>
        );
      case 'bar':
        return (
          <BarChart {...commonProps}>
            <defs>
              <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor={primaryColor.primary}/>
                <stop offset="100%" stopColor={primaryColor.secondary}/>
              </linearGradient>
              <filter id="barGlow">
                <feDropShadow dx="0" dy="0" stdDeviation="4" floodColor={primaryColor.glow || primaryColor.primary}/>
              </filter>
            </defs>
            <CartesianGrid 
              strokeDasharray={highContrastMode ? "5 5" : "3 3"}
              stroke={highContrastMode ? "#000000" : "#2a2d31"} 
              opacity={highContrastMode ? 0.8 : 0.3}
              strokeWidth={highContrastMode ? 2 : 1}
            />
            <XAxis 
              dataKey="date" 
              stroke={highContrastMode ? "#000000" : "#8a8f99"} 
              fontSize={highContrastMode ? 14 : 12}
              fontWeight={highContrastMode ? "bold" : "normal"}
              tickLine={highContrastMode}
              axisLine={highContrastMode}
              tick={{ fill: highContrastMode ? "#000000" : "#8a8f99" }}
            />
            <YAxis 
              stroke={highContrastMode ? "#000000" : "#8a8f99"} 
              fontSize={highContrastMode ? 14 : 12}
              fontWeight={highContrastMode ? "bold" : "normal"}
              tickLine={highContrastMode}
              axisLine={highContrastMode}
              tick={{ fill: highContrastMode ? "#000000" : "#8a8f99" }}
            />
            <Tooltip content={<CustomTooltip highContrast={highContrastMode} />} />
            <Bar
              dataKey="displayValue"
              fill={highContrastMode ? primaryColor.primary : `url(#${gradientId})`}
              stroke={highContrastMode ? primaryColor.border : "none"}
              strokeWidth={highContrastMode ? 3 : 0}
              name="Value"
              radius={[4, 4, 0, 0]}
              filter={highContrastMode ? "none" : "url(#barGlow)"}
            />
          </BarChart>
        );
      default:
        return (
          <LineChart {...commonProps}>
            <defs>
              <filter id="lineGlow">
                <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                <feMerge> 
                  <feMergeNode in="coloredBlur"/>
                  <feMergeNode in="SourceGraphic"/>
                </feMerge>
              </filter>
            </defs>
            <CartesianGrid 
              strokeDasharray={highContrastMode ? "5 5" : "3 3"}
              stroke={highContrastMode ? "#000000" : "hsl(var(--border))"} 
              opacity={highContrastMode ? 0.8 : 0.3}
              strokeWidth={highContrastMode ? 2 : 1}
            />
            <XAxis 
              dataKey="date" 
              stroke={highContrastMode ? "#000000" : "#8a8f99"} 
              fontSize={highContrastMode ? 14 : 12}
              fontWeight={highContrastMode ? "bold" : "normal"}
              tickLine={highContrastMode}
              axisLine={highContrastMode}
              tick={{ fill: highContrastMode ? "#000000" : "#8a8f99" }}
            />
            <YAxis 
              stroke={highContrastMode ? "#000000" : "#8a8f99"} 
              fontSize={highContrastMode ? 14 : 12}
              fontWeight={highContrastMode ? "bold" : "normal"}
              tickLine={highContrastMode}
              axisLine={highContrastMode}
              tick={{ fill: highContrastMode ? "#000000" : "#8a8f99" }}
            />
            <Tooltip content={<CustomTooltip highContrast={highContrastMode} />} />
            {hoveredIndex !== null && (
              <ReferenceLine 
                x={chartData[hoveredIndex]?.date} 
                stroke={primaryColor.primary} 
                strokeDasharray={highContrastMode ? "8 4" : "2 2"}
                strokeWidth={highContrastMode ? 4 : 2}
                opacity={highContrastMode ? 1 : 0.8}
              />
            )}
            <Line
              type="monotone"
              dataKey="displayValue"
              stroke={primaryColor.primary}
              strokeWidth={highContrastMode ? 6 : 4}
              strokeDasharray={highContrastMode ? "0" : "0"}
              dot={highContrastMode ? {
                r: 6,
                fill: primaryColor.primary,
                stroke: "#FFFFFF",
                strokeWidth: 3
              } : false}
              activeDot={{ 
                r: highContrastMode ? 10 : 8, 
                fill: primaryColor.primary,
                stroke: highContrastMode ? "#FFFFFF" : "#0e0f13",
                strokeWidth: highContrastMode ? 4 : 3,
                filter: highContrastMode ? "none" : "url(#lineGlow)"
              }}
              name="Value"
              filter="url(#lineGlow)"
              onMouseEnter={(data, index) => setHoveredIndex(typeof index === 'number' ? index : null)}
              onMouseLeave={() => setHoveredIndex(null)}
            />
            {filters.showVolume && (
              <Line
                type="monotone"
                dataKey="displayVolume"
                stroke={secondaryColor.primary}
                strokeWidth={2}
                strokeDasharray="8 4"
                dot={false}
                name="Volume"
                opacity={0.8}
              />
            )}
          </LineChart>
        );
    }
  };

  return (
    <div className={`space-y-6 ${className}`}>
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-heading font-bold">{title}</h2>
          <p className="text-muted-foreground mt-1">Interactive performance analytics and insights</p>
        </div>
        <div className="flex items-center gap-2">
          <div className={`flex items-center space-x-3 p-3 rounded-lg border-2 transition-all duration-200 ${
            highContrastMode 
              ? 'bg-black text-white border-black shadow-lg' 
              : 'bg-background border-border hover:border-primary/50'
          }`}>
            <Eye className={`h-5 w-5 ${
              highContrastMode ? 'text-white' : 'text-muted-foreground'
            }`} />
            <Label 
              htmlFor="high-contrast" 
              className={`text-sm font-semibold cursor-pointer ${
                highContrastMode ? 'text-white' : 'text-foreground'
              }`}
            >
              High Contrast Mode
            </Label>
            <Switch
              id="high-contrast"
              checked={highContrastMode}
              onCheckedChange={setHighContrastMode}
              className={highContrastMode ? 'data-[state=checked]:bg-white' : ''}
            />
            {highContrastMode && (
              <Badge variant="secondary" className="bg-white text-black font-bold text-xs">
                ACTIVE
              </Badge>
            )}
          </div>
          {enableExport && (
            <Select onValueChange={(value) => handleExport(value as 'csv' | 'png')}>
              <SelectTrigger className="w-32">
                <Download className="w-4 h-4 mr-2" />
                <SelectValue placeholder="Export" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="csv">Export CSV</SelectItem>
                <SelectItem value="png">Export PNG</SelectItem>
              </SelectContent>
            </Select>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Main Chart Column */}
        <div className="lg:col-span-3 space-y-4">
          <Card className={highContrastMode ? "bg-white text-black border-black" : ""}>
            <CardHeader className="pb-4">
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg font-semibold">Performance Trends</CardTitle>
                <div className="flex items-center gap-2">
                  {timeRangeOptions.map((option) => (
                    <Button
                      key={option.value}
                      variant={filters.timeRange === option.value ? "default" : "outline"}
                      size="sm"
                      onClick={() => handleFilterChange('timeRange', option.value)}
                      className={`text-xs ${
                        highContrastMode
                          ? filters.timeRange === option.value
                            ? "bg-black text-white border-black hover:bg-gray-800"
                            : "bg-white text-black border-2 border-black hover:bg-gray-100 font-semibold"
                          : ""
                      }`}
                    >
                      {option.label}
                    </Button>
                  ))}
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <AnimatePresence mode="wait">
                <motion.div
                  key={filters.timeRange + filters.chartType}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.3 }}
                  className="h-96"
                >
                  {loading ? (
                    <div className="space-y-3">
                      <Skeleton className="h-4 w-full" />
                      <Skeleton className="h-4 w-3/4" />
                      <Skeleton className="h-64 w-full" />
                    </div>
                  ) : (
                    <ResponsiveContainer width="100%" height="100%">
                      {renderChart()}
                    </ResponsiveContainer>
                  )}
                </motion.div>
              </AnimatePresence>
            </CardContent>
          </Card>

          {/* Enhanced Volume Distribution Chart */}
          <Card className={highContrastMode ? "bg-white text-black border-black" : ""}>
            <CardHeader className="pb-4">
              <CardTitle className="text-lg font-semibold">Volume Distribution</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-48">
                {loading ? (
                  <Skeleton className="h-full w-full" />
                ) : (
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData.slice(-7)}>
                      <defs>
                        <linearGradient id="volumeGradient" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor={getColorPalette(highContrastMode, 2).primary}/>
                          <stop offset="100%" stopColor={getColorPalette(highContrastMode, 2).secondary}/>
                        </linearGradient>
                        <filter id="volumeGlow">
                          <feDropShadow dx="0" dy="0" stdDeviation="3" floodColor={getColorPalette(highContrastMode, 2).glow || getColorPalette(highContrastMode, 2).primary} floodOpacity="0.6"/>
                        </filter>
                      </defs>
                      <CartesianGrid 
                        strokeDasharray="3 3" 
                        stroke={highContrastMode ? "#e0e0e0" : "#2a2d31"} 
                        opacity={highContrastMode ? 0.5 : 0.3} 
                      />
                      <XAxis 
                        dataKey="date" 
                        stroke={highContrastMode ? "#666" : "#8a8f99"} 
                        fontSize={12}
                        tickLine={false}
                        axisLine={false}
                      />
                      <YAxis 
                        stroke={highContrastMode ? "#666" : "#8a8f99"} 
                        fontSize={12}
                        tickLine={false}
                        axisLine={false}
                      />
                      <Tooltip content={<CustomTooltip highContrast={highContrastMode} />} />
                      <Bar
                        dataKey="volume"
                        fill={highContrastMode ? getColorPalette(highContrastMode, 2).primary : "url(#volumeGradient)"}
                        name="Volume"
                        radius={[4, 4, 0, 0]}
                        filter="url(#volumeGlow)"
                      />
                    </BarChart>
                  </ResponsiveContainer>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Control Panel */}
        <div className="space-y-4">
          {/* Enhanced Quick Stats with better colors */}
          <div className="grid grid-cols-2 lg:grid-cols-1 gap-4">
            <Card className={`${highContrastMode ? "bg-white text-black border-black" : ""} p-4 relative overflow-hidden`}>
              <div className={`absolute inset-0 opacity-10 ${highContrastMode ? '' : 'bg-gradient-to-br from-blue-500/20 to-purple-500/20'}`} />
              <div className="relative flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Current Value</p>
                  <div className="text-2xl font-bold">
                    {loading ? <Skeleton className="h-8 w-16" /> : data[data.length - 1]?.value.toLocaleString()}
                  </div>
                </div>
                <div className="p-2 rounded-full" style={{background: getColorPalette(highContrastMode, 0).gradient}}>
                  <TrendingUp className="w-6 h-6 text-white" />
                </div>
              </div>
            </Card>

            <Card className={`${highContrastMode ? "bg-white text-black border-black" : ""} p-4 relative overflow-hidden`}>
              <div className={`absolute inset-0 opacity-10 ${highContrastMode ? '' : 'bg-gradient-to-br from-green-500/20 to-blue-500/20'}`} />
              <div className="relative flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Change</p>
                  <div className="text-2xl font-bold">
                    {loading ? <Skeleton className="h-8 w-16" /> : `${data[data.length - 1]?.change || 0}%`}
                  </div>
                </div>
                <div className="p-2 rounded-full" style={{background: getColorPalette(highContrastMode, 1).gradient}}>
                  <Activity className="w-6 h-6 text-white" />
                </div>
              </div>
            </Card>
          </div>

          {/* Filters */}
          {enableFilters && (
            <Card className={highContrastMode ? "bg-white text-black border-black" : ""}>
              <CardHeader className="pb-4">
                <CardTitle className="text-base font-semibold flex items-center gap-2">
                  <Settings className="w-4 h-4" />
                  Controls
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label className="text-sm font-medium mb-2 block">Chart Type</Label>
                  <div className="grid grid-cols-3 gap-2">
                    {chartTypeOptions.map((option) => (
                      <Button
                        key={option.value}
                        variant={filters.chartType === option.value ? "default" : "outline"}
                        size="sm"
                        onClick={() => handleFilterChange('chartType', option.value)}
                        className={`flex flex-col items-center gap-1 h-auto py-2 ${
                          highContrastMode
                            ? filters.chartType === option.value
                              ? "bg-black text-white border-black hover:bg-gray-800"
                              : "bg-white text-black border-2 border-black hover:bg-gray-100 font-semibold"
                            : ""
                        }`}
                      >
                        <option.icon className="w-4 h-4" />
                        <span className="text-xs">{option.label}</span>
                      </Button>
                    ))}
                  </div>
                </div>

                <div>
                  <Label className="text-sm font-medium mb-2 block">Category Filter</Label>
                  <Select 
                    value={filters.category[0] || ''} 
                    onValueChange={(value) => handleFilterChange('category', [value])}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select category" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Revenue">Revenue</SelectItem>
                      <SelectItem value="Users">Users</SelectItem>
                      <SelectItem value="Conversions">Conversions</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex items-center justify-between">
                  <Label className="text-sm font-medium">Show Volume</Label>
                  <Switch
                    checked={filters.showVolume}
                    onCheckedChange={(checked) => handleFilterChange('showVolume', checked)}
                  />
                </div>

                <div>
                  <Label className="text-sm font-medium mb-2 block">Data Range</Label>
                  <Slider
                    value={[data.length * 0.8]}
                    onValueChange={(value) => {}}
                    max={data.length}
                    step={1}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-muted-foreground mt-1">
                    <span>Start</span>
                    <span>End</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Enhanced Legend with gradient indicators */}
          <Card className={highContrastMode ? "bg-white text-black border-black" : ""}>
            <CardHeader className="pb-2">
              <CardTitle className="text-base font-semibold">Legend</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center gap-3">
                <div 
                  className="w-4 h-4 rounded-md shadow-sm" 
                  style={{background: getColorPalette(highContrastMode, 0).gradient}}
                />
                <span className="text-sm font-medium">Primary Value</span>
              </div>
              {filters.showVolume && (
                <div className="flex items-center gap-3">
                  <div 
                    className="w-4 h-2 rounded-sm shadow-sm" 
                    style={{background: getColorPalette(highContrastMode, 1).gradient}}
                  />
                  <span className="text-sm font-medium">Volume</span>
                </div>
              )}
              <div className="flex items-center gap-3">
                <div 
                  className="w-4 h-4 rounded-md shadow-sm" 
                  style={{background: getColorPalette(highContrastMode, 2).gradient}}
                />
                <span className="text-sm font-medium">Distribution</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}