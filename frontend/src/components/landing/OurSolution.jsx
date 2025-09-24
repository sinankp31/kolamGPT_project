import React from 'react';

const OurSolution = () => {
  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-4xl font-bold text-gray-900 mb-6">
              Bridging Tradition and Technology
            </h2>
            <p className="text-lg text-gray-600 mb-6">
              KolamGPT combines the ancient wisdom of South Indian kolam art with modern AI technology.
              Our platform not only analyzes your patterns but also educates you about the rich cultural
              heritage behind each design.
            </p>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="bg-orange-100 p-2 rounded-lg">
                  <span className="text-orange-600">✓</span>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">Preserve Cultural Heritage</h3>
                  <p className="text-gray-600">Help keep traditional art forms alive through digital innovation</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-orange-100 p-2 rounded-lg">
                  <span className="text-orange-600">✓</span>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">Educational Insights</h3>
                  <p className="text-gray-600">Learn about mathematical principles and regional variations</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-orange-100 p-2 rounded-lg">
                  <span className="text-orange-600">✓</span>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">Community Building</h3>
                  <p className="text-gray-600">Connect with fellow kolam enthusiasts worldwide</p>
                </div>
              </div>
            </div>
          </div>
          <div className="relative">
            <div className="bg-gradient-to-br from-orange-400 to-pink-400 p-1 rounded-2xl">
              <div className="bg-white rounded-xl p-8">
                <div className="text-center">
                  <div className="text-6xl mb-4">🎨✨</div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-4">Experience the Magic</h3>
                  <p className="text-gray-600 mb-6">
                    Upload your kolam and watch as AI reveals the hidden mathematical beauty and cultural significance of your art.
                  </p>
                  <div className="bg-orange-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-700 italic">
                      "KolamGPT has helped me understand the deeper meaning behind the patterns my grandmother used to draw every morning."
                    </p>
                    <p className="text-sm font-medium text-orange-600 mt-2">- Priya S., Chennai</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default OurSolution;