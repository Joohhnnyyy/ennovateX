import { Metadata } from 'next'
import { Layers, TrendingUp, Server, Cpu, BarChart3, CheckCircle, ArrowUp, Zap } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Infinitely Scalable | Ennovatex AI Platform',
  description: 'Auto-scaling infrastructure that grows with your business needs. Handle millions of requests with zero configuration.',
}

export default function InfinitelyScalablePage() {
  const scalingFeatures = [
    {
      icon: TrendingUp,
      title: 'Auto-Scaling',
      description: 'Automatically scale up or down based on demand',
      value: '0-1M+ req/s'
    },
    {
      icon: Server,
      title: 'Load Balancing',
      description: 'Intelligent traffic distribution across servers',
      value: '99.99% Uptime'
    },
    {
      icon: Cpu,
      title: 'Resource Optimization',
      description: 'Dynamic resource allocation for peak efficiency',
      value: '70% Cost Savings'
    },
    {
      icon: Zap,
      title: 'Instant Provisioning',
      description: 'New instances ready in under 30 seconds',
      value: '<30s Deploy'
    }
  ]

  const scalingBenefits = [
    'Zero configuration auto-scaling',
    'Pay only for resources you use',
    'Automatic failover and redundancy',
    'Global load distribution',
    'Real-time performance monitoring',
    'Predictive scaling based on patterns',
    'Multi-cloud deployment support',
    'Container orchestration with Kubernetes'
  ]

  const useCases = [
    {
      title: 'E-commerce Platforms',
      description: 'Handle traffic spikes during sales events',
      icon: BarChart3,
      metrics: 'Scale from 1K to 100K users instantly'
    },
    {
      title: 'Media Streaming',
      description: 'Deliver content to millions simultaneously',
      icon: Layers,
      metrics: 'Support 10M+ concurrent streams'
    },
    {
      title: 'Gaming Applications',
      description: 'Scale game servers based on player count',
      icon: Server,
      metrics: 'Auto-scale to 1M+ active players'
    }
  ]

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <div className="flex items-center justify-center gap-3 mb-6">
              <div className="p-3 rounded-lg bg-primary/10">
                <Layers className="h-8 w-8 text-primary" />
              </div>
              <Badge variant="secondary" className="text-sm font-medium">
                Zero Configuration
              </Badge>
            </div>
            <h1 className="text-4xl md:text-6xl font-heading font-bold text-foreground mb-6">
              Infinitely
              <span className="block bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                Scalable
              </span>
            </h1>
            <p className="text-xl text-muted-foreground leading-relaxed max-w-3xl mx-auto mb-8">
              Auto-scaling infrastructure that grows with your business needs. 
              Handle millions of requests with zero configuration required.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild>
                <Link href="/demo">See Scaling Demo</Link>
              </Button>
              <Button variant="outline" size="lg" asChild>
                <Link href="/demo">Try Demo</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Scaling Features */}
      <section className="py-16 px-6 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-foreground mb-4">
              Scale Without Limits
            </h2>
            <p className="text-lg text-muted-foreground">
              Intelligent infrastructure that adapts to your needs
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {scalingFeatures.map((feature, index) => {
              const IconComponent = feature.icon
              return (
                <Card key={index} className="text-center hover:shadow-lg transition-shadow group">
                  <CardHeader className="pb-4">
                    <div className="mx-auto p-3 rounded-lg bg-primary/10 w-fit mb-4 group-hover:bg-primary/20 transition-colors">
                      <IconComponent className="h-6 w-6 text-primary" />
                    </div>
                    <CardTitle className="text-2xl font-bold text-primary">
                      {feature.value}
                    </CardTitle>
                    <CardDescription className="font-semibold">
                      {feature.title}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">
                      {feature.description}
                    </p>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </div>
      </section>

      {/* Use Cases */}
      <section className="py-16 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-foreground mb-4">
              Built for Every Scale
            </h2>
            <p className="text-lg text-muted-foreground">
              From startups to enterprise, we scale with you
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {useCases.map((useCase, index) => {
              const IconComponent = useCase.icon
              return (
                <Card key={index} className="hover:shadow-lg transition-shadow group">
                  <CardHeader>
                    <div className="flex items-center gap-3 mb-4">
                      <div className="p-2 rounded-lg bg-primary/10 group-hover:bg-primary/20 transition-colors">
                        <IconComponent className="h-5 w-5 text-primary" />
                      </div>
                      <CardTitle className="text-lg">{useCase.title}</CardTitle>
                    </div>
                    <CardDescription className="text-sm mb-4">
                      {useCase.description}
                    </CardDescription>
                    <Badge variant="outline" className="w-fit">
                      {useCase.metrics}
                    </Badge>
                  </CardHeader>
                </Card>
              )
            })}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-16 px-6 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-heading font-bold text-foreground mb-6">
                Smart Scaling Technology
              </h2>
              <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
                Our intelligent auto-scaling system monitors your application performance 
                and automatically adjusts resources to maintain optimal performance.
              </p>
              <div className="space-y-4">
                {scalingBenefits.map((benefit, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <CheckCircle className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="relative">
              <div className="bg-gradient-to-br from-primary/10 via-transparent to-accent/10 rounded-2xl p-8">
                <div className="bg-card rounded-xl p-6 shadow-lg">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="font-semibold text-foreground">Scaling Monitor</h3>
                    <Badge variant="secondary" className="text-xs">
                      Live
                    </Badge>
                  </div>
                  <div className="space-y-6">
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm text-muted-foreground">Active Instances</span>
                        <div className="flex items-center gap-1">
                          <ArrowUp className="h-3 w-3 text-green-500" />
                          <span className="text-sm font-medium text-green-500">12</span>
                        </div>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div className="bg-green-500 h-2 rounded-full w-[75%]"></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm text-muted-foreground">CPU Usage</span>
                        <span className="text-sm font-medium text-blue-500">68%</span>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div className="bg-blue-500 h-2 rounded-full w-[68%]"></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm text-muted-foreground">Memory Usage</span>
                        <span className="text-sm font-medium text-purple-500">54%</span>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div className="bg-purple-500 h-2 rounded-full w-[54%]"></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm text-muted-foreground">Requests/sec</span>
                        <span className="text-sm font-medium text-orange-500">8.2K</span>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div className="bg-orange-500 h-2 rounded-full w-[82%]"></div>
                      </div>
                    </div>
                    <div className="pt-4 border-t border-border">
                      <div className="flex items-center gap-2 text-green-500">
                        <CheckCircle className="h-4 w-4" />
                        <span className="text-sm font-medium">Auto-scaling active</span>
                      </div>
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
            Ready to Scale Infinitely?
          </h2>
          <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
            Start small and grow big with our intelligent auto-scaling infrastructure.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" asChild>
              <Link href="/demo">Try Demo</Link>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <Link href="/docs/scaling">Scaling Guide</Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}