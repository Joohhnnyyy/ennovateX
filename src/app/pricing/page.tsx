"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import NavBar from "@/components/NavBar"

import { 
  Check, 
  X, 
  Zap, 
  Shield, 
  Brain, 
  Users, 
  Database, 
  Globe, 
  Star, 
  ArrowRight, 
  Sparkles, 
  Crown, 
  Rocket,
  Phone,
  Mail,
  MessageCircle
} from 'lucide-react';

interface PricingPlan {
  id: string;
  name: string;
  description: string;
  price: string;
  period: string;
  popular?: boolean;
  enterprise?: boolean;
  features: string[];
  limitations?: string[];
  icon: React.ReactNode;
  color: string;
  buttonText: string;
}

interface FAQ {
  question: string;
  answer: string;
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

const PricingCard: React.FC<{ plan: PricingPlan; index: number; billingCycle: 'monthly' | 'yearly' }> = ({ 
  plan, 
  index, 
  billingCycle 
}) => {
  const adjustedPrice = billingCycle === 'yearly' && plan.price !== 'Custom' 
    ? `$${Math.round(parseInt(plan.price.replace('$', '')) * 0.8)}` 
    : plan.price;

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay: index * 0.1 }}
      className={`relative bg-card/50 backdrop-blur-xl rounded-2xl border shadow-lg hover:shadow-xl transition-all duration-300 ${
        plan.popular 
          ? 'border-primary/50 ring-2 ring-primary/20 scale-105' 
          : 'border-border/50'
      } ${
        plan.enterprise 
          ? 'bg-gradient-to-br from-primary/10 to-accent/10'
          : ''
      }`}
    >
      {plan.popular && (
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
          <div className="bg-gradient-to-r from-primary to-accent text-primary-foreground px-4 py-1 rounded-full text-sm font-medium flex items-center space-x-1">
            <Star className="w-4 h-4" />
            <span>Most Popular</span>
          </div>
        </div>
      )}
      
      {plan.enterprise && (
        <div className="absolute -top-4 right-4">
          <div className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white p-2 rounded-full">
            <Crown className="w-5 h-5" />
          </div>
        </div>
      )}

      <div className="p-8">
        <div className="flex items-center space-x-3 mb-4">
          <div className={`p-3 rounded-xl`} style={{ backgroundColor: `${plan.color}20` }}>
            {plan.icon}
          </div>
          <div>
            <h3 className="text-xl font-heading font-bold text-foreground">{plan.name}</h3>
            <p className="text-sm text-muted-foreground">{plan.description}</p>
          </div>
        </div>

        <div className="mb-6">
          <div className="flex items-baseline space-x-2">
            <span className="text-4xl font-bold text-foreground">{adjustedPrice}</span>
            {plan.price !== 'Custom' && (
              <span className="text-muted-foreground">/{plan.period}</span>
            )}
          </div>
          {billingCycle === 'yearly' && plan.price !== 'Custom' && (
            <p className="text-sm text-green-500 mt-1">Save 20% with yearly billing</p>
          )}
        </div>

        <button 
          className={`w-full py-3 px-6 rounded-xl font-medium transition-all duration-200 mb-6 ${
            plan.popular || plan.enterprise
              ? 'bg-gradient-to-r from-primary to-accent text-primary-foreground hover:shadow-lg hover:scale-105'
              : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
          }`}
        >
          {plan.buttonText}
        </button>

        <div className="space-y-4">
          <h4 className="font-semibold text-foreground">Features included:</h4>
          <ul className="space-y-3">
            {plan.features.map((feature, featureIndex) => (
              <li key={featureIndex} className="flex items-start space-x-3">
                <Check className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                <span className="text-sm text-muted-foreground">{feature}</span>
              </li>
            ))}
          </ul>
          
          {plan.limitations && plan.limitations.length > 0 && (
            <>
              <h4 className="font-semibold text-foreground mt-6">Limitations:</h4>
              <ul className="space-y-3">
                {plan.limitations.map((limitation, limitIndex) => (
                  <li key={limitIndex} className="flex items-start space-x-3">
                    <X className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-muted-foreground">{limitation}</span>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default function PricingPage() {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');
  const [expandedFAQ, setExpandedFAQ] = useState<number | null>(null);

  const pricingPlans: PricingPlan[] = [
    {
      id: 'starter',
      name: 'Starter',
      description: 'Perfect for individuals and small projects',
      price: '$29',
      period: 'month',
      icon: <Rocket className="w-6 h-6" style={{ color: '#10B981' }} />,
      color: '#10B981',
      buttonText: 'Start Free Trial',
      features: [
        'Up to 1,000 AI requests per month',
        'Basic AI models access',
        'Standard support',
        'API access',
        'Basic analytics',
        'Community forum access'
      ],
      limitations: [
        'Limited to 3 projects',
        'No custom model training',
        'Basic data storage (1GB)'
      ]
    },
    {
      id: 'professional',
      name: 'Professional',
      description: 'Ideal for growing businesses and teams',
      price: '$99',
      period: 'month',
      popular: true,
      icon: <Brain className="w-6 h-6" style={{ color: '#1428A0' }} />,
      color: '#1428A0',
      buttonText: 'Get Started',
      features: [
        'Up to 10,000 AI requests per month',
        'Advanced AI models access',
        'Priority support',
        'Full API access',
        'Advanced analytics & insights',
        'Custom integrations',
        'Team collaboration tools',
        'Data export capabilities',
        'Custom model fine-tuning'
      ],
      limitations: [
        'Limited to 10 team members',
        'Advanced data storage (50GB)'
      ]
    },
    {
      id: 'enterprise',
      name: 'Enterprise',
      description: 'For large organizations with custom needs',
      price: 'Custom',
      period: 'contact us',
      enterprise: true,
      icon: <Crown className="w-6 h-6" style={{ color: '#F59E0B' }} />,
      color: '#F59E0B',
      buttonText: 'Contact Sales',
      features: [
        'Unlimited AI requests',
        'All AI models + custom models',
        'Dedicated support manager',
        'White-label solutions',
        'Advanced security & compliance',
        'Custom integrations & APIs',
        'Unlimited team members',
        'On-premise deployment options',
        'Custom SLA agreements',
        'Advanced training & onboarding',
        'Unlimited data storage',
        'Custom reporting & analytics'
      ]
    }
  ];

  const faqs: FAQ[] = [
    {
      question: 'What is included in the free trial?',
      answer: 'The free trial includes full access to the Starter plan for 14 days, including 1,000 AI requests, basic models, and standard support.'
    },
    {
      question: 'Can I change my plan at any time?',
      answer: 'Yes, you can upgrade or downgrade your plan at any time. Changes will be reflected in your next billing cycle.'
    },
    {
      question: 'What happens if I exceed my request limit?',
      answer: 'If you exceed your monthly request limit, you can either upgrade your plan or purchase additional requests at $0.05 per request.'
    },
    {
      question: 'Do you offer custom pricing for large volumes?',
      answer: 'Yes, we offer custom pricing for enterprise customers with high-volume needs. Contact our sales team for a personalized quote.'
    },
    {
      question: 'Is there a setup fee?',
      answer: 'No, there are no setup fees for any of our plans. You only pay the monthly or yearly subscription fee.'
    },
    {
      question: 'What payment methods do you accept?',
      answer: 'We accept all major credit cards and bank transfers for enterprise customers.'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background/95 to-primary/5">

      
      {/* Floating Navigation */}
      <NavBar />
      {/* Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <FloatingElement delay={0.2} className="absolute top-20 right-20">
          <div className="p-4 bg-gradient-to-br from-primary/20 to-accent/20 rounded-2xl backdrop-blur-sm border border-white/10">
            <Sparkles className="w-8 h-8 text-primary" />
          </div>
        </FloatingElement>

        <FloatingElement delay={0.4} className="absolute top-40 left-20">
          <div className="p-4 bg-gradient-to-br from-accent/20 to-primary/20 rounded-2xl backdrop-blur-sm border border-white/10">
            <Crown className="w-8 h-8 text-accent" />
          </div>
        </FloatingElement>

        <FloatingElement delay={0.6} className="absolute bottom-40 right-32">
          <div className="p-4 bg-gradient-to-br from-[#00ADEF]/20 to-[#1428A0]/20 rounded-2xl backdrop-blur-sm border border-white/10">
            <Zap className="w-8 h-8 text-[#00ADEF]" />
          </div>
        </FloatingElement>
      </div>

      <div className="relative z-10 container mx-auto px-6 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <div className="mb-6">
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
              EnnovateX AI Pricing
            </div>
          </div>
          <h1 className="text-4xl font-heading font-bold text-foreground mb-4">
            Choose Your AI Journey
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-8">
            Flexible pricing plans designed to scale with your business needs. Start free and upgrade as you grow.
          </p>

          {/* Billing Toggle */}
          <div className="flex items-center justify-center space-x-4 mb-8">
            <span className={`text-sm font-medium ${
              billingCycle === 'monthly' ? 'text-foreground' : 'text-muted-foreground'
            }`}>
              Monthly
            </span>
            <button
              onClick={() => setBillingCycle(billingCycle === 'monthly' ? 'yearly' : 'monthly')}
              className={`relative w-14 h-7 rounded-full transition-colors duration-200 ${
                billingCycle === 'yearly' ? 'bg-primary' : 'bg-secondary'
              }`}
            >
              <div className={`absolute top-1 w-5 h-5 bg-white rounded-full transition-transform duration-200 ${
                billingCycle === 'yearly' ? 'translate-x-8' : 'translate-x-1'
              }`} />
            </button>
            <span className={`text-sm font-medium ${
              billingCycle === 'yearly' ? 'text-foreground' : 'text-muted-foreground'
            }`}>
              Yearly
            </span>
            {billingCycle === 'yearly' && (
              <span className="bg-green-500/20 text-green-500 px-2 py-1 rounded-full text-xs font-medium">
                Save 20%
              </span>
            )}
          </div>
        </motion.div>

        {/* Pricing Cards */}
        <div className="grid lg:grid-cols-3 gap-8 mb-16">
          {pricingPlans.map((plan, index) => (
            <PricingCard 
              key={plan.id} 
              plan={plan} 
              index={index} 
              billingCycle={billingCycle}
            />
          ))}
        </div>

        {/* Features Comparison */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="mb-16"
        >
          <div className="text-center mb-8">
            <h2 className="text-3xl font-heading font-bold text-foreground mb-4">
              Compare Features
            </h2>
            <p className="text-muted-foreground">
              See what's included in each plan
            </p>
          </div>

          <div className="bg-card/50 backdrop-blur-xl rounded-2xl border border-border/50 overflow-hidden shadow-lg">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-secondary/20">
                  <tr>
                    <th className="text-left p-6 font-semibold text-foreground">Features</th>
                    <th className="text-center p-6 font-semibold text-foreground">Starter</th>
                    <th className="text-center p-6 font-semibold text-foreground">Professional</th>
                    <th className="text-center p-6 font-semibold text-foreground">Enterprise</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-t border-border/50">
                    <td className="p-6 text-muted-foreground">AI Requests per month</td>
                    <td className="p-6 text-center text-foreground">1,000</td>
                    <td className="p-6 text-center text-foreground">10,000</td>
                    <td className="p-6 text-center text-foreground">Unlimited</td>
                  </tr>
                  <tr className="border-t border-border/50 bg-secondary/10">
                    <td className="p-6 text-muted-foreground">AI Models Access</td>
                    <td className="p-6 text-center text-foreground">Basic</td>
                    <td className="p-6 text-center text-foreground">Advanced</td>
                    <td className="p-6 text-center text-foreground">All + Custom</td>
                  </tr>
                  <tr className="border-t border-border/50">
                    <td className="p-6 text-muted-foreground">Support Level</td>
                    <td className="p-6 text-center text-foreground">Standard</td>
                    <td className="p-6 text-center text-foreground">Priority</td>
                    <td className="p-6 text-center text-foreground">Dedicated</td>
                  </tr>
                  <tr className="border-t border-border/50 bg-secondary/10">
                    <td className="p-6 text-muted-foreground">Team Members</td>
                    <td className="p-6 text-center text-foreground">1</td>
                    <td className="p-6 text-center text-foreground">10</td>
                    <td className="p-6 text-center text-foreground">Unlimited</td>
                  </tr>
                  <tr className="border-t border-border/50">
                    <td className="p-6 text-muted-foreground">Data Storage</td>
                    <td className="p-6 text-center text-foreground">1GB</td>
                    <td className="p-6 text-center text-foreground">50GB</td>
                    <td className="p-6 text-center text-foreground">Unlimited</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </motion.div>

        {/* FAQ Section */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="mb-16"
        >
          <div className="text-center mb-8">
            <h2 className="text-3xl font-heading font-bold text-foreground mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-muted-foreground">
              Got questions? We've got answers.
            </p>
          </div>

          <div className="max-w-3xl mx-auto space-y-4">
            {faqs.map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="bg-card/50 backdrop-blur-xl rounded-2xl border border-border/50 overflow-hidden"
              >
                <button
                  onClick={() => setExpandedFAQ(expandedFAQ === index ? null : index)}
                  className="w-full p-6 text-left flex items-center justify-between hover:bg-secondary/10 transition-colors"
                >
                  <span className="font-semibold text-foreground">{faq.question}</span>
                  <ArrowRight className={`w-5 h-5 text-muted-foreground transition-transform ${
                    expandedFAQ === index ? 'rotate-90' : ''
                  }`} />
                </button>
                {expandedFAQ === index && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="px-6 pb-6"
                  >
                    <p className="text-muted-foreground">{faq.answer}</p>
                  </motion.div>
                )}
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Contact Section */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.8 }}
        >
          <div className="bg-gradient-to-r from-primary/10 to-accent/10 rounded-2xl p-8 border border-border/50 text-center">
            <h3 className="text-2xl font-heading font-bold text-foreground mb-4">
              Need a Custom Solution?
            </h3>
            <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
              Our enterprise team is ready to help you build a custom AI solution that fits your unique requirements.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <button className="flex items-center space-x-2 bg-primary text-primary-foreground px-6 py-3 rounded-xl hover:bg-primary/90 transition-colors">
                <Phone className="w-4 h-4" />
                <span>Schedule a Call</span>
              </button>
              <button className="flex items-center space-x-2 bg-secondary text-secondary-foreground px-6 py-3 rounded-xl hover:bg-secondary/80 transition-colors">
                <Mail className="w-4 h-4" />
                <span>Contact Sales</span>
              </button>
              <button className="flex items-center space-x-2 bg-accent text-accent-foreground px-6 py-3 rounded-xl hover:bg-accent/90 transition-colors">
                <MessageCircle className="w-4 h-4" />
                <span>Live Chat</span>
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}