import { Metadata } from 'next'
import { Zap, Clock, Globe, Cpu, BarChart3, CheckCircle } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Lightning Fast Performance | Ennovatex AI Platform',
  description: 'Experience sub-100ms response times with our optimized performance, edge computing, and intelligent caching solutions.',
}

export default function LightningFastPage() {
  const performanceMetrics = [
    {
      icon: Clock,
      title: 'Sub-100ms Response',
      description: 'Average API response time under 100 milliseconds',
      value: '<100ms'
    },
    {
      icon: Globe,
      title: 'Global CDN',
      description: 'Content delivered from 200+ edge locations worldwide',
      value: '200+ Locations'
    },
    {
      icon: Cpu,
      title: 'Edge Computing',
      description: 'Processing power closer to your users',
      value: '99.9% Uptime'
    },
    {
      icon: BarChart3,
      title: 'Smart Caching',
      description: 'Intelligent caching reduces load times by 80%',
      value: '80% Faster'
    }
  ]

  const features = [
    'Optimized database queries with intelligent indexing',
    'Advanced compression algorithms for faster data transfer',
    'Real-time performance monitoring and auto-optimization',
    'Predictive caching based on user behavior patterns',
    'Load balancing across multiple data centers',
    'HTTP/3 and QUIC protocol support for faster connections'
  ]

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <div className="flex items-center justify-center gap-3 mb-6">
              <div className="p-3 rounded-lg bg-primary/10">
                <Zap className="h-8 w-8 text-primary" />
              </div>
              <Badge variant="secondary" className="text-sm font-medium">
                99.9% Uptime Guaranteed
              </Badge>
            </div>
            <h1 className="text-4xl md:text-6xl font-heading font-bold text-foreground mb-6">
              Lightning Fast
              <span className="block bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                Performance
              </span>
            </h1>
            <p className="text-xl text-muted-foreground leading-relaxed max-w-3xl mx-auto mb-8">
              Experience blazing-fast performance with our optimized infrastructure, 
              edge computing, and intelligent caching that delivers sub-100ms response times globally.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild>
                <Link href="/demo">Try Live Demo</Link>
              </Button>
              <Button variant="outline" size="lg" asChild>
                <Link href="/demo">Try Demo</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Performance Metrics */}
      <section className="py-16 px-6 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-foreground mb-4">
              Performance That Speaks for Itself
            </h2>
            <p className="text-lg text-muted-foreground">
              Real metrics from our global infrastructure
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {performanceMetrics.map((metric, index) => {
              const IconComponent = metric.icon
              return (
                <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                  <CardHeader className="pb-4">
                    <div className="mx-auto p-3 rounded-lg bg-primary/10 w-fit mb-4">
                      <IconComponent className="h-6 w-6 text-primary" />
                    </div>
                    <CardTitle className="text-2xl font-bold text-primary">
                      {metric.value}
                    </CardTitle>
                    <CardDescription className="font-semibold">
                      {metric.title}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">
                      {metric.description}
                    </p>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-heading font-bold text-foreground mb-6">
                Built for Speed
              </h2>
              <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
                Our platform is engineered from the ground up for maximum performance. 
                Every component is optimized to deliver the fastest possible experience.
              </p>
              <div className="space-y-4">
                {features.map((feature, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <CheckCircle className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="relative">
              <div className="bg-gradient-to-br from-primary/10 via-transparent to-accent/10 rounded-2xl p-8">
                <div className="bg-card rounded-xl p-6 shadow-lg">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold text-foreground">Performance Monitor</h3>
                    <Badge variant="secondary" className="text-xs">
                      Live
                    </Badge>
                  </div>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Response Time</span>
                      <span className="text-sm font-medium text-green-500">87ms</span>
                    </div>
                    <div className="w-full bg-muted rounded-full h-2">
                      <div className="bg-green-500 h-2 rounded-full w-[87%]"></div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Throughput</span>
                      <span className="text-sm font-medium text-blue-500">15.2k req/s</span>
                    </div>
                    <div className="w-full bg-muted rounded-full h-2">
                      <div className="bg-blue-500 h-2 rounded-full w-[95%]"></div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Cache Hit Rate</span>
                      <span className="text-sm font-medium text-purple-500">94.7%</span>
                    </div>
                    <div className="w-full bg-muted rounded-full h-2">
                      <div className="bg-purple-500 h-2 rounded-full w-[94%]"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-6 bg-gradient-to-r from-primary/10 via-transparent to-accent/10">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-3xl md:text-4xl font-heading font-bold text-foreground mb-6">
            Ready to Experience Lightning Speed?
          </h2>
          <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
            Join thousands of developers who trust our platform for mission-critical applications.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" asChild>
              <Link href="/demo">Try Demo</Link>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <Link href="/docs">View Documentation</Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}