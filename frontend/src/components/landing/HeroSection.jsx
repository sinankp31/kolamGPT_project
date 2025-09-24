import React from 'react';
import { Link } from 'react-router-dom';

const HeroSection = () => {
  return (
    <section className="pt-20 pb-16 bg-gradient-to-br from-orange-50 to-yellow-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6 animate-fade-in-up">
            Discover the Beauty of
            <span className="text-orange-600 block">Traditional Kolam Art</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
            Upload your kolam patterns and let AI analyze their mathematical beauty, cultural significance, and artistic elements. Experience the perfect blend of tradition and technology.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
            <Link
              to="/analyze"
              className="bg-orange-600 text-white px-8 py-4 rounded-lg hover:bg-orange-700 transition-colors font-semibold text-lg shadow-lg hover:shadow-xl"
            >
              Analyze Your Kolam
            </Link>
            <button className="border-2 border-orange-600 text-orange-600 px-8 py-4 rounded-lg hover:bg-orange-50 transition-colors font-semibold text-lg">
              Learn More
            </button>
          </div>
        </div>
        <div className="mt-16 relative">
          <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-4xl mx-auto">
            <div className="grid md:grid-cols-3 gap-8 text-center">
              <div className="animate-fade-in-up" style={{ animationDelay: '0.6s' }}>
                <div className="text-4xl mb-4">🔍</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">AI Analysis</h3>
                <p className="text-gray-600">Advanced computer vision analyzes dot patterns, symmetry, and mathematical properties</p>
              </div>
              <div className="animate-fade-in-up" style={{ animationDelay: '0.8s' }}>
                <div className="text-4xl mb-4">🎨</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Cultural Insights</h3>
                <p className="text-gray-600">Learn about regional styles, historical significance, and artistic techniques</p>
              </div>
              <div className="animate-fade-in-up" style={{ animationDelay: '1s' }}>
                <div className="text-4xl mb-4">✨</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Digital Recreation</h3>
                <p className="text-gray-600">Generate beautiful digital versions of your traditional kolam patterns</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;