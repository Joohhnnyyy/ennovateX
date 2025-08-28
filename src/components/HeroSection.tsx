"use client"

import { motion, useMotionValue, useSpring, useTransform } from "framer-motion"
import { useEffect, useRef, useState } from "react"
import { Button } from "@/components/ui/button"
import { toast } from "sonner"
import { Book } from "lucide-react"

interface HeroSectionProps {
  onTryDemo?: () => void
  onViewDocs?: () => void
  className?: string
}

export default function HeroSection({ onTryDemo, onViewDocs, className = "" }: HeroSectionProps) {
  const [isLogoHovered, setIsLogoHovered] = useState(false)

  const handleTryDemo = () => {
    toast("Opening interactive demo…")
    setTimeout(() => {
      window.location.href = '/demo'
    }, 500)
    onTryDemo?.()
  }

  const handleViewDocs = () => {
    toast.loading("Opening documentation...", { id: "docs-loading" })
    
    setTimeout(() => {
      toast.success("Documentation loaded!", { id: "docs-loading" })
      window.location.href = '/docs'
    }, 800)
    onViewDocs?.()
  }

  const titleVariants = {
    hidden: { 
      opacity: 0, 
      y: 50,
      scale: 0.9
    },
    visible: {
      opacity: 1,
      y: 0,
      scale: 1
    }
  }

  const wordVariants = {
    hidden: { 
      opacity: 0, 
      y: 30,
      rotateX: 90
    },
    visible: {
      opacity: 1,
      y: 0,
      rotateX: 0
    }
  }

  const logoVariants = {
    initial: { 
      opacity: 0, 
      scale: 0.5, 
      rotateY: -180,
      y: -30
    },
    animate: {
      opacity: 1,
      scale: 1,
      rotateY: 0,
      y: 0
    }
  }

  const glowVariants = {
    animate: {
      opacity: [0.3, 0.6, 0.3],
      scale: [1, 1.05, 1]
    }
  }

  const glowTransition = {
    duration: 3,
    repeat: Infinity
  }

  return (
    <section
      className={`relative h-screen flex items-center justify-center bg-background overflow-hidden ${className}`}
      style={{ marginTop: 0, paddingTop: 0 }}
    >
      {/* Gradient Orbs Background */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-to-r from-[#1428A0] to-[#00ADEF] rounded-full blur-3xl opacity-20 animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gradient-to-l from-primary to-accent rounded-full blur-3xl opacity-15 animate-pulse delay-1000" />

      {/* Animated Background Vignette */}
      <motion.div
        className="absolute inset-0 bg-gradient-radial from-transparent via-background/50 to-background"
        animate={{
          scale: [1, 1.1, 1],
          opacity: [0.3, 0.5, 0.3]
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />

      <motion.div 
        className="relative z-10 text-center px-4 max-w-4xl mx-auto"
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{
          duration: 1.2,
          ease: [0.25, 0.46, 0.45, 0.94],
          staggerChildren: 0.15,
          delayChildren: 0.1
        }}
      >
        {/* Logo Emblem */}
        <motion.div
          className="mb-4 mt-4 relative inline-block"
          variants={logoVariants}
          initial="initial"
          animate="animate"
          transition={{
            duration: 1.5,
            ease: [0.175, 0.885, 0.32, 1.275],
            delay: 0.2
          }}
          onHoverStart={() => setIsLogoHovered(true)}
          onHoverEnd={() => setIsLogoHovered(false)}
        >
          {/* Glow Effect */}
          <motion.div
            className="absolute inset-0 rounded-full blur-xl bg-primary/30"
            variants={glowVariants}
            animate="animate"
            style={{ scale: 1.5 }}
          />
          
          {/* Samsung Logo SVG */}
          <motion.svg
            width="300"
            height="80"
            viewBox="0 0 120 32"
            className="relative z-10 drop-shadow-2xl"
            whileHover={{ scale: 1.05 }}
            initial={{ opacity: 0, scale: 0.8, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ 
              duration: 1.5, 
              delay: 0.8,
              ease: [0.25, 0.46, 0.45, 0.94]
            }}
          >
            <title>Samsung Logo</title>
            <desc>Samsung brand logo with gradient animation</desc>
            
            {/* Samsung Logo Path */}
            <motion.path
              d="M8 19.651v-1.14h3.994v1.45a1.334 1.334 0 0 0 1.494 1.346 1.3 1.3 0 0 0 1.444-1.007 1.833 1.833 0 0 0-.026-1.113c-.773-1.944-6.055-2.824-6.726-5.854a5.347 5.347 0 0 1-.025-2.02C8.567 8.88 10.705 8 13.359 8c2.113 0 5.025.492 5.025 3.754v1.062h-3.71v-.932a1.275 1.275 0 0 0-1.392-1.347 1.25 1.25 0 0 0-1.365 1.01 2.021 2.021 0 0 0 .026.777c.437 1.734 6.081 2.667 6.7 5.8a6.943 6.943 0 0 1 .025 2.46C18.307 23.068 16.091 24 13.412 24 10.6 24 8 22.99 8 19.651zm48.392-.051v-1.14h3.943v1.424A1.312 1.312 0 0 0 61.8 21.23a1.286 1.286 0 0 0 1.443-.984 1.759 1.759 0 0 0-.025-1.088c-.748-1.915-5.979-2.8-6.648-5.825a5.215 5.215 0 0 1-.026-1.994c.415-2.407 2.556-3.287 5.156-3.287 2.088 0 4.973.518 4.973 3.728v1.036h-3.684v-.906a1.268 1.268 0 0 0-1.365-1.346 1.2 1.2 0 0 0-1.34.984 2.017 2.017 0 0 0 .025.777c.412 1.734 6 2.641 6.623 5.747a6.806 6.806 0 0 1 .025 2.434c-.361 2.486-2.551 3.392-5.2 3.392-2.787.002-5.365-1.011-5.365-4.298zm14.121.545a5.876 5.876 0 0 1-.025-.985V8.44h3.762v11.055a4.111 4.111 0 0 0 .025.57 1.468 1.468 0 0 0 2.835 0 3.97 3.97 0 0 0 .026-.57V8.44H80.9v10.718c0 .285-.026.829-.026.985-.257 2.8-2.448 3.7-5.179 3.7s-4.924-.905-5.182-3.7zm30.974-.156a7.808 7.808 0 0 1-.052-.989v-6.288c0-.259.025-.725.051-.985.335-2.795 2.577-3.675 5.231-3.675 2.629 0 4.947.88 5.206 3.676a7.185 7.185 0 0 1 .025.985v.487h-3.762v-.824a3.1 3.1 0 0 0-.051-.57 1.553 1.553 0 0 0-2.964 0 3.088 3.088 0 0 0-.051.7v6.834a4.17 4.17 0 0 0 .026.57 1.472 1.472 0 0 0 1.571 1.09 1.406 1.406 0 0 0 1.52-1.087 2.09 2.09 0 0 0 .026-.57v-2.178h-1.52V14.99H112V19a7.674 7.674 0 0 1-.052.984c-.257 2.718-2.6 3.676-5.231 3.676s-4.973-.955-5.23-3.673zm-52.438 3.389l-.1-13.825-2.58 13.825h-3.762L40.055 9.553l-.1 13.825h-3.713l.309-14.912h6.056l1.881 11.651 1.881-11.651h6.055l.335 14.912zm-19.79 0l-2.01-13.825-2.062 13.825h-4.019L23.9 8.466h6.623l2.732 14.912zm62.977-.155L88.5 10.822l.206 12.4h-3.66V8.466h5.514l3.5 12.013-.201-12.013h3.685v14.758z"
              fill="url(#samsungGradient)"
              initial={{ pathLength: 0, opacity: 0 }}
              animate={{ pathLength: 1, opacity: 1 }}
              transition={{ duration: 2, delay: 0.5 }}
            />
            
            <defs>
              <linearGradient id="samsungGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#9b8cff" />
                <stop offset="50%" stopColor="#ffe89b" />
                <stop offset="100%" stopColor="#9b8cff" />
              </linearGradient>
            </defs>
          </motion.svg>

          {/* Hover Help Text */}
          <motion.div
            className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 text-xs text-muted-foreground whitespace-nowrap"
            initial={{ opacity: 0, y: 10 }}
            animate={{ 
              opacity: isLogoHovered ? 1 : 0,
              y: isLogoHovered ? 0 : 10
            }}
            transition={{ duration: 0.2 }}
          >
            Innovation in Motion
          </motion.div>
        </motion.div>

        {/* Headline */}
        <motion.div
          variants={titleVariants}
          initial="hidden"
          animate="visible"
          className="mb-6"
          transition={{
            duration: 1.0,
            ease: [0.25, 0.46, 0.45, 0.94],
            delay: 0.4
          }}
        >
          <motion.h1 
            className="text-5xl md:text-7xl lg:text-8xl font-heading font-bold leading-tight mb-4"
            variants={wordVariants}
            transition={{
              duration: 0.8,
              ease: [0.25, 0.46, 0.45, 0.94]
            }}
          >
            <motion.span 
              className="inline-block bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent"
              variants={wordVariants}
              transition={{
                duration: 0.8,
                ease: [0.25, 0.46, 0.45, 0.94],
                delay: 0.1
              }}
            >
              EnnovateX
            </motion.span>
          </motion.h1>
          
          <motion.p
            className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed"
            variants={wordVariants}
            transition={{
              duration: 0.8,
              ease: [0.25, 0.46, 0.45, 0.94],
              delay: 0.2
            }}
          >
            Transforming ideas into reality through cutting-edge innovation and seamless digital experiences
          </motion.p>
        </motion.div>

        {/* CTA Buttons */}
        <motion.div
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          initial={{ opacity: 0, y: 40, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ 
            delay: 0.8, 
            duration: 0.8,
            ease: [0.25, 0.46, 0.45, 0.94]
          }}
        >
          <Button
            size="lg"
            onClick={handleTryDemo}
            className="relative overflow-hidden bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary text-primary-foreground font-semibold px-8 py-3 rounded-full transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-primary/25 focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-background"
          >
            <motion.span
              className="relative z-10"
              whileTap={{ scale: 0.95 }}
            >
              Try Demo
            </motion.span>
            
            {/* Hover Glow Effect */}
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-primary/20 to-primary/10 rounded-full blur-sm"
              initial={{ scale: 0, opacity: 0 }}
              whileHover={{ scale: 1.2, opacity: 1 }}
              transition={{ duration: 0.3 }}
            />
          </Button>

          <Button
            variant="outline"
            size="lg"
            onClick={handleViewDocs}
            className="relative group font-semibold px-8 py-3 rounded-full border-2 border-border hover:border-primary/70 hover:bg-gradient-to-r hover:from-primary/10 hover:to-primary/5 transition-all duration-500 hover:scale-105 focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-background overflow-hidden backdrop-blur-sm"
          >
            <motion.span 
              whileTap={{ scale: 0.95 }}
              className="relative z-10 flex items-center gap-2"
            >
              <Book className="w-5 h-5" />
              View Documentation
            </motion.span>
            
            {/* Animated background gradient */}
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-primary/20 via-primary/10 to-transparent opacity-0 group-hover:opacity-100"
              initial={{ x: '-100%' }}
              whileHover={{ x: '100%' }}
              transition={{ duration: 0.6, ease: "easeInOut" }}
            />
            
            {/* Glow effect */}
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-primary/30 to-primary/20 rounded-full blur-md opacity-0 group-hover:opacity-50"
              initial={{ scale: 0.8 }}
              whileHover={{ scale: 1.1 }}
              transition={{ duration: 0.3 }}
            />
          </Button>
        </motion.div>
      </motion.div>
    </section>
  )
}