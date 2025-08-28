"use client"

import { toast } from "sonner"
import { FloatingDock } from "@/components/ui/floating-dock"
import { 
  IconHome, 
  IconApps, 
  IconPresentation, 
  IconDashboard, 
  IconBook 
} from "@tabler/icons-react"

interface NavBarProps {
  className?: string
}

export default function NavBar({ className }: NavBarProps) {
  const handleDemoClick = () => {
    toast.loading("Opening demo...", { id: "demo-loading" })
    
    setTimeout(() => {
      toast.success("Demo loaded successfully!", { id: "demo-loading" })
      window.location.href = '/demo'
    }, 800)
  }

  const navigationItems = [
    {
      title: "Home",
      icon: <IconHome className="h-full w-full" />,
      href: "/",
    },
    {
      title: "Products",
      icon: <IconApps className="h-full w-full" />,
      href: "/products",
    },
    {
      title: "Demo",
      icon: <IconPresentation className="h-full w-full" />,
      href: "/demo",
      onClick: (e: React.MouseEvent) => {
        e.preventDefault()
        handleDemoClick()
      }
    },
    {
      title: "Dashboard",
      icon: <IconDashboard className="h-full w-full" />,
      href: "/dashboard",
    },
    {
      title: "Docs",
      icon: <IconBook className="h-full w-full" />,
      href: "/docs",
    },

  ]

  return (
    <div className={`fixed bottom-4 left-1/2 transform -translate-x-1/2 z-50 ${className || ""}`}>
      <FloatingDock
        items={navigationItems}
        desktopClassName="fixed bottom-4 left-1/2 transform -translate-x-1/2"
        mobileClassName="fixed bottom-4 right-4"
      />
    </div>
  )
}