import { Metadata } from 'next'
import { BarChart3, TrendingUp, Eye, PieChart, LineChart, CheckCircle, Activity, Target } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Advanced Analytics | Ennovatex AI Platform',
  description: 'Real-time insights with customizable dashboards and reports. Track user behavior and business metrics in real-time.',
}

export default function AdvancedAnalyticsPage() {
  const analyticsFeatures = [
    {
      icon: Activity,
      title: 'Real-Time Data',
      description: 'Live data streaming with sub-second updates',
      value: '<1s Latency'
    },
    {
      icon: BarChart3,
      title: 'Custom Dashboards',
      description: 'Drag-and-drop dashboard builder with 50+ widgets',
      value: '50+ Widgets'
    },
    {
      icon: Target,
      title: 'Predictive Analytics',
      description: 'AI-powered forecasting and trend analysis',
      value: '95% Accuracy'
    },
    {
      icon: Eye,
      title: 'User Behavior',
      description: 'Track user journeys and conversion funnels',
      value: 'Full Journey'
    }
  ]

  const analyticsCapabilities = [
    'Real-time data visualization and monitoring',
    'Custom KPI tracking and alerting',
    'Advanced segmentation and cohort analysis',
    'A/B testing and experiment tracking',
    'Funnel analysis and conversion optimization',
    'Predictive modeling and forecasting',
    'Cross-platform data integration',
    'Automated report generation and scheduling'
  ]

  const dashboardTypes = [
    {
      title: 'Executive Dashboard',
      description: 'High-level KPIs and business metrics',
      icon: TrendingUp,
      features: ['Revenue tracking', 'Growth metrics', 'Performance overview']
    },
    {
      title: 'Product Analytics',
      description: 'User engagement and feature adoption',
      icon: BarChart3,
      features: ['Feature usage', 'User retention', 'Product performance']
    },
    {
      title: 'Marketing Analytics',
      description: 'Campaign performance and attribution',
      icon: PieChart,
      features: ['Campaign ROI', 'Attribution modeling', 'Customer acquisition']
    },
    {
      title: 'Operational Dashboard',
      description: 'System health and performance metrics',
      icon: LineChart,
      features: ['System uptime', 'Error tracking', 'Performance monitoring']
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
                <BarChart3 className="h-8 w-8 text-primary" />
              </div>
              <Badge variant="secondary" className="text-sm font-medium">
                Real-time
              </Badge>
            </div>
            <h1 className="text-4xl md:text-6xl font-heading font-bold text-foreground mb-6">
              Advanced
              <span className="block bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                Analytics
              </span>
            </h1>
            <p className="text-xl text-muted-foreground leading-relaxed max-w-3xl mx-auto mb-8">
              Real-time insights with customizable dashboards and reports. 
              Track user behavior and business metrics with powerful analytics tools.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild>
                <Link href="/demo">View Analytics Demo</Link>
              </Button>
              <Button variant="outline" size="lg" asChild>
                <Link href="/dashboard">Live Dashboard</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Analytics Features */}
      <section className="py-16 px-6 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-foreground mb-4">
              Powerful Analytics Engine
            </h2>
            <p className="text-lg text-muted-foreground">
              Turn data into actionable insights
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {analyticsFeatures.map((feature, index) => {
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

      {/* Dashboard Types */}
      <section className="py-16 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-foreground mb-4">
              Dashboards for Every Need
            </h2>
            <p className="text-lg text-muted-foreground">
              Pre-built templates and custom solutions
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {dashboardTypes.map((dashboard, index) => {
              const IconComponent = dashboard.icon
              return (
                <Card key={index} className="hover:shadow-lg transition-shadow group">
                  <CardHeader>
                    <div className="flex items-center gap-3 mb-4">
                      <div className="p-2 rounded-lg bg-primary/10 group-hover:bg-primary/20 transition-colors">
                        <IconComponent className="h-5 w-5 text-primary" />
                      </div>
                      <div>
                        <CardTitle className="text-lg">{dashboard.title}</CardTitle>
                        <CardDescription className="text-sm">
                          {dashboard.description}
                        </CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {dashboard.features.map((feature, featureIndex) => (
                        <div key={featureIndex} className="flex items-center gap-2">
                          <CheckCircle className="h-4 w-4 text-primary" />
                          <span className="text-sm text-muted-foreground">{feature}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </div>
      </section>

      {/* Capabilities Section */}
      <section className="py-16 px-6 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-heading font-bold text-foreground mb-6">
                Complete Analytics Suite
              </h2>
              <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
                From basic reporting to advanced machine learning insights, 
                our analytics platform provides everything you need to understand your data.
              </p>
              <div className="space-y-4">
                {analyticsCapabilities.map((capability, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <CheckCircle className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">{capability}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="relative">
              <div className="bg-gradient-to-br from-primary/10 via-transparent to-accent/10 rounded-2xl p-8">
                <div className="bg-card rounded-xl p-6 shadow-lg">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="font-semibold text-foreground">Analytics Dashboard</h3>
                    <Badge variant="secondary" className="text-xs">
                      Live
                    </Badge>
                  </div>
                  <div className="space-y-6">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-muted/50 rounded-lg p-3">
                        <div className="text-xs text-muted-foreground mb-1">Page Views</div>
                        <div className="text-lg font-bold text-foreground">24.7K</div>
                        <div className="text-xs text-green-500">+12.5%</div>
                      </div>
                      <div className="bg-muted/50 rounded-lg p-3">
                        <div className="text-xs text-muted-foreground mb-1">Conversions</div>
                        <div className="text-lg font-bold text-foreground">1.2K</div>
                        <div className="text-xs text-green-500">+8.3%</div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm text-muted-foreground">Conversion Rate</span>
                        <span className="text-sm font-medium text-primary">4.86%</span>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div className="bg-primary h-2 rounded-full w-[48%]"></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm text-muted-foreground">Bounce Rate</span>
                        <span className="text-sm font-medium text-orange-500">32.1%</span>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div className="bg-orange-500 h-2 rounded-full w-[32%]"></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm text-muted-foreground">Avg. Session</span>
                        <span className="text-sm font-medium text-blue-500">3m 42s</span>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div className="bg-blue-500 h-2 rounded-full w-[74%]"></div>
                      </div>
                    </div>
                    <div className="pt-4 border-t border-border">
                      <div className="flex items-center gap-2 text-green-500">
                        <Activity className="h-4 w-4" />
                        <span className="text-sm font-medium">Real-time tracking active</span>
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
            Start Analyzing Your Data Today
          </h2>
          <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
            Transform your raw data into actionable insights with our powerful analytics platform.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" asChild>
              <Link href="/demo">Try Demo</Link>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <Link href="/docs/analytics">Analytics Guide</Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}