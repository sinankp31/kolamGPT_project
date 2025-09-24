import React from 'react';

const AnalysisDisplay = ({ analysis }) => {
  if (!analysis) return null;

  const { original_image, analysis: analysisData, description, regenerated_image } = analysis;

  const getColorClass = (index) => {
    if (index % 4 === 0) return 'bg-orange-100 text-orange-700';
    if (index % 4 === 1) return 'bg-blue-100 text-blue-700';
    if (index % 4 === 2) return 'bg-purple-100 text-purple-700';
    return 'bg-pink-100 text-pink-700';
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">Kolam Analysis Results</h2>

      {/* Original Image */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Original Image</h3>
        <div className="flex justify-center">
          <img
            src={original_image}
            alt="Original kolam"
            className="max-w-full h-auto rounded-lg shadow-md"
          />
        </div>
      </div>

      {/* Analysis Summary */}
      <div className="grid md:grid-cols-2 gap-6 mb-8">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Pattern Analysis</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="font-medium text-gray-700">Dot Count:</span>
              <span className="text-orange-600 font-bold">{analysisData.dot_count}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="font-medium text-gray-700">Line Count:</span>
              <span className="text-orange-600 font-bold">{analysisData.line_count}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="font-medium text-gray-700">Symmetry Score:</span>
              <span className="text-orange-600 font-bold">{analysisData.symmetry_score}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="font-medium text-gray-700">Grid Pattern:</span>
              <span className="text-orange-600 font-bold">{analysisData.grid_pattern}</span>
            </div>
          </div>
        </div>

        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Key Features</h3>
          <div className="space-y-2">
            {description.key_features.map((feature, index) => (
              <div
                key={index}
                className={`p-3 rounded-lg ${getColorClass(index)}`}
              >
                <div className="flex items-center gap-2">
                  <span className="text-sm">✨</span>
                  <span className="text-sm font-medium">{feature}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Description */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Cultural & Artistic Interpretation</h3>
        <div className="bg-gradient-to-r from-orange-50 to-yellow-50 p-6 rounded-lg">
          <p className="text-gray-700 leading-relaxed">{description.interpretation}</p>
        </div>
      </div>

      {/* Regenerated Image */}
      {regenerated_image && (
        <div className="mb-8">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Digital Recreation</h3>
          <div className="flex justify-center">
            <img
              src={regenerated_image}
              alt="Regenerated kolam"
              className="max-w-full h-auto rounded-lg shadow-md"
            />
          </div>
        </div>
      )}

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