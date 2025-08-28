import { Metadata } from 'next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Rocket, GitBranch, Server, Zap, CheckCircle, Clock, Shield, Globe } from 'lucide-react'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'One-Click Deploy | Ennovatex AI Platform',
  description: 'Deploy your applications instantly with our automated deployment pipeline. Zero-downtime deployments with rollback capabilities.',
}

export default function OneClickDeployPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-cyan-500/10" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="text-center">
            <Badge variant="outline" className="mb-4 border-blue-500/50 text-blue-300">
              One-Click Deploy
            </Badge>
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
              Deploy in
              <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                {' '}Seconds
              </span>
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Streamline your deployment process with automated pipelines, zero-downtime deployments, 
              and instant rollbacks. From code to production in just one click.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                <Rocket className="mr-2 h-4 w-4" />
                Deploy Now
              </Button>
              <Button size="lg" variant="outline" className="border-blue-500/50 text-blue-300 hover:bg-blue-500/10">
                Watch Demo
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Deployment Process */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-white mb-4">Deployment Process</h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            From commit to production in three simple steps
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="bg-blue-600/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 border border-blue-500/30">
              <GitBranch className="h-8 w-8 text-blue-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">1. Code Commit</h3>
            <p className="text-gray-400">
              Push your code to any branch and trigger automated builds
            </p>
          </div>

          <div className="text-center">
            <div className="bg-cyan-600/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 border border-cyan-500/30">
              <Zap className="h-8 w-8 text-cyan-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">2. Auto Build</h3>
            <p className="text-gray-400">
              Automated testing, building, and optimization of your application
            </p>
          </div>

          <div className="text-center">
            <div className="bg-green-600/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 border border-green-500/30">
              <Rocket className="h-8 w-8 text-green-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">3. Deploy</h3>
            <p className="text-gray-400">
              Zero-downtime deployment to production with health checks
            </p>
          </div>
        </div>
      </div>

      {/* Deployment Features */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Zap className="h-8 w-8 text-blue-400 mb-2" />
              <CardTitle className="text-white">Instant Deployment</CardTitle>
              <CardDescription className="text-gray-400">
                Deploy your applications in seconds, not hours
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Sub-30 second deployments</li>
                <li>• Parallel processing</li>
                <li>• Optimized build caching</li>
                <li>• CDN edge deployment</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Shield className="h-8 w-8 text-green-400 mb-2" />
              <CardTitle className="text-white">Zero Downtime</CardTitle>
              <CardDescription className="text-gray-400">
                Blue-green deployments ensure continuous availability
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Blue-green deployment</li>
                <li>• Health check validation</li>
                <li>• Traffic switching</li>
                <li>• Automatic rollback</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Clock className="h-8 w-8 text-orange-400 mb-2" />
              <CardTitle className="text-white">Rollback Protection</CardTitle>
              <CardDescription className="text-gray-400">
                Instant rollback to previous versions when needed
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• One-click rollback</li>
                <li>• Version history</li>
                <li>• Database migrations</li>
                <li>• Configuration snapshots</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Server className="h-8 w-8 text-purple-400 mb-2" />
              <CardTitle className="text-white">Multi-Environment</CardTitle>
              <CardDescription className="text-gray-400">
                Deploy to staging, production, and custom environments
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Environment isolation</li>
                <li>• Custom configurations</li>
                <li>• Promotion workflows</li>
                <li>• Environment variables</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <CheckCircle className="h-8 w-8 text-cyan-400 mb-2" />
              <CardTitle className="text-white">Quality Gates</CardTitle>
              <CardDescription className="text-gray-400">
                Automated testing and quality checks before deployment
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Unit & integration tests</li>
                <li>• Security scanning</li>
                <li>• Performance testing</li>
                <li>• Code quality checks</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Globe className="h-8 w-8 text-pink-400 mb-2" />
              <CardTitle className="text-white">Global Distribution</CardTitle>
              <CardDescription className="text-gray-400">
                Deploy to multiple regions simultaneously
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Multi-region deployment</li>
                <li>• Edge computing</li>
                <li>• Load balancing</li>
                <li>• Geo-routing</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Deployment Pipeline */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-gradient-to-r from-blue-900/20 to-cyan-900/20 rounded-2xl p-8 border border-blue-500/20">
          <div className="text-center mb-12">
            <h3 className="text-2xl font-bold text-white mb-4">Deployment Pipeline</h3>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Visualize your entire deployment process with real-time status updates
            </p>
          </div>

          <div className="grid lg:grid-cols-5 gap-4">
            {[
              { stage: 'Source', icon: GitBranch, status: 'completed' },
              { stage: 'Build', icon: Zap, status: 'completed' },
              { stage: 'Test', icon: CheckCircle, status: 'running' },
              { stage: 'Deploy', icon: Rocket, status: 'pending' },
              { stage: 'Monitor', icon: Globe, status: 'pending' }
            ].map((step, index) => {
              const Icon = step.icon
              return (
                <div key={step.stage} className="text-center">
                  <div className={`
                    w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-2 border-2
                    ${step.status === 'completed' ? 'bg-green-600/20 border-green-500 text-green-400' : ''}
                    ${step.status === 'running' ? 'bg-blue-600/20 border-blue-500 text-blue-400 animate-pulse' : ''}
                    ${step.status === 'pending' ? 'bg-gray-600/20 border-gray-500 text-gray-400' : ''}
                  `}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <span className="text-sm text-gray-300">{step.stage}</span>
                <div key={step.stage} className="text-center relative">
                  {index < 4 && (
                    <div className="hidden lg:block absolute top-6 left-1/2 w-8 h-0.5 bg-gray-600 transform translate-x-full" />
                  )}
                </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* Supported Platforms */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h3 className="text-2xl font-bold text-white mb-4">Supported Platforms</h3>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Deploy to any cloud provider or hosting platform
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
          {[
            'AWS', 'Google Cloud', 'Azure', 'Vercel', 'Netlify', 'Heroku',
            'DigitalOcean', 'Kubernetes', 'Docker', 'Railway', 'Render', 'Fly.io'
          ].map((platform) => (
            <div key={platform} className="bg-slate-800/30 rounded-lg p-4 text-center border border-slate-700/50 hover:border-blue-500/50 transition-colors">
              <div className="h-8 w-8 bg-gradient-to-br from-blue-500 to-cyan-500 rounded mx-auto mb-2" />
              <span className="text-sm text-gray-300">{platform}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid md:grid-cols-4 gap-8">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-400 mb-2">&lt; 30s</div>
            <div className="text-gray-400">Average Deploy Time</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-400 mb-2">99.9%</div>
            <div className="text-gray-400">Success Rate</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-cyan-400 mb-2">0</div>
            <div className="text-gray-400">Downtime</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-400 mb-2">&lt; 5s</div>
            <div className="text-gray-400">Rollback Time</div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h3 className="text-3xl font-bold text-white mb-4">
            Ready to Accelerate Your Deployments?
          </h3>
          <p className="text-gray-400 mb-8 max-w-2xl mx-auto">
            Join thousands of developers who have streamlined their deployment process.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
              <Rocket className="mr-2 h-4 w-4" />
              Start Deploying
            </Button>
            <Link href="/contact">
              <Button size="lg" variant="outline" className="border-blue-500/50 text-blue-300 hover:bg-blue-500/10">
                Contact Sales
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}