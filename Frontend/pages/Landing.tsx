import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Shirt, User, Sparkles, ArrowRight, CheckCircle } from 'lucide-react';
import { Button, GlassCard } from '../components/ui/GlassComponents';

const Landing: React.FC = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { staggerChildren: 0.2 }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white overflow-x-hidden selection:bg-brand-purple/30">
      {/* Animated Background */}
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
         <div className="absolute top-[-10%] left-[-10%] w-[600px] h-[600px] bg-purple-700/30 rounded-full blur-[128px] animate-blob" />
         <div className="absolute top-[20%] right-[-5%] w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[128px] animate-blob animation-delay-2000" />
         <div className="absolute bottom-[-10%] left-[20%] w-[600px] h-[600px] bg-pink-600/20 rounded-full blur-[128px] animate-blob animation-delay-4000" />
      </div>

      {/* Navbar */}
      <nav className="relative z-50 flex items-center justify-between px-6 py-6 md:px-12 max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-purple to-brand-cyan flex items-center justify-center shadow-lg shadow-brand-purple/25">
            <span className="font-bold text-xl">O</span>
          </div>
          <span className="text-2xl font-bold tracking-tight">OutfitLens</span>
        </div>
        <div className="flex items-center gap-4">
          <Link to="/login">
            <Button variant="secondary" className="hidden md:flex">Sign In</Button>
          </Link>
          <Link to="/register">
            <Button>Get Started <ArrowRight size={16} /></Button>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <motion.section 
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="relative z-10 flex flex-col items-center text-center px-4 pt-20 pb-32 max-w-5xl mx-auto"
      >
        <motion.div variants={itemVariants} className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 backdrop-blur-md text-sm font-medium text-purple-200 mb-8">
          <Sparkles size={16} className="text-brand-cyan" />
          <span>AI-Powered Virtual Try-On Technology</span>
        </motion.div>
        
        <motion.h1 variants={itemVariants} className="text-5xl md:text-7xl font-bold tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-b from-white via-white to-gray-400">
          Transform Your Look <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-purple via-brand-pink to-brand-cyan">With AI Magic</span>
        </motion.h1>
        
        <motion.p variants={itemVariants} className="text-lg md:text-xl text-gray-400 max-w-2xl mb-10 leading-relaxed">
          Upload your photo, choose your clothing, and let our advanced AI instantly visualize how you'd look. No more dressing room queues.
        </motion.p>
        
        <motion.div variants={itemVariants} className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
          <Link to="/register" className="w-full sm:w-auto">
            <Button className="w-full h-14 text-lg">Start Generating Now</Button>
          </Link>
          <Link to="/login" className="w-full sm:w-auto">
            <Button variant="outline" className="w-full h-14 text-lg">View Demo</Button>
          </Link>
        </motion.div>
      </motion.section>

      {/* Features Grid */}
      <section className="relative z-10 px-4 pb-32 max-w-7xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8">
          {[
            { icon: <User size={32} />, title: "Upload Photo", desc: "Take a selfie or upload a full-body photo of yourself." },
            { icon: <Shirt size={32} />, title: "Choose Clothing", desc: "Upload an image of the clothing item you want to try on." },
            { icon: <Sparkles size={32} />, title: "Instant Magic", desc: "Our AI generates a realistic visualization in seconds." },
          ].map((feature, idx) => (
            <GlassCard key={idx} hoverEffect className="flex flex-col items-center text-center p-8">
              <div className="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center text-brand-cyan mb-6 border border-white/10 shadow-[inset_0_0_20px_rgba(255,255,255,0.05)]">
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
              <p className="text-gray-400">{feature.desc}</p>
            </GlassCard>
          ))}
        </div>
      </section>

      {/* How it works / Demo section */}
      <section className="relative z-10 px-4 pb-32">
        <div className="max-w-7xl mx-auto">
          <GlassCard className="p-8 md:p-12 border-white/10 bg-slate-800/30">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <h2 className="text-3xl md:text-4xl font-bold mb-6">Professional Results, <br/>Instantly.</h2>
                <div className="space-y-4">
                  {['Realistic fabric physics', 'Accurate body mapping', 'High resolution output', 'Preserves lighting & shadows'].map((item, i) => (
                    <div key={i} className="flex items-center gap-3">
                      <div className="p-1 rounded-full bg-green-500/20 text-green-400">
                        <CheckCircle size={16} />
                      </div>
                      <span className="text-gray-300">{item}</span>
                    </div>
                  ))}
                </div>
                <Link to="/register">
                  <Button className="mt-8">Try It Yourself</Button>
                </Link>
              </div>
              <div className="relative">
                 <div className="aspect-[4/3] rounded-2xl overflow-hidden border border-white/10 shadow-2xl relative bg-black/40">
                    <div className="absolute inset-0 flex items-center justify-center text-gray-500">
                         <div className="text-center">
                             <Sparkles className="w-12 h-12 mx-auto mb-2 opacity-50" />
                             <p>Interactive Demo Preview</p>
                         </div>
                    </div>
                    {/* Abstract representation of UI */}
                    <div className="absolute bottom-4 left-4 right-4 h-2 bg-white/20 rounded-full overflow-hidden">
                         <div className="h-full w-2/3 bg-brand-cyan"></div>
                    </div>
                 </div>
              </div>
            </div>
          </GlassCard>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/5 bg-slate-900/50 backdrop-blur-lg py-12">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2 opacity-75 hover:opacity-100 transition-opacity">
             <div className="w-6 h-6 rounded bg-brand-purple flex items-center justify-center text-xs font-bold">O</div>
             <span className="font-bold">OutfitLens</span>
          </div>
          <div className="text-gray-500 text-sm">
            © 2024 OutfitLens AI. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
