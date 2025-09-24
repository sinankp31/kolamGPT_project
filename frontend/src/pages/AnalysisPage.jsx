import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/landing/Header';
import ImageUpload from '../components/ImageUpload/ImageUpload';
import AnalysisDisplay from '../components/AnalysisDisplay/AnalysisDisplay';
import { analyzeKolamApi } from '../services/api';

const AnalysisPage = () => {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleAnalyzeImage = async (uploadedImage) => {
    if (!uploadedImage) return;

    setIsLoading(true);
    setAnalysisResult(null);

    try {
      const result = await analyzeKolamApi(uploadedImage);
      setAnalysisResult(result);
    } catch (error) {
      console.error("API Call failed:", error);
      setAnalysisResult({ error: `Oops! I encountered an error: ${error.message}. Please ensure the backend server is running and check the console for details.` });
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoHome = () => {
    navigate('/');
    setAnalysisResult(null);
    setIsLoading(false);
  };

  return (
    <div className="bg-[#FFF8DC] font-sans text-gray-900 overflow-x-hidden min-h-screen">
      <Header onStartAnalyzing={handleGoHome} showNav={false} />
      <main className="container mx-auto px-4 sm:px-8 md:px-16 py-8" style={{background: 'linear-gradient(135deg, #FFF8DC 0%, #FFE4B5 50%, #FFF8DC 100%)'}}>
        <div className="max-w-6xl mx-auto">
          {/* Hero Section for Analysis */}
          <div className="text-center mb-16 relative">
            <div className="inline-flex items-center gap-2 bg-orange-200 text-orange-800 px-4 py-2 rounded-full text-sm font-medium mb-8">
              <span className="w-2 h-2 bg-orange-500 rounded-full"></span>
              AI Analysis Studio
            </div>

            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              Analyze Your <span className="text-orange-600">Kolam Designs</span>
            </h1>

            <p className="text-xl sm:text-2xl text-gray-700 max-w-4xl mx-auto mb-10 leading-relaxed">
              Upload your kolam patterns and let our AI analyze symmetry, patterns, and provide detailed insights about your traditional art.
            </p>

            {/* Decorative sticker */}
            <div className="absolute top-0 right-0 bg-yellow-300 p-4 border-2 border-black rounded-lg shadow-[8px_8px_0_0_#000] transform rotate-12 hidden md:block">
              <div className="text-sm font-bold text-black">🎨 AI MAGIC</div>
            </div>
          </div>

          {/* Upload and Analysis Section */}
          <div className="flex flex-col lg:flex-row gap-8 mb-12">
            {/* Upload Area - Fixed Width */}
            <div className="lg:w-96 flex-shrink-0">
              <div className="bg-white rounded-2xl shadow-xl p-8 border-2 border-orange-200 sticky top-8">
                <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Upload Your Kolam</h2>
                <ImageUpload onAnalyze={handleAnalyzeImage} isLoading={isLoading} />
              </div>
            </div>

            {/* Analysis Results - Flexible Width */}
            <div className="flex-1">
              <div className="bg-white rounded-2xl shadow-xl p-8 border-2 border-blue-200">
                <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Analysis Results</h2>
                <AnalysisDisplay result={analysisResult} isLoading={isLoading} />
              </div>
            </div>
          </div>

          {/* Fun Elements */}
          <div className="text-center">
            <div className="inline-flex items-center gap-4 bg-gradient-to-r from-green-200 to-blue-200 text-green-800 px-8 py-4 rounded-full text-lg font-medium shadow-lg">
              <span className="text-xl">✨</span>
              <span>Powered by Advanced AI Technology</span>
              <span className="text-xl">🎨</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default AnalysisPage;