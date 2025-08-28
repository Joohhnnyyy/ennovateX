"use client"

import { motion } from "framer-motion"
import { Zap } from "lucide-react"

export default function FloatingLogo() {
  return (
    <motion.div
      className="fixed top-6 left-6 z-50 flex items-center space-x-2"
      initial={{ opacity: 0, y: -20, x: -20 }}
      animate={{ opacity: 1, y: 0, x: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      <motion.div
        className="flex items-center space-x-2 bg-background/80 backdrop-blur-md border border-border/40 rounded-full px-4 py-2 shadow-lg"
        whileHover={{ scale: 1.05 }}
        transition={{ duration: 0.2 }}
      >
        <div className="relative">
          <Zap className="h-6 w-6 text-primary" />
          <div className="absolute inset-0 bg-primary/20 rounded-full blur-lg animate-pulse" />
        </div>
        <span className="font-heading font-bold text-lg text-foreground">
          Samsung EnnovateX
        </span>
      </motion.div>
    </motion.div>
  )
}