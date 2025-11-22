import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { imageApi, generationApi } from '../lib/api';
import { GlassCard, Button } from '../components/ui/GlassComponents';
import { UploadCloud, ArrowRight, ArrowLeft, Check, Loader2, Sparkles, Download, Share2, X } from 'lucide-react';
import { ImageModel, GenerationStatus } from '../types';
import { motion, AnimatePresence } from 'framer-motion';

const STEPS = [
  { id: 1, title: 'Upload Your Photo' },
  { id: 2, title: 'Upload Clothing' },
  { id: 3, title: 'Generate' },
  { id: 4, title: 'Result' },
];

const Generate: React.FC = () => {
  const [step, setStep] = useState(1);
  const [userPhoto, setUserPhoto] = useState<ImageModel | null>(null);
  const [clothingPhoto, setClothingPhoto] = useState<ImageModel | null>(null);
  const [generationId, setGenerationId] = useState<string | null>(null);
  const [resultImage, setResultImage] = useState<ImageModel | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Upload handling
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;

    const file = e.target.files[0];
    setLoading(true);
    try {
      const type = step === 1 ? 'user_photo' : 'clothing_photo';
      const uploaded = await imageApi.upload(file, type);
      if (step === 1) {
        setUserPhoto(uploaded);
        toast.success('Photo uploaded successfully!');
      } else {
        setClothingPhoto(uploaded);
        toast.success('Clothing photo uploaded successfully!');
      }
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to upload image');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    if (!userPhoto || !clothingPhoto) return;
    setLoading(true);
    setStep(4);

    try {
      const gen = await generationApi.create(userPhoto.id, clothingPhoto.id);
      setGenerationId(gen.id);
      toast.loading('Generating your outfit...', { id: 'generation' });
      pollStatus(gen.id);
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to start generation');
      setLoading(false);
    }
  };

  const pollStatus = async (id: string) => {
    const interval = setInterval(async () => {
      try {
        const statusData = await generationApi.getStatus(id);
        if (statusData.status === GenerationStatus.COMPLETED && statusData.result_image) {
          clearInterval(interval);
          setResultImage(statusData.result_image);
          setLoading(false);
          toast.success('Outfit generated successfully!', { id: 'generation' });
        } else if (statusData.status === GenerationStatus.FAILED) {
          clearInterval(interval);
          setError(statusData.error_message || "Generation failed");
          setLoading(false);
          toast.error(statusData.error_message || 'Generation failed', { id: 'generation' });
        }
      } catch (e) {
        clearInterval(interval);
        setError("Network error while polling");
        setLoading(false);
        toast.error('Network error while processing', { id: 'generation' });
      }
    }, 2000);
  };

  const reset = () => {
    setStep(1);
    setUserPhoto(null);
    setClothingPhoto(null);
    setGenerationId(null);
    setResultImage(null);
    setError('');
  };

  // --- Sub-components for steps ---

  const UploadStep = ({ title, currentImage }: { title: string, currentImage: ImageModel | null }) => (
    <div className="text-center">
      <h2 className="text-2xl font-bold mb-6">{title}</h2>
      
      <div 
        onClick={() => fileInputRef.current?.click()}
        className={`
          border-2 border-dashed rounded-2xl p-10 cursor-pointer transition-all duration-300 group
          ${currentImage ? 'border-green-500/50 bg-green-500/5' : 'border-white/20 hover:border-brand-cyan/50 hover:bg-white/5'}
        `}
      >
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileChange} 
          className="hidden" 
          accept="image/jpeg,image/png,image/webp"
        />
        
        {currentImage ? (
          <div className="relative inline-block">
             <img src={currentImage.url} alt="Preview" className="max-h-64 rounded-lg shadow-lg mx-auto" />
             <div className="absolute -top-2 -right-2 bg-green-500 text-white rounded-full p-1">
                <Check size={16} />
             </div>
             <p className="mt-4 text-green-400 font-medium">Image Uploaded</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="w-16 h-16 bg-white/10 rounded-full flex items-center justify-center mx-auto group-hover:scale-110 transition-transform text-gray-300">
              <UploadCloud size={32} />
            </div>
            <div>
              <p className="text-lg font-medium">Click to upload or drag and drop</p>
              <p className="text-sm text-gray-500 mt-2">JPG, PNG or WEBP (Max 10MB)</p>
            </div>
          </div>
        )}
      </div>

      {loading && <p className="mt-4 text-brand-cyan animate-pulse">Uploading...</p>}
    </div>
  );

  const ReviewStep = () => (
    <div className="space-y-8">
      <div className="grid md:grid-cols-2 gap-8">
        <div className="space-y-2">
           <p className="font-medium text-gray-400 text-center">Your Photo</p>
           <div className="aspect-[3/4] rounded-xl overflow-hidden border border-white/10 bg-black/20 relative">
              <img src={userPhoto?.url} className="w-full h-full object-cover" alt="User" />
           </div>
        </div>
        <div className="space-y-2">
           <p className="font-medium text-gray-400 text-center">Clothing Item</p>
           <div className="aspect-[3/4] rounded-xl overflow-hidden border border-white/10 bg-black/20 relative">
              <img src={clothingPhoto?.url} className="w-full h-full object-cover" alt="Cloth" />
           </div>
        </div>
      </div>
    </div>
  );

  const ResultStep = () => (
    <div className="text-center py-4">
      {loading ? (
        <div className="py-20 space-y-6">
           <div className="relative w-32 h-32 mx-auto">
              <div className="absolute inset-0 rounded-full border-4 border-white/5"></div>
              <div className="absolute inset-0 rounded-full border-4 border-t-brand-purple border-r-transparent border-b-transparent border-l-transparent animate-spin"></div>
              <Sparkles className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-brand-purple animate-pulse" />
           </div>
           <div>
             <h3 className="text-xl font-bold animate-pulse">Generating your look...</h3>
             <p className="text-gray-400 mt-2">This usually takes about 10-15 seconds.</p>
           </div>
        </div>
      ) : resultImage ? (
        <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
           <div className="max-w-md mx-auto rounded-2xl overflow-hidden border border-white/20 shadow-[0_0_50px_rgba(124,58,237,0.3)] mb-8">
              <img src={resultImage.url} alt="Result" className="w-full h-auto" />
           </div>
           <h2 className="text-2xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-300">Look Transformed! ✨</h2>
           <div className="flex justify-center gap-4">
              <Button variant="secondary" icon={<Download size={18} />} onClick={() => window.open(resultImage.url, '_blank')}>Download</Button>
              <Button variant="outline" icon={<Share2 size={18} />}>Share</Button>
              <Button onClick={reset}>Create Another</Button>
           </div>
        </div>
      ) : (
        <div className="py-10">
           <div className="text-red-400 mb-4">
             <X size={48} className="mx-auto" />
           </div>
           <p className="text-lg text-red-300">{error || "Something went wrong."}</p>
           <Button variant="outline" className="mt-6" onClick={() => setStep(3)}>Try Again</Button>
        </div>
      )}
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto">
      {/* Progress Bar */}
      <div className="mb-12 relative">
        <div className="absolute top-1/2 left-0 w-full h-1 bg-white/10 -translate-y-1/2 rounded-full z-0" />
        <div 
          className="absolute top-1/2 left-0 h-1 bg-brand-purple -translate-y-1/2 rounded-full z-0 transition-all duration-500" 
          style={{ width: `${((step - 1) / 3) * 100}%` }} 
        />
        <div className="relative z-10 flex justify-between">
          {STEPS.map((s) => (
            <div key={s.id} className="flex flex-col items-center gap-2">
              <div 
                className={`
                  w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold border-2 transition-colors duration-300
                  ${step >= s.id ? 'bg-brand-purple border-brand-purple text-white' : 'bg-slate-900 border-white/20 text-gray-500'}
                `}
              >
                {step > s.id ? <Check size={14} /> : s.id}
              </div>
              <span className={`text-xs font-medium ${step >= s.id ? 'text-white' : 'text-gray-600'}`}>{s.title}</span>
            </div>
          ))}
        </div>
      </div>

      <GlassCard className="p-8 md:p-12 min-h-[500px] flex flex-col justify-center relative">
        <AnimatePresence mode="wait">
          <motion.div 
             key={step}
             initial={{ opacity: 0, x: 20 }}
             animate={{ opacity: 1, x: 0 }}
             exit={{ opacity: 0, x: -20 }}
             className="w-full"
          >
            {step === 1 && <UploadStep title="Upload Your Photo" currentImage={userPhoto} />}
            {step === 2 && <UploadStep title="Upload Clothing Item" currentImage={clothingPhoto} />}
            {step === 3 && <ReviewStep />}
            {step === 4 && <ResultStep />}
          </motion.div>
        </AnimatePresence>

        {/* Controls */}
        {!loading && step < 4 && (
          <div className="flex justify-between mt-12 pt-8 border-t border-white/5">
            <Button 
              variant="secondary" 
              onClick={() => setStep(p => p - 1)} 
              disabled={step === 1}
              className={step === 1 ? 'invisible' : ''}
            >
              <ArrowLeft size={18} /> Back
            </Button>

            <Button 
              onClick={step === 3 ? handleGenerate : () => setStep(p => p + 1)} 
              disabled={
                (step === 1 && !userPhoto) || 
                (step === 2 && !clothingPhoto)
              }
            >
              {step === 3 ? (
                  <>Generate Look <Sparkles size={18} className="ml-1" /></>
              ) : (
                  <>Next Step <ArrowRight size={18} /></>
              )}
            </Button>
          </div>
        )}
      </GlassCard>
    </div>
  );
};

export default Generate;
