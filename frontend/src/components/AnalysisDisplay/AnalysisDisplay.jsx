import React from 'react';
import LoadingIndicator from '../common/LoadingIndicator';

const AnalysisDisplay = ({ result, isLoading }) => {
  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="relative">
          <LoadingIndicator />
          <div className="absolute -top-4 -right-4 bg-yellow-400 text-black rounded-full p-2 text-sm">
            ✨
          </div>
        </div>
        <p className="mt-6 text-lg font-medium text-orange-700">AI is analyzing your beautiful kolam art...</p>
        <p className="text-sm text-gray-600 mt-2">This may take a few moments</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">🎨</div>
        <p className="text-lg font-medium text-gray-600">Ready to analyze your kolam masterpiece!</p>
        <p className="text-sm text-gray-500 mt-2">Upload an image to see AI-powered insights</p>
      </div>
    );
  }

  if (result.error) {
    return (
      <div className="text-center py-12 bg-red-50 border-2 border-red-200 rounded-2xl">
        <div className="text-4xl mb-4">😅</div>
        <p className="text-red-700 font-medium mb-2">Oops! Something went wrong</p>
        <p className="text-red-600 text-sm">{result.error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Success Message */}
      <div className="text-center bg-green-50 border-2 border-green-200 rounded-2xl p-6">
        <div className="text-4xl mb-2">🎉</div>
        <h3 className="text-lg font-bold text-green-800 mb-1">Analysis Complete!</h3>
        <p className="text-green-700">Your kolam has been beautifully analyzed</p>
      </div>

      {/* Images Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="relative">
          <div className="bg-gradient-to-br from-blue-400 to-blue-600 p-1 rounded-2xl">
            <div className="bg-white rounded-xl p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-bold text-gray-800">Your Original Art</h3>
                <div className="bg-blue-100 text-blue-700 px-2 py-1 rounded-full text-xs font-medium">
                  📸 Uploaded
                </div>
              </div>
              <img src={result.original_image} alt="Original Kolam" className="w-full rounded-lg shadow-lg" />
            </div>
          </div>
        </div>

        <div className="relative">
          <div className="bg-gradient-to-br from-purple-400 to-pink-400 p-1 rounded-2xl">
            <div className="bg-white rounded-xl p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-bold text-gray-800">AI Regenerated</h3>
                <div className="bg-purple-100 text-purple-700 px-2 py-1 rounded-full text-xs font-medium">
                  🤖 AI Magic
                </div>
              </div>
              <img src={result.regenerated_image} alt="Regenerated Kolam" className="w-full rounded-lg shadow-lg" />
            </div>
          </div>
        </div>
      </div>

      {/* Analysis Details */}
      <div className="bg-gradient-to-br from-orange-50 to-yellow-50 border-2 border-orange-200 rounded-2xl overflow-hidden">
        <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="text-2xl">🔍</div>
            <h3 className="text-xl font-bold">{result.description.title}</h3>
          </div>
        </div>
        <div className="p-6">
          <div className="grid gap-4">
            {Object.entries(result.description).filter(([key]) => key !== 'title').map(([key, item], index) => (
              <div key={key} className="bg-white rounded-xl p-4 shadow-sm border border-orange-100">
                <div className="flex items-start gap-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                    index % 4 === 0 ? 'bg-blue-100 text-blue-700' :
                    index % 4 === 1 ? 'bg-green-100 text-green-700' :
                    index % 4 === 2 ? 'bg-purple-100 text-purple-700' :
                    'bg-pink-100 text-pink-700'
                  }`}>
                    {index + 1}
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-bold text-orange-700 uppercase tracking-wide mb-1">
                      {item.label}
                    </div>
                    <div className="text-gray-800 leading-relaxed">
                      {item.value}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Fun Footer */}
      <div className="text-center">
        <div className="inline-flex items-center gap-4 bg-gradient-to-r from-pink-100 to-purple-100 text-purple-700 px-6 py-3 rounded-full text-sm font-medium shadow-lg">
          <span className="text-lg">🎨</span>
          <span>Keep creating beautiful kolam art!</span>
          <span className="text-lg">✨</span>
        </div>
      </div>
    </div>
  );
};

export default AnalysisDisplay;