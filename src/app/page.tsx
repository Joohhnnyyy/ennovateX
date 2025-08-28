import NavBar from "@/components/NavBar"


import HeroSection from "@/components/HeroSection"
import FeaturesSection from "@/components/FeaturesSection"
import DashboardPanel from "@/components/DashboardPanel"
import PerformanceCharts from "@/components/PerformanceCharts"
import Footer from "@/components/Footer"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background pb-20" style={{ margin: 0, padding: 0 }}>

      

      
      {/* Floating Navigation */}
      <NavBar />
      
      {/* Main Content Sections */}
      <main className="relative">
        {/* Hero Section - Full viewport height */}
        <section>
          <HeroSection />
        </section>

        {/* Features Section - Full width with container */}
        <section className="py-24">
          <FeaturesSection />
        </section>



        {/* Dashboard Panel - Contained */}
        <section className="py-24">
          <div className="container mx-auto px-6">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-heading font-bold mb-4">
                Dashboard Preview
              </h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Get a glimpse of your command center with real-time insights
              </p>
            </div>
            <DashboardPanel />
          </div>
        </section>

        {/* Performance Charts - Full width contained */}
        <section className="py-24 bg-muted/30">
          <div className="container mx-auto px-6">
            <PerformanceCharts />
          </div>
        </section>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  )
}