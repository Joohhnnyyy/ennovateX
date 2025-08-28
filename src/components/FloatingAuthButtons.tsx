"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { LogIn } from "lucide-react"

export default function FloatingAuthButtons() {

  return (
    <motion.div
      className="fixed top-6 right-6 z-50 flex items-center space-x-3"
      initial={{ opacity: 0, y: -20, x: 20 }}
      animate={{ opacity: 1, y: 0, x: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      {/* Sign In Button */}
      <motion.div
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        transition={{ duration: 0.2 }}
      >
        <Button
          variant="ghost"
          size="sm"
          className="bg-background/80 backdrop-blur-md border border-border/40 text-foreground/80 hover:text-foreground hover:bg-muted/50 shadow-lg hover:shadow-xl transition-all duration-300"
          onClick={() => window.location.href = '/signin'}
        >
          <LogIn className="h-4 w-4 mr-2" />
          Sign in
        </Button>
      </motion.div>

    </motion.div>
  )
}