"use client"

import { motion } from "framer-motion"
import { Zap } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function Header() {
  return (
    <motion.header
      className="fixed top-0 left-0 right-0 z-40 bg-background/80 backdrop-blur-md border-b border-border/40"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      <div className="container mx-auto flex items-center justify-between h-16 px-4 sm:px-6">
        {/* Logo */}
        <motion.div
          className="flex items-center space-x-2"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
        >
          <div className="relative">
            <Zap className="h-8 w-8 text-primary" />
            <div className="absolute inset-0 bg-primary/20 rounded-full blur-lg animate-pulse" />
          </div>
          <span className="font-heading font-bold text-xl text-foreground">
            Samsung EnnovateX
          </span>
        </motion.div>


      </div>
    </motion.header>
  )
}