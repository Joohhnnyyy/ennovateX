"use client";

import React from 'react';
import { motion } from 'framer-motion';
import NavBar from "@/components/NavBar"

import { Zap, Brain, Shield, Sparkles, Globe, Rocket, BarChart3, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const products = [
  {
    id: 'ai-platform',
    name: 'AI Platform',
    description: 'Advanced artificial intelligence platform for enterprise automation and insights.',
    icon: Brain,
    features: ['Machine Learning', 'Natural Language Processing', 'Computer Vision', 'Predictive Analytics'],
    availability: 'Available in Demo',
    badge: 'Most Popular'
  },
  {
    id: 'security-suite',
    name: 'Security Suite',
    description: 'Comprehensive security solution with SOC2 compliance and enterprise-grade protection.',
    icon: Shield,
    features: ['End-to-End Encryption', 'SOC2 Compliance', 'Threat Detection', 'Access Control'],
    availability: 'Available in Demo',
    badge: 'Enterprise'
  },
  {
    id: 'analytics-pro',
    name: 'Analytics Pro',
    description: 'Real-time analytics and business intelligence platform for data-driven decisions.',
    icon: BarChart3,
    features: ['Real-time Dashboards', 'Custom Reports', 'Data Visualization', 'API Integration'],
    availability: 'Available in Demo',
    badge: 'New'
  },
  {
    id: 'collaboration-hub',
    name: 'Collaboration Hub',
    description: 'Team collaboration platform with integrated communication and project management.',
    icon: Users,
    features: ['Team Chat', 'Project Management', 'File Sharing', 'Video Conferencing'],
    availability: 'Available in Demo',
    badge: null
  },
  {
    id: 'global-infrastructure',
    name: 'Global Infrastructure',
    description: 'Worldwide infrastructure with auto-scaling and high availability.',
    icon: Globe,
    features: ['Global CDN', 'Auto-scaling', '99.9% Uptime', 'Multi-region Deployment'],
    availability: 'Available in Demo',
    badge: null
  },
  {
    id: 'deployment-engine',
    name: 'Deployment Engine',
    description: 'One-click deployment automation with CI/CD integration.',
    icon: Rocket,
    features: ['One-click Deploy', 'CI/CD Integration', 'Rollback Support', 'Environment Management'],
    availability: 'Available in Demo',
    badge: null
  }
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.5
    }
  }
};

export default function ProductsPage() {
  return (
    <div className="min-h-screen bg-background">

      
      {/* Floating Navigation */}
      <NavBar />
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent mb-6">
              Our Products
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-8">
              Discover our comprehensive suite of AI-powered solutions designed to transform your business operations and drive innovation.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Products Grid */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
          >
            {products.map((product) => {
              const IconComponent = product.icon;
              return (
                <motion.div key={product.id} variants={itemVariants}>
                  <Card className="h-full hover:shadow-lg transition-shadow duration-300 border-border/50 hover:border-primary/20">
                    <CardHeader>
                      <div className="flex items-center justify-between mb-4">
                        <div className="p-3 rounded-lg bg-primary/10">
                          <IconComponent className="h-6 w-6 text-primary" />
                        </div>
                        {product.badge && (
                          <Badge variant={product.badge === 'Most Popular' ? 'default' : 'secondary'}>
                            {product.badge}
                          </Badge>
                        )}
                      </div>
                      <CardTitle className="text-xl font-semibold">{product.name}</CardTitle>
                      <CardDescription className="text-muted-foreground">
                        {product.description}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div>
                          <h4 className="font-medium mb-2">Key Features:</h4>
                          <ul className="space-y-1">
                            {product.features.map((feature, index) => (
                              <li key={index} className="text-sm text-muted-foreground flex items-center">
                                <Sparkles className="h-3 w-3 text-primary mr-2" />
                                {feature}
                              </li>
                            ))}
                          </ul>
                        </div>
                        <div className="pt-4 border-t border-border/50">
                          <p className="text-lg font-semibold text-primary mb-4">{product.availability}</p>
                          <div className="space-y-2">
                            <Button className="w-full" size="sm">
                              Get Started
                            </Button>
                            <Button variant="outline" className="w-full" size="sm">
                              Learn More
                            </Button>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              Ready to Transform Your Business?
            </h2>
            <p className="text-xl text-muted-foreground mb-8">
              Join thousands of companies already using our AI-powered solutions to drive innovation and growth.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90">
                <Zap className="h-5 w-5 mr-2" />
                Start Free Trial
              </Button>
              <Button variant="outline" size="lg">
                Schedule Demo
              </Button>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}