import React, { useEffect, useState } from 'react';
import { generationApi } from '../lib/api';
import { GlassCard, Button } from '../components/ui/GlassComponents';
import { Generation } from '../types';
import { Calendar, ArrowRight } from 'lucide-react';

const History: React.FC = () => {
  const [history, setHistory] = useState<Generation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await generationApi.getHistory();
        setHistory(data.items);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) return <div className="flex justify-center p-20"><div className="animate-spin rounded-full h-8 w-8 border-2 border-brand-purple" /></div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold mb-6">Generation History</h1>
      
      {history.map((item) => (
        <GlassCard key={item.id} className="p-4 flex flex-col md:flex-row items-center gap-6 hover:bg-white/5 transition-colors">
          {/* Images Row */}
          <div className="flex items-center gap-4 flex-1">
             <div className="w-20 h-24 rounded-lg bg-black/20 overflow-hidden border border-white/10">
                 <img src={item.user_photo.url} className="w-full h-full object-cover opacity-80" alt="User" />
             </div>
             <div className="text-gray-500"><ArrowRight size={16} /></div>
             <div className="w-20 h-24 rounded-lg bg-black/20 overflow-hidden border border-white/10">
                 <img src={item.clothing_photo.url} className="w-full h-full object-cover opacity-80" alt="Cloth" />
             </div>
             <div className="text-brand-purple"><ArrowRight size={20} /></div>
             <div className="w-24 h-32 rounded-lg bg-black/40 overflow-hidden border border-brand-purple/30 shadow-lg shadow-brand-purple/10">
                 {item.result_image ? (
                    <img src={item.result_image.url} className="w-full h-full object-cover" alt="Result" />
                 ) : (
                    <div className="w-full h-full flex items-center justify-center text-xs text-gray-500">Pending</div>
                 )}
             </div>
          </div>

          {/* Meta */}
          <div className="flex flex-row md:flex-col items-center md:items-end gap-2 md:gap-1 min-w-[120px]">
            <div className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${
                item.status === 'completed' ? 'bg-green-500/20 text-green-400' : 'bg-blue-500/20 text-blue-400'
            }`}>
                {item.status}
            </div>
            <div className="flex items-center gap-1 text-xs text-gray-400">
                <Calendar size={12} />
                {new Date(item.created_at).toLocaleDateString()}
            </div>
            <Button variant="outline" className="text-xs py-1 h-8 mt-2">Details</Button>
          </div>
        </GlassCard>
      ))}
      
      {history.length === 0 && (
          <p className="text-center text-gray-400 py-12">No history found.</p>
      )}
    </div>
  );
};

export default History;
