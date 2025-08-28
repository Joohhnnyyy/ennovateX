"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import NavBar from "@/components/NavBar"

import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  Zap, 
  Brain, 
  Shield, 
  Bell, 
  Settings, 
  Search,
  Filter,
  Download,
  RefreshCw,
  ChevronDown,
  Activity,
  Database,
  Cpu,
  Globe
} from 'lucide-react';

interface MetricCard {
  title: string;
  value: string;
  change: string;
  trend: 'up' | 'down';
  icon: React.ReactNode;
}

interface ChartData {
  name: string;
  value: number;
  color: string;
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

const MetricCard: React.FC<MetricCard> = ({ title, value, change, trend, icon }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6 }}
    className="bg-card/50 backdrop-blur-xl rounded-2xl border border-border/50 p-6 shadow-lg hover:shadow-xl transition-all duration-300"
  >
    <div className="flex items-center justify-between mb-4">
      <div className="p-3 bg-primary/10 rounded-xl">
        {icon}
      </div>
      <div className={`flex items-center space-x-1 text-sm font-medium ${
        trend === 'up' ? 'text-green-500' : 'text-red-500'
      }`}>
        <TrendingUp className={`w-4 h-4 ${trend === 'down' ? 'rotate-180' : ''}`} />
        <span>{change}</span>
      </div>
    </div>
    <h3 className="text-2xl font-bold text-foreground mb-1">{value}</h3>
    <p className="text-muted-foreground text-sm">{title}</p>
  </motion.div>
);

const MiniChart: React.FC<{ data: ChartData[] }> = ({ data }) => (
  <div className="flex items-end space-x-1 h-16">
    {data.map((item, index) => (
      <motion.div
        key={index}
        initial={{ height: 0 }}
        animate={{ height: `${item.value}%` }}
        transition={{ duration: 0.8, delay: index * 0.1 }}
        className="flex-1 rounded-t-sm"
        style={{ backgroundColor: item.color }}
      />
    ))}
  </div>
);

export default function DashboardPage() {
  const [selectedTimeframe, setSelectedTimeframe] = useState('7d');
  const [searchQuery, setSearchQuery] = useState('');

  const metrics: MetricCard[] = [
    {
      title: 'Total AI Processes',
      value: '2,847',
      change: '+12.5%',
      trend: 'up',
      icon: <Brain className="w-6 h-6 text-primary" />
    },
    {
      title: 'Active Users',
      value: '1,234',
      change: '+8.2%',
      trend: 'up',
      icon: <Users className="w-6 h-6 text-primary" />
    },
    {
      title: 'System Performance',
      value: '98.7%',
      change: '+2.1%',
      trend: 'up',
      icon: <Activity className="w-6 h-6 text-primary" />
    },
    {
      title: 'Data Processed',
      value: '847 GB',
      change: '+15.3%',
      trend: 'up',
      icon: <Database className="w-6 h-6 text-primary" />
    }
  ];

  const chartData: ChartData[] = [
    { name: 'Mon', value: 65, color: '#1428A0' },
    { name: 'Tue', value: 78, color: '#1428A0' },
    { name: 'Wed', value: 90, color: '#00ADEF' },
    { name: 'Thu', value: 85, color: '#00ADEF' },
    { name: 'Fri', value: 95, color: '#1428A0' },
    { name: 'Sat', value: 70, color: '#00ADEF' },
    { name: 'Sun', value: 80, color: '#1428A0' }
  ];

  const recentActivities = [
    { id: 1, action: 'AI Model Training Completed', time: '2 minutes ago', status: 'success' },
    { id: 2, action: 'Data Pipeline Updated', time: '15 minutes ago', status: 'info' },
    { id: 3, action: 'Security Scan Completed', time: '1 hour ago', status: 'success' },
    { id: 4, action: 'System Backup Created', time: '2 hours ago', status: 'info' },
    { id: 5, action: 'Performance Alert Resolved', time: '3 hours ago', status: 'warning' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background/95 to-primary/5">

      
      {/* Floating Navigation */}
      <NavBar />
      {/* Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <FloatingElement delay={0.2} className="absolute top-20 right-20">
          <div className="p-4 bg-gradient-to-br from-primary/20 to-accent/20 rounded-2xl backdrop-blur-sm border border-white/10">
            <Zap className="w-8 h-8 text-primary" />
          </div>
        </FloatingElement>

        <FloatingElement delay={0.4} className="absolute top-40 left-20">
          <div className="p-4 bg-gradient-to-br from-accent/20 to-primary/20 rounded-2xl backdrop-blur-sm border border-white/10">
            <Shield className="w-8 h-8 text-accent" />
          </div>
        </FloatingElement>

        <FloatingElement delay={0.6} className="absolute bottom-40 right-32">
          <div className="p-4 bg-gradient-to-br from-[#00ADEF]/20 to-[#1428A0]/20 rounded-2xl backdrop-blur-sm border border-white/10">
            <Cpu className="w-8 h-8 text-[#00ADEF]" />
          </div>
        </FloatingElement>
      </div>

      <div className="relative z-10 container mx-auto px-6 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-12"
        >
          <div>
            <div className="mb-4">
              <svg 
                height="35" 
                width="140" 
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
              <div className="text-lg font-heading font-semibold text-primary">
                EnnovateX AI Dashboard
              </div>
            </div>
            <h1 className="text-4xl font-heading font-bold text-foreground mb-2">
              Welcome back, Admin
            </h1>
            <p className="text-muted-foreground">
              Monitor your AI platform performance and manage operations
            </p>
          </div>

          <div className="flex items-center space-x-4 mt-6 lg:mt-0">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 pr-4 py-2 bg-input/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200"
              />
            </div>
            <button className="p-2 bg-secondary hover:bg-secondary/80 rounded-xl transition-all duration-200">
              <Bell className="w-5 h-5 text-secondary-foreground" />
            </button>
            <button className="p-2 bg-secondary hover:bg-secondary/80 rounded-xl transition-all duration-200">
              <Settings className="w-5 h-5 text-secondary-foreground" />
            </button>
          </div>
        </motion.div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {metrics.map((metric, index) => (
            <motion.div
              key={metric.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
            >
              <MetricCard {...metric} />
            </motion.div>
          ))}
        </div>

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Performance Chart */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="lg:col-span-2"
          >
            <div className="bg-card/50 backdrop-blur-xl rounded-2xl border border-border/50 p-6 shadow-lg">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-heading font-bold text-foreground">
                  Performance Overview
                </h2>
                <div className="flex items-center space-x-2">
                  <select
                    value={selectedTimeframe}
                    onChange={(e) => setSelectedTimeframe(e.target.value)}
                    className="bg-input/50 border border-border rounded-lg px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                  >
                    <option value="7d">Last 7 days</option>
                    <option value="30d">Last 30 days</option>
                    <option value="90d">Last 90 days</option>
                  </select>
                  <button className="p-2 bg-secondary hover:bg-secondary/80 rounded-lg transition-all duration-200">
                    <RefreshCw className="w-4 h-4 text-secondary-foreground" />
                  </button>
                </div>
              </div>
              
              <div className="h-64 flex items-end justify-between space-x-2">
                {chartData.map((item, index) => (
                  <div key={item.name} className="flex-1 flex flex-col items-center">
                    <motion.div
                      initial={{ height: 0 }}
                      animate={{ height: `${item.value}%` }}
                      transition={{ duration: 0.8, delay: index * 0.1 }}
                      className="w-full rounded-t-lg mb-2"
                      style={{ backgroundColor: item.color, minHeight: '200px', maxHeight: '200px' }}
                    />
                    <span className="text-xs text-muted-foreground">{item.name}</span>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Recent Activity */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <div className="bg-card/50 backdrop-blur-xl rounded-2xl border border-border/50 p-6 shadow-lg">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-heading font-bold text-foreground">
                  Recent Activity
                </h2>
                <button className="text-primary hover:text-primary/80 text-sm font-medium">
                  View All
                </button>
              </div>
              
              <div className="space-y-4">
                {recentActivities.map((activity, index) => (
                  <motion.div
                    key={activity.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: index * 0.1 }}
                    className="flex items-start space-x-3 p-3 bg-secondary/20 rounded-lg"
                  >
                    <div className={`w-2 h-2 rounded-full mt-2 ${
                      activity.status === 'success' ? 'bg-green-500' :
                      activity.status === 'warning' ? 'bg-yellow-500' :
                      'bg-blue-500'
                    }`} />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-foreground">
                        {activity.action}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {activity.time}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>

        {/* System Status */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="mt-8"
        >
          <div className="bg-card/50 backdrop-blur-xl rounded-2xl border border-border/50 p-6 shadow-lg">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-heading font-bold text-foreground">
                System Status
              </h2>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full" />
                <span className="text-sm text-muted-foreground">All systems operational</span>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="flex items-center space-x-4 p-4 bg-secondary/20 rounded-lg">
                <div className="p-3 bg-green-500/20 rounded-xl">
                  <Globe className="w-6 h-6 text-green-500" />
                </div>
                <div>
                  <h3 className="font-semibold text-foreground">API Status</h3>
                  <p className="text-sm text-muted-foreground">99.9% uptime</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-4 p-4 bg-secondary/20 rounded-lg">
                <div className="p-3 bg-blue-500/20 rounded-xl">
                  <Database className="w-6 h-6 text-blue-500" />
                </div>
                <div>
                  <h3 className="font-semibold text-foreground">Database</h3>
                  <p className="text-sm text-muted-foreground">Healthy</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-4 p-4 bg-secondary/20 rounded-lg">
                <div className="p-3 bg-purple-500/20 rounded-xl">
                  <Cpu className="w-6 h-6 text-purple-500" />
                </div>
                <div>
                  <h3 className="font-semibold text-foreground">AI Models</h3>
                  <p className="text-sm text-muted-foreground">12 active</p>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.8 }}
          className="mt-8"
        >
          <div className="bg-gradient-to-r from-primary/10 to-accent/10 rounded-2xl p-6 border border-border/50">
            <h3 className="text-xl font-heading font-bold text-foreground mb-4">
              Quick Actions
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <button className="flex flex-col items-center space-y-2 p-4 bg-card/50 hover:bg-card/70 rounded-xl transition-all duration-200">
                <Brain className="w-8 h-8 text-primary" />
                <span className="text-sm font-medium text-foreground">Train Model</span>
              </button>
              <button className="flex flex-col items-center space-y-2 p-4 bg-card/50 hover:bg-card/70 rounded-xl transition-all duration-200">
                <Database className="w-8 h-8 text-primary" />
                <span className="text-sm font-medium text-foreground">Manage Data</span>
              </button>
              <button className="flex flex-col items-center space-y-2 p-4 bg-card/50 hover:bg-card/70 rounded-xl transition-all duration-200">
                <BarChart3 className="w-8 h-8 text-primary" />
                <span className="text-sm font-medium text-foreground">View Reports</span>
              </button>
              <button className="flex flex-col items-center space-y-2 p-4 bg-card/50 hover:bg-card/70 rounded-xl transition-all duration-200">
                <Settings className="w-8 h-8 text-primary" />
                <span className="text-sm font-medium text-foreground">Settings</span>
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}