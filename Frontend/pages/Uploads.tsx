import React, { useEffect, useState } from 'react';
import { imageApi } from '../lib/api';
import { GlassCard } from '../components/ui/GlassComponents';
import { ImageModel } from '../types';
import { Trash2, Eye } from 'lucide-react';

const Uploads: React.FC = () => {
  const [images, setImages] = useState<ImageModel[]>([]);

  useEffect(() => {
    imageApi.getAll().then(res => setImages(res.items));
  }, []);

  return (
    <div>
       <h1 className="text-2xl font-bold mb-6">My Uploads</h1>
       <div className="columns-2 md:columns-3 lg:columns-4 gap-4 space-y-4">
          {images.map(img => (
              <div key={img.id} className="break-inside-avoid relative group rounded-xl overflow-hidden">
                  <img src={img.url} alt="Upload" className="w-full rounded-xl border border-white/10" />
                  <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-4 backdrop-blur-sm">
                      <button className="p-2 rounded-full bg-white/10 hover:bg-white/20 text-white transition-colors"><Eye size={20} /></button>
                      <button className="p-2 rounded-full bg-red-500/20 hover:bg-red-500/40 text-red-300 transition-colors"><Trash2 size={20} /></button>
                  </div>
                  <div className="absolute bottom-2 left-2 px-2 py-1 bg-black/50 rounded text-[10px] uppercase tracking-wider font-bold text-gray-300">
                      {img.image_type.replace('_', ' ')}
                  </div>
              </div>
          ))}
       </div>
    </div>
  );
};

export default Uploads;
