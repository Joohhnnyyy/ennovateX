import { Metadata } from 'next'
import { Shield, Lock, Eye, FileCheck, Users, AlertTriangle, CheckCircle, Award } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Enterprise Security | Ennovatex AI Platform',
  description: 'Bank-grade encryption, SOC2 Type II certification, and comprehensive security features for enterprise applications.',
}

export default function EnterpriseSecurityPage() {
  const securityFeatures = [
    {
      icon: Lock,
      title: 'End-to-End Encryption',
      description: 'AES-256 encryption for data at rest and in transit',
      badge: 'AES-256'
    },
    {
      icon: Award,
      title: 'SOC2 Type II',
      description: 'Certified compliance with industry security standards',
      badge: 'Certified'
    },
    {
      icon: Eye,
      title: 'Zero Trust Architecture',
      description: 'Never trust, always verify security model',
      badge: 'Zero Trust'
    },
    {
      icon: Users,
      title: 'Access Control',
      description: 'Role-based permissions and secure access management',
      badge: 'RBAC'
    }
  ]

  const complianceStandards = [
    {
      name: 'SOC2 Type II',
      description: 'Security, availability, and confidentiality controls',
      status: 'Certified',
      icon: Award
    },
    {
      name: 'GDPR',
      description: 'General Data Protection Regulation compliance',
      status: 'Compliant',
      icon: FileCheck
    },
    {
      name: 'HIPAA',
      description: 'Healthcare data protection standards',
      status: 'Ready',
      icon: Shield
    },
    {
      name: 'ISO 27001',
      description: 'Information security management systems',
      status: 'In Progress',
      icon: CheckCircle
    }
  ]

  const securityMeasures = [
    'Advanced threat detection and response',
    'Regular security audits and penetration testing',
    'Data loss prevention (DLP) systems',
    'Role-based access control (RBAC)',
    'Continuous security monitoring',
    'Incident response and disaster recovery plans',
    'Secure development lifecycle (SDLC)',
    'Regular employee security training'
  ]

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <div className="flex items-center justify-center gap-3 mb-6">
              <div className="p-3 rounded-lg bg-primary/10">
                <Shield className="h-8 w-8 text-primary" />
              </div>
              <Badge variant="secondary" className="text-sm font-medium">
                SOC2 Certified
              </Badge>
            </div>
            <h1 className="text-4xl md:text-6xl font-heading font-bold text-foreground mb-6">
              Enterprise
              <span className="block bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                Security
              </span>
            </h1>
            <p className="text-xl text-muted-foreground leading-relaxed max-w-3xl mx-auto mb-8">
              Bank-grade encryption, comprehensive compliance, and advanced security features 
              designed to protect your most sensitive data and applications.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild>
                <Link href="/demo">Security Demo</Link>
              </Button>
              <Button variant="outline" size="lg" asChild>
                <Link href="/docs/security">Security Docs</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Security Features */}
      <section className="py-16 px-6 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-foreground mb-4">
              Military-Grade Security
            </h2>
            <p className="text-lg text-muted-foreground">
              Comprehensive protection at every layer
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {securityFeatures.map((feature, index) => {
              const IconComponent = feature.icon
              return (
                <Card key={index} className="text-center hover:shadow-lg transition-shadow group">
                  <CardHeader className="pb-4">
                    <div className="mx-auto p-3 rounded-lg bg-primary/10 w-fit mb-4 group-hover:bg-primary/20 transition-colors">
                      <IconComponent className="h-6 w-6 text-primary" />
                    </div>
                    <Badge variant="outline" className="mx-auto w-fit mb-2">
                      {feature.badge}
                    </Badge>
                    <CardTitle className="text-lg font-semibold">
                      {feature.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-sm">
                      {feature.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </div>
      </section>

      {/* Compliance Standards */}
      <section className="py-16 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-heading font-bold text-foreground mb-4">
              Compliance & Certifications
            </h2>
            <p className="text-lg text-muted-foreground">
              Meeting the highest industry standards
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {complianceStandards.map((standard, index) => {
              const IconComponent = standard.icon
              const statusColor = {
                'Certified': 'text-green-500 bg-green-500/10',
                'Compliant': 'text-blue-500 bg-blue-500/10',
                'Ready': 'text-purple-500 bg-purple-500/10',
                'In Progress': 'text-orange-500 bg-orange-500/10'
              }[standard.status] || 'text-gray-500 bg-gray-500/10'
              
              return (
                <Card key={index} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-2 rounded-lg bg-primary/10">
                          <IconComponent className="h-5 w-5 text-primary" />
                        </div>
                        <div>
                          <CardTitle className="text-lg">{standard.name}</CardTitle>
                          <CardDescription className="text-sm">
                            {standard.description}
                          </CardDescription>
                        </div>
                      </div>
                      <Badge className={statusColor}>
                        {standard.status}
                      </Badge>
                    </div>
                  </CardHeader>
                </Card>
              )
            })}
          </div>
        </div>
      </section>

      {/* Security Measures */}
      <section className="py-16 px-6 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-heading font-bold text-foreground mb-6">
                Comprehensive Protection
              </h2>
              <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
                Our multi-layered security approach ensures your data and applications 
                are protected against evolving threats and vulnerabilities.
              </p>
              <div className="space-y-4">
                {securityMeasures.map((measure, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <CheckCircle className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
                    <span className="text-foreground">{measure}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="relative">
              <div className="bg-gradient-to-br from-primary/10 via-transparent to-accent/10 rounded-2xl p-8">
                <div className="bg-card rounded-xl p-6 shadow-lg">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="font-semibold text-foreground">Security Dashboard</h3>
                    <Badge variant="secondary" className="text-xs">
                      Live
                    </Badge>
                  </div>
                  <div className="space-y-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span className="text-sm text-muted-foreground">Threat Detection</span>
                      </div>
                      <span className="text-sm font-medium text-green-500">Active</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                        <span className="text-sm text-muted-foreground">Encryption Status</span>
                      </div>
                      <span className="text-sm font-medium text-blue-500">AES-256</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                        <span className="text-sm text-muted-foreground">Access Control</span>
                      </div>
                      <span className="text-sm font-medium text-purple-500">RBAC</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                        <span className="text-sm text-muted-foreground">Compliance</span>
                      </div>
                      <span className="text-sm font-medium text-orange-500">SOC2</span>
                    </div>
                    <div className="pt-4 border-t border-border">
                      <div className="flex items-center gap-2 text-green-500">
                        <CheckCircle className="h-4 w-4" />
                        <span className="text-sm font-medium">All systems secure</span>
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
            Secure Your Enterprise Today
          </h2>
          <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
            Join enterprise customers who trust our platform with their most sensitive data.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" asChild>
              <Link href="/demo">Try Demo</Link>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <Link href="/demo">Try Demo</Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}