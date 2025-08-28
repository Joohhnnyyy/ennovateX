"use client"

import { motion, useInView } from "framer-motion"
import { useRef } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { 
  Zap, 
  Shield, 
  Layers, 
  BarChart3, 
  Users, 
  Rocket,
  Globe,
  Lock
} from "lucide-react"

interface Feature {
  id: string
  icon: React.ComponentType<any>
  title: string
  description: string
  details: string
  badge?: string
  href: string
}

const features: Feature[] = [
  {
    id: "performance",
    icon: Zap,
    title: "Lightning Fast",
    description: "Optimized performance with edge computing and intelligent caching.",
    details: "Experience sub-100ms response times with our global CDN network",
    badge: "99.9% uptime",
    href: "/features/lightning-fast"
  },
  {
    id: "security",
    icon: Shield,
    title: "Enterprise Security",
    description: "Bank-grade encryption and compliance with industry standards.",
    details: "SOC2 Type II certified with end-to-end encryption",
    badge: "SOC2 Certified",
    href: "/features/enterprise-security"
  },
  {
    id: "scalable",
    icon: Layers,
    title: "Infinitely Scalable",
    description: "Auto-scaling infrastructure that grows with your business needs.",
    details: "Handle millions of requests with zero configuration required",
    href: "/features/infinitely-scalable"
  },
  {
    id: "analytics",
    icon: BarChart3,
    title: "Advanced Analytics",
    description: "Real-time insights with customizable dashboards and reports.",
    details: "Track user behavior and business metrics in real-time",
    badge: "Real-time",
    href: "/features/advanced-analytics"
  },
  {
    id: "collaboration",
    icon: Users,
    title: "Team Collaboration",
    description: "Seamless workflow management with role-based permissions.",
    details: "Invite unlimited team members with granular access controls",
    href: "/features/team-collaboration"
  },
  {
    id: "deployment",
    icon: Rocket,
    title: "One-Click Deploy",
    description: "Deploy to production in seconds with automated CI/CD pipelines.",
    details: "Zero-downtime deployments with automatic rollback capabilities",
    href: "/features/one-click-deploy"
  },
  {
    id: "global",
    icon: Globe,
    title: "Global Reach",
    description: "Worldwide infrastructure with intelligent traffic routing.",
    details: "200+ edge locations ensuring optimal performance globally",
    href: "/features/global-reach"
  },
  {
    id: "compliance",
    icon: Lock,
    title: "Data Privacy",
    description: "GDPR compliant with comprehensive data protection measures.",
    details: "Your data is encrypted, anonymized, and never shared",
    badge: "GDPR Ready",
    href: "/features/data-privacy"
  }
]

interface FeatureCardProps {
  feature: Feature
  index: number
}

function FeatureCard({ feature, index }: FeatureCardProps) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-50px" })
  const router = useRouter()

  const handleLearnMore = () => {
    router.push(feature.href)
  }

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault()
      handleLearnMore()
    }
  }

  const IconComponent = feature.icon

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 20 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
      transition={{ 
        duration: 0.4, 
        delay: index * 0.1,
        ease: "easeOut"
      }}
      whileHover={{ y: -4 }}
      className="group"
    >
      <Card 
        className="relative h-full bg-card border-border hover:border-primary/20 transition-all duration-300 cursor-pointer hover:shadow-lg hover:shadow-primary/5"
        tabIndex={0}
        role="button"
        aria-label={`Learn more about ${feature.title}`}
        onKeyDown={handleKeyDown}
        onClick={handleLearnMore}
      >
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg" />
        
        <CardHeader className="relative pb-4">
          <div className="flex items-center justify-between">
            <motion.div
              className="p-3 rounded-lg bg-muted group-hover:bg-primary/10 transition-colors duration-300"
              whileHover={{ scale: 1.05 }}
            >
              <motion.div
                animate={isInView ? {
                  stroke: "var(--color-muted-foreground)",
                } : {}}
                whileHover={{
                  stroke: "var(--color-primary)",
                  scale: 1.1
                }}
                transition={{ duration: 0.2 }}
              >
                <IconComponent className="h-6 w-6" />
              </motion.div>
            </motion.div>
            
            {feature.badge && (
              <Badge variant="secondary" className="text-xs font-medium">
                {feature.badge}
              </Badge>
            )}
          </div>
          
          <CardTitle className="text-lg font-semibold group-hover:text-primary transition-colors duration-200">
            {feature.title}
          </CardTitle>
        </CardHeader>
        
        <CardContent className="relative pt-0">
          <CardDescription className="text-muted-foreground mb-4 leading-relaxed">
            {feature.description}
          </CardDescription>
          
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            whileHover={{ opacity: 1, height: "auto" }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <p className="text-sm text-foreground/80 mb-3 leading-relaxed">
              {feature.details}
            </p>
          </motion.div>
          
          <Button 
            variant="ghost" 
            size="sm" 
            className="text-primary hover:text-primary-foreground hover:bg-primary p-0 h-auto font-medium text-sm group-hover:translate-x-1 transition-transform duration-200"
          >
            Learn more →
          </Button>
        </CardContent>
      </Card>
    </motion.div>
  )
}

interface FeaturesSectionProps {
  className?: string
}

export default function FeaturesSection({ className = "" }: FeaturesSectionProps) {
  return (
    <section className={`py-16 ${className}`}>
      <div className="container mx-auto px-6">
        <div className="max-w-3xl mb-12">
          <div className="flex items-center gap-3 mb-4">
            <div className="h-1 w-12 bg-gradient-to-r from-primary to-accent rounded-full" />
            <Badge variant="outline" className="text-xs font-medium border-primary/20 text-primary">
              Features
            </Badge>
          </div>
          
          <h2 className="text-3xl md:text-4xl font-heading font-bold text-foreground mb-4">
            Everything you need to{" "}
            <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              build better
            </span>
          </h2>
          
          <p className="text-lg text-muted-foreground leading-relaxed">
            Powerful features designed to accelerate your development workflow 
            and scale your applications with confidence.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <FeatureCard 
              key={feature.id} 
              feature={feature} 
              index={index} 
            />
          ))}
        </div>
      </div>
    </section>
  )
}