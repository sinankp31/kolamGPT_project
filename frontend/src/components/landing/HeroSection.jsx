import React from 'react';
import { Sparkles } from 'lucide-react';

const HeroSection = ({ onStartAnalyzing }) => {
  return (
    <main className="container mx-auto px-4 sm:px-8 md:px-16 py-16 sm:py-24 text-center" style={{background: 'linear-gradient(135deg, #FFF8DC 0%, #FFE4B5 50%, #FFF8DC 100%)'}}>
      {/* Hero Section */}
      <div className="relative inline-block">
        <h1 className="text-6xl sm:text-8xl md:text-9xl font-black tracking-tighter leading-none">
          K<span className="relative inline-block">
            O
            {/* Green Sticker */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-24 h-24 sm:w-28 sm:h-28 bg-green-300 rounded-full flex items-center justify-center p-2 transform rotate-[-15deg]">
              <div className="w-full h-full border-2 border-dashed border-black rounded-full flex items-center justify-center">
                <span className="text-4xl">🎨</span>
              </div>
              {/* This is a simplified version of the circular text */}
              <p className="absolute text-[8px] sm:text-[10px] w-full h-full font-bold text-black uppercase tracking-wider text-center animate-spin-slow">
                SAYING GOODBYE TO BORING PATTERNS •
              </p>
            </div>
          </span>LAM
          <br />
          ON DEMAND
        </h1>

        {/* "Cruising on a Pattern Cloud" Sticker */}
        <div className="absolute top-[-2rem] right-[-3rem] sm:top-0 sm:right-[-4rem] md:right-[-6rem] bg-white p-4 border-2 border-black rounded-lg shadow-[8px_8px_0_0_#000] transform -rotate-6 w-48 sm:w-56">
           <p className="text-xs font-bold uppercase">HELLO, I AM</p>
           <p className="text-lg font-bold">Cruising on a Pattern Cloud ☁️</p>
        </div>
      </div>

      <p className="max-w-2xl mx-auto mt-8 text-lg sm:text-xl md:text-2xl font-medium text-gray-700">
        We take your kolam creation stress away, so you can focus on the bigger picture.
      </p>

      <button
        onClick={onStartAnalyzing}
        className="inline-block mt-12 bg-red-500 text-white text-sm sm:text-base font-bold py-4 px-10 rounded-lg shadow-lg hover:bg-red-600 transition-transform hover:scale-105"
      >
        START ANALYZING NOW
      </button>
    </main>
  );
};

export default HeroSection;