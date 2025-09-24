import React from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/landing/Header';
import HeroSection from '../components/landing/HeroSection';
import OurSolution from '../components/landing/OurSolution';
import HowItWorks from '../components/landing/HowItWorks';
import ContactUs from '../components/landing/ContactUs';
import FeaturesGrid from '../components/landing/FeaturesGrid';
import Footer from '../components/landing/Footer';

const LandingPage = () => {
  const navigate = useNavigate();

  const handleStartAnalyzing = () => {
    navigate('/analyze');
  };

  return (
    <div className="bg-[#FFF8DC] font-sans text-gray-900 overflow-x-hidden kolam-dots relative">
      <Header onStartAnalyzing={handleStartAnalyzing} />
      <HeroSection onStartAnalyzing={handleStartAnalyzing} />
      <FeaturesGrid />
      <OurSolution />
      <HowItWorks />
      <ContactUs />
      <Footer />

      {/* Add keyframes for animation in a style tag */}
      <style jsx global>{`
        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        .animate-spin-slow {
           animation: spin-slow 20s linear infinite;
        }
      `}</style>
    </div>
  );
};

export default LandingPage;