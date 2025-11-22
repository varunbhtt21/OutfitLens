import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuthStore } from '../store/authStore';
import { generationApi } from '../lib/api';
import { GlassCard, Button } from '../components/ui/GlassComponents';
import { Plus, ArrowRight, Image as ImageIcon, Sparkles, Zap } from 'lucide-react';
import { Generation } from '../types';
import { motion } from 'framer-motion';

const Dashboard: React.FC = () => {
  const { user } = useAuthStore();
  const [recentGens, setRecentGens] = useState<Generation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecent = async () => {
      try {
        const data = await generationApi.getHistory(1);
        setRecentGens(data.items.slice(0, 3)); // Take top 3
      } catch (e: any) {
        toast.error('Failed to load dashboard data');
        console.error("Failed to fetch dashboard data", e);
      } finally {
        setLoading(false);
      }
    };
    fetchRecent();
  }, []);

  const stats = [
    { label: 'Total Generations', value: '12', icon: <Sparkles size={20} className="text-brand-purple" /> },
    { label: 'Images Uploaded', value: '48', icon: <ImageIcon size={20} className="text-brand-cyan" /> },
    { label: 'Available Credits', value: 'Free', icon: <Zap size={20} className="text-yellow-400" /> },
  ];

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">Hello, {user?.full_name?.split(' ')[0]}! 👋</h1>
          <p className="text-gray-400">Ready to create your next look?</p>
        </div>
        <Link to="/generate">
          <Button className="shadow-lg shadow-brand-purple/25">
            <Plus size={18} /> Create New Generation
          </Button>
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat, idx) => (
          <GlassCard key={idx} className="flex items-center gap-4 p-6">
            <div className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center border border-white/10">
              {stat.icon}
            </div>
            <div>
              <p className="text-sm text-gray-400">{stat.label}</p>
              <p className="text-2xl font-bold">{stat.value}</p>
            </div>
          </GlassCard>
        ))}
      </div>

      {/* Recent Activity */}
      <section>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold">Recent Generations</h2>
          <Link to="/history" className="text-sm text-brand-cyan hover:underline flex items-center gap-1">
            View All <ArrowRight size={14} />
          </Link>
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
             <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-brand-purple"></div>
          </div>
        ) : recentGens.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {recentGens.map((gen) => (
              <motion.div key={gen.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                <GlassCard hoverEffect className="p-0 overflow-hidden group cursor-pointer h-full flex flex-col">
                  <div className="relative aspect-[3/4] overflow-hidden bg-black/20">
                    {gen.result_image ? (
                        <img src={gen.result_image.url} alt="Result" className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
                    ) : (
                        <div className="w-full h-full flex items-center justify-center text-gray-500 bg-white/5">
                           Processing...
                        </div>
                    )}
                    <div className={`absolute top-3 right-3 px-2 py-1 rounded-md text-xs font-bold backdrop-blur-md ${
                        gen.status === 'completed' ? 'bg-green-500/20 text-green-300 border border-green-500/20' : 
                        gen.status === 'failed' ? 'bg-red-500/20 text-red-300 border border-red-500/20' : 
                        'bg-blue-500/20 text-blue-300 border border-blue-500/20'
                    }`}>
                        {gen.status.toUpperCase()}
                    </div>
                  </div>
                  <div className="p-4 border-t border-white/5 mt-auto">
                    <p className="text-sm text-gray-400">Generated on</p>
                    <p className="text-sm font-medium">{new Date(gen.created_at).toLocaleDateString()}</p>
                  </div>
                </GlassCard>
              </motion.div>
            ))}
          </div>
        ) : (
            <GlassCard className="p-12 text-center">
                <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Sparkles className="text-gray-500" />
                </div>
                <h3 className="text-lg font-medium mb-2">No generations yet</h3>
                <p className="text-gray-400 mb-6">Start your first virtual try-on experience now.</p>
                <Link to="/generate">
                    <Button variant="secondary">Start Creating</Button>
                </Link>
            </GlassCard>
        )}
      </section>
    </div>
  );
};

export default Dashboard;
