import { Metadata } from 'next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Globe, Zap, Shield, Server, MapPin, Clock, Network, Gauge } from 'lucide-react'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Global Reach | Ennovatex AI Platform',
  description: 'Worldwide infrastructure with edge computing, CDN distribution, and low-latency access from anywhere on Earth.',
}

export default function GlobalReachPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-emerald-900 to-slate-900">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/10 to-teal-500/10" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="text-center">
            <Badge variant="outline" className="mb-4 border-emerald-500/50 text-emerald-300">
              Global Reach
            </Badge>
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
              Worldwide
              <span className="bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
                {' '}Infrastructure
              </span>
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Deploy your applications across our global network of data centers and edge locations. 
              Deliver lightning-fast experiences to users anywhere on Earth.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-emerald-600 hover:bg-emerald-700">
                <Globe className="mr-2 h-4 w-4" />
                Explore Network
              </Button>
              <Button size="lg" variant="outline" className="border-emerald-500/50 text-emerald-300 hover:bg-emerald-500/10">
                View Coverage Map
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Global Stats */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid md:grid-cols-4 gap-8 mb-16">
          <div className="text-center">
            <div className="text-4xl font-bold text-emerald-400 mb-2">200+</div>
            <div className="text-gray-400">Global Locations</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-teal-400 mb-2">6</div>
            <div className="text-gray-400">Continents</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-cyan-400 mb-2">&lt; 50ms</div>
            <div className="text-gray-400">Average Latency</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-green-400 mb-2">99.99%</div>
            <div className="text-gray-400">Uptime SLA</div>
          </div>
        </div>
      </div>

      {/* Infrastructure Features */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-white mb-4">Global Infrastructure</h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Built for performance, reliability, and scale across the globe
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Zap className="h-8 w-8 text-emerald-400 mb-2" />
              <CardTitle className="text-white">Edge Computing</CardTitle>
              <CardDescription className="text-gray-400">
                Process data closer to users for ultra-low latency
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• 200+ edge locations</li>
                <li>• Real-time processing</li>
                <li>• Smart routing</li>
                <li>• Cache optimization</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Network className="h-8 w-8 text-teal-400 mb-2" />
              <CardTitle className="text-white">CDN Distribution</CardTitle>
              <CardDescription className="text-gray-400">
                Global content delivery with intelligent caching
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Multi-tier caching</li>
                <li>• Image optimization</li>
                <li>• Compression algorithms</li>
                <li>• Bandwidth optimization</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Server className="h-8 w-8 text-cyan-400 mb-2" />
              <CardTitle className="text-white">Data Centers</CardTitle>
              <CardDescription className="text-gray-400">
                Tier-4 data centers with redundant infrastructure
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• 99.99% uptime guarantee</li>
                <li>• Redundant power systems</li>
                <li>• Climate control</li>
                <li>• 24/7 monitoring</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <MapPin className="h-8 w-8 text-purple-400 mb-2" />
              <CardTitle className="text-white">Geographic Distribution</CardTitle>
              <CardDescription className="text-gray-400">
                Strategic locations for optimal global coverage
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• North America: 80 locations</li>
                <li>• Europe: 60 locations</li>
                <li>• Asia-Pacific: 45 locations</li>
                <li>• Other regions: 15 locations</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Clock className="h-8 w-8 text-orange-400 mb-2" />
              <CardTitle className="text-white">Low Latency</CardTitle>
              <CardDescription className="text-gray-400">
                Optimized routing for minimal response times
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Anycast routing</li>
                <li>• BGP optimization</li>
                <li>• Traffic engineering</li>
                <li>• Real-time monitoring</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Shield className="h-8 w-8 text-pink-400 mb-2" />
              <CardTitle className="text-white">DDoS Protection</CardTitle>
              <CardDescription className="text-gray-400">
                Advanced security at every edge location
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Multi-layer protection</li>
                <li>• Traffic filtering</li>
                <li>• Rate limiting</li>
                <li>• Threat intelligence</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Regional Coverage */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-gradient-to-r from-emerald-900/20 to-teal-900/20 rounded-2xl p-8 border border-emerald-500/20">
          <div className="text-center mb-12">
            <h3 className="text-2xl font-bold text-white mb-4">Regional Coverage</h3>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Comprehensive coverage across all major regions and markets
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h4 className="text-lg font-semibold text-white mb-4 flex items-center">
                <MapPin className="h-5 w-5 text-emerald-400 mr-2" />
                North America
              </h4>
              <div className="space-y-2 text-sm text-gray-300">
                <div>• United States: 45 locations</div>
                <div>• Canada: 8 locations</div>
                <div>• Mexico: 3 locations</div>
                <div className="text-emerald-400 font-medium">Average latency: 15ms</div>
              </div>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h4 className="text-lg font-semibold text-white mb-4 flex items-center">
                <MapPin className="h-5 w-5 text-teal-400 mr-2" />
                Europe
              </h4>
              <div className="space-y-2 text-sm text-gray-300">
                <div>• Western Europe: 35 locations</div>
                <div>• Eastern Europe: 15 locations</div>
                <div>• Nordic countries: 10 locations</div>
                <div className="text-teal-400 font-medium">Average latency: 18ms</div>
              </div>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h4 className="text-lg font-semibold text-white mb-4 flex items-center">
                <MapPin className="h-5 w-5 text-cyan-400 mr-2" />
                Asia-Pacific
              </h4>
              <div className="space-y-2 text-sm text-gray-300">
                <div>• East Asia: 25 locations</div>
                <div>• Southeast Asia: 12 locations</div>
                <div>• Australia/NZ: 8 locations</div>
                <div className="text-cyan-400 font-medium">Average latency: 22ms</div>
              </div>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h4 className="text-lg font-semibold text-white mb-4 flex items-center">
                <MapPin className="h-5 w-5 text-purple-400 mr-2" />
                South America
              </h4>
              <div className="space-y-2 text-sm text-gray-300">
                <div>• Brazil: 6 locations</div>
                <div>• Argentina: 2 locations</div>
                <div>• Chile: 2 locations</div>
                <div className="text-purple-400 font-medium">Average latency: 28ms</div>
              </div>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h4 className="text-lg font-semibold text-white mb-4 flex items-center">
                <MapPin className="h-5 w-5 text-orange-400 mr-2" />
                Middle East & Africa
              </h4>
              <div className="space-y-2 text-sm text-gray-300">
                <div>• UAE: 3 locations</div>
                <div>• South Africa: 2 locations</div>
                <div>• Israel: 2 locations</div>
                <div className="text-orange-400 font-medium">Average latency: 35ms</div>
              </div>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h4 className="text-lg font-semibold text-white mb-4 flex items-center">
                <MapPin className="h-5 w-5 text-pink-400 mr-2" />
                India
              </h4>
              <div className="space-y-2 text-sm text-gray-300">
                <div>• Mumbai: 4 locations</div>
                <div>• Delhi: 3 locations</div>
                <div>• Bangalore: 3 locations</div>
                <div className="text-pink-400 font-medium">Average latency: 25ms</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h3 className="text-2xl font-bold text-white mb-4">Performance Metrics</h3>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Real-time performance data from our global network
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <Card className="bg-slate-800/50 border-slate-700 text-center">
            <CardContent className="pt-6">
              <Gauge className="h-8 w-8 text-emerald-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white mb-1">15ms</div>
              <div className="text-sm text-gray-400">Global Average Latency</div>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700 text-center">
            <CardContent className="pt-6">
              <Zap className="h-8 w-8 text-teal-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white mb-1">2.5TB/s</div>
              <div className="text-sm text-gray-400">Network Capacity</div>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700 text-center">
            <CardContent className="pt-6">
              <Shield className="h-8 w-8 text-cyan-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white mb-1">99.99%</div>
              <div className="text-sm text-gray-400">Uptime SLA</div>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700 text-center">
            <CardContent className="pt-6">
              <Globe className="h-8 w-8 text-purple-400 mx-auto mb-2" />
              <div className="text-2xl font-bold text-white mb-1">95%</div>
              <div className="text-sm text-gray-400">Cache Hit Ratio</div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Network Partners */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h3 className="text-2xl font-bold text-white mb-4">Network Partners</h3>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Partnered with leading infrastructure providers worldwide
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
          {[
            'AWS', 'Google Cloud', 'Microsoft Azure', 'Cloudflare', 'Fastly', 'Akamai',
            'DigitalOcean', 'Vultr', 'Linode', 'OVH', 'Hetzner', 'Equinix'
          ].map((partner) => (
            <div key={partner} className="bg-slate-800/30 rounded-lg p-4 text-center border border-slate-700/50 hover:border-emerald-500/50 transition-colors">
              <div className="h-8 w-8 bg-gradient-to-br from-emerald-500 to-teal-500 rounded mx-auto mb-2" />
              <span className="text-sm text-gray-300">{partner}</span>
            </div>
          ))}
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h3 className="text-3xl font-bold text-white mb-4">
            Ready to Go Global?
          </h3>
          <p className="text-gray-400 mb-8 max-w-2xl mx-auto">
            Deploy your applications on our worldwide infrastructure and deliver 
            exceptional performance to users everywhere.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-emerald-600 hover:bg-emerald-700">
              <Globe className="mr-2 h-4 w-4" />
              Deploy Globally
            </Button>
            <Button size="lg" variant="outline" className="border-emerald-500/50 text-emerald-300 hover:bg-emerald-500/10">
              <Link href="/contact">Contact Sales</Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}