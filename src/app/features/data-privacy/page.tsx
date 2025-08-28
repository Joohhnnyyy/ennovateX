import { Metadata } from 'next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Shield, Lock, Eye, FileText, UserCheck, Database, Key, AlertTriangle } from 'lucide-react'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Data Privacy | Ennovatex AI Platform',
  description: 'Comprehensive data privacy controls with GDPR compliance, encryption, and user consent management.',
}

export default function DataPrivacyPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/10 to-purple-500/10" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="text-center">
            <Badge variant="outline" className="mb-4 border-indigo-500/50 text-indigo-300">
              Data Privacy
            </Badge>
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
              Privacy by
              <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
                {' '}Design
              </span>
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Comprehensive data privacy controls that put users in control. GDPR compliant, 
              end-to-end encrypted, with transparent data handling practices.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-indigo-600 hover:bg-indigo-700">
                <Shield className="mr-2 h-4 w-4" />
                Privacy Center
              </Button>
              <Button size="lg" variant="outline" className="border-indigo-500/50 text-indigo-300 hover:bg-indigo-500/10">
                View Privacy Policy
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Privacy Principles */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-white mb-4">Privacy Principles</h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Our commitment to protecting your data and respecting your privacy
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="text-center">
            <div className="bg-indigo-600/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 border border-indigo-500/30">
              <Eye className="h-8 w-8 text-indigo-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Transparency</h3>
            <p className="text-gray-400">
              Clear information about what data we collect and how it's used
            </p>
          </div>

          <div className="text-center">
            <div className="bg-purple-600/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 border border-purple-500/30">
              <UserCheck className="h-8 w-8 text-purple-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">User Control</h3>
            <p className="text-gray-400">
              Complete control over your data with easy access and deletion
            </p>
          </div>

          <div className="text-center">
            <div className="bg-blue-600/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 border border-blue-500/30">
              <Lock className="h-8 w-8 text-blue-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Security</h3>
            <p className="text-gray-400">
              Military-grade encryption and security measures
            </p>
          </div>

          <div className="text-center">
            <div className="bg-cyan-600/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 border border-cyan-500/30">
              <Shield className="h-8 w-8 text-cyan-400" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Compliance</h3>
            <p className="text-gray-400">
              Full compliance with GDPR, CCPA, and other privacy regulations
            </p>
          </div>
        </div>
      </div>

      {/* Privacy Features */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Lock className="h-8 w-8 text-indigo-400 mb-2" />
              <CardTitle className="text-white">End-to-End Encryption</CardTitle>
              <CardDescription className="text-gray-400">
                Your data is encrypted at rest and in transit
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• AES-256 encryption</li>
                <li>• Zero-knowledge architecture</li>
                <li>• Encrypted backups</li>
                <li>• Secure key management</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <UserCheck className="h-8 w-8 text-purple-400 mb-2" />
              <CardTitle className="text-white">Consent Management</CardTitle>
              <CardDescription className="text-gray-400">
                Granular control over data collection and usage
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Granular permissions</li>
                <li>• Consent tracking</li>
                <li>• Easy opt-out</li>
                <li>• Preference center</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Database className="h-8 w-8 text-blue-400 mb-2" />
              <CardTitle className="text-white">Data Minimization</CardTitle>
              <CardDescription className="text-gray-400">
                We only collect data that's necessary for our services
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Purpose limitation</li>
                <li>• Data retention policies</li>
                <li>• Automatic deletion</li>
                <li>• Regular audits</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Eye className="h-8 w-8 text-cyan-400 mb-2" />
              <CardTitle className="text-white">Data Transparency</CardTitle>
              <CardDescription className="text-gray-400">
                Complete visibility into your data usage
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Data usage dashboard</li>
                <li>• Access logs</li>
                <li>• Processing activities</li>
                <li>• Third-party sharing</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Key className="h-8 w-8 text-green-400 mb-2" />
              <CardTitle className="text-white">User Rights</CardTitle>
              <CardDescription className="text-gray-400">
                Exercise your privacy rights with ease
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Right to access</li>
                <li>• Right to rectification</li>
                <li>• Right to erasure</li>
                <li>• Data portability</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <AlertTriangle className="h-8 w-8 text-orange-400 mb-2" />
              <CardTitle className="text-white">Breach Protection</CardTitle>
              <CardDescription className="text-gray-400">
                Proactive monitoring and incident response
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• 24/7 monitoring</li>
                <li>• Incident response plan</li>
                <li>• Breach notifications</li>
                <li>• Forensic analysis</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Compliance Standards */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-gradient-to-r from-indigo-900/20 to-purple-900/20 rounded-2xl p-8 border border-indigo-500/20">
          <div className="text-center mb-12">
            <h3 className="text-2xl font-bold text-white mb-4">Compliance Standards</h3>
            <p className="text-gray-400 max-w-2xl mx-auto">
              We meet and exceed international privacy and security standards
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 text-center">
              <div className="h-12 w-12 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-lg mx-auto mb-4 flex items-center justify-center">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <h4 className="text-lg font-semibold text-white mb-2">GDPR</h4>
              <p className="text-sm text-gray-400">General Data Protection Regulation compliance</p>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 text-center">
              <div className="h-12 w-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg mx-auto mb-4 flex items-center justify-center">
                <Lock className="h-6 w-6 text-white" />
              </div>
              <h4 className="text-lg font-semibold text-white mb-2">CCPA</h4>
              <p className="text-sm text-gray-400">California Consumer Privacy Act compliance</p>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 text-center">
              <div className="h-12 w-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-lg mx-auto mb-4 flex items-center justify-center">
                <FileText className="h-6 w-6 text-white" />
              </div>
              <h4 className="text-lg font-semibold text-white mb-2">HIPAA</h4>
              <p className="text-sm text-gray-400">Health Insurance Portability and Accountability Act</p>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 text-center">
              <div className="h-12 w-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-lg mx-auto mb-4 flex items-center justify-center">
                <Database className="h-6 w-6 text-white" />
              </div>
              <h4 className="text-lg font-semibold text-white mb-2">SOC 2</h4>
              <p className="text-sm text-gray-400">Service Organization Control 2 Type II</p>
            </div>
          </div>
        </div>
      </div>

      {/* Privacy Controls */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <h3 className="text-2xl font-bold text-white mb-6">Privacy Control Center</h3>
            <p className="text-gray-300 mb-8">
              Take control of your privacy with our comprehensive privacy dashboard. 
              Manage your data, review permissions, and exercise your rights.
            </p>
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-indigo-400 rounded-full" />
                <span className="text-gray-300">View and download your data</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-purple-400 rounded-full" />
                <span className="text-gray-300">Manage consent preferences</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-blue-400 rounded-full" />
                <span className="text-gray-300">Request data deletion</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-cyan-400 rounded-full" />
                <span className="text-gray-300">Review access logs</span>
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
            <h4 className="text-lg font-semibold text-white mb-4">Your Privacy Rights</h4>
            <div className="space-y-4">
              <div className="flex justify-between items-center p-3 bg-slate-700/50 rounded-lg">
                <span className="text-gray-300">Data Access</span>
                <Badge variant="outline" className="border-green-500/50 text-green-300">Available</Badge>
              </div>
              <div className="flex justify-between items-center p-3 bg-slate-700/50 rounded-lg">
                <span className="text-gray-300">Data Portability</span>
                <Badge variant="outline" className="border-blue-500/50 text-blue-300">Available</Badge>
              </div>
              <div className="flex justify-between items-center p-3 bg-slate-700/50 rounded-lg">
                <span className="text-gray-300">Data Deletion</span>
                <Badge variant="outline" className="border-red-500/50 text-red-300">Available</Badge>
              </div>
              <div className="flex justify-between items-center p-3 bg-slate-700/50 rounded-lg">
                <span className="text-gray-300">Consent Management</span>
                <Badge variant="outline" className="border-purple-500/50 text-purple-300">Active</Badge>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Data Processing */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h3 className="text-2xl font-bold text-white mb-4">Data Processing Transparency</h3>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Understand how your data flows through our systems
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="bg-indigo-600/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 border border-indigo-500/30">
              <Database className="h-8 w-8 text-indigo-400" />
            </div>
            <h4 className="text-lg font-semibold text-white mb-2">Collection</h4>
            <p className="text-gray-400 text-sm">
              We collect only necessary data with your explicit consent
            </p>
          </div>

          <div className="text-center">
            <div className="bg-purple-600/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 border border-purple-500/30">
              <Lock className="h-8 w-8 text-purple-400" />
            </div>
            <h4 className="text-lg font-semibold text-white mb-2">Processing</h4>
            <p className="text-gray-400 text-sm">
              Data is processed securely for specified purposes only
            </p>
          </div>

          <div className="text-center">
            <div className="bg-blue-600/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4 border border-blue-500/30">
              <Shield className="h-8 w-8 text-blue-400" />
            </div>
            <h4 className="text-lg font-semibold text-white mb-2">Protection</h4>
            <p className="text-gray-400 text-sm">
              Your data is protected with enterprise-grade security
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h3 className="text-3xl font-bold text-white mb-4">
            Your Privacy, Your Control
          </h3>
          <p className="text-gray-400 mb-8 max-w-2xl mx-auto">
            Experience the peace of mind that comes with true privacy protection. 
            Your data, your rules.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-indigo-600 hover:bg-indigo-700">
              <Shield className="mr-2 h-4 w-4" />
              Access Privacy Center
            </Button>
            <Button size="lg" variant="outline" className="border-indigo-500/50 text-indigo-300 hover:bg-indigo-500/10">
              <Link href="/contact">Contact Privacy Team</Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}