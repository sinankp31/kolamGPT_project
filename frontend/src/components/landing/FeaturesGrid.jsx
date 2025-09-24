import React from 'react';

const FeaturesGrid = () => {
  const features = [
    {
      icon: '🔍',
      title: 'Pattern Recognition',
      description: 'Advanced AI identifies dots, lines, and complex patterns in your kolam images'
    },
    {
      icon: '📐',
      title: 'Mathematical Analysis',
      description: 'Graph theory and symmetry analysis reveal the mathematical beauty of traditional designs'
    },
    {
      icon: '🎭',
      title: 'Cultural Context',
      description: 'Learn about regional styles, historical significance, and artistic traditions'
    },
    {
      icon: '🤖',
      title: 'AI Interpretation',
      description: 'Get detailed explanations of pattern complexity, symmetry, and artistic elements'
    },
    {
      icon: '🎨',
      title: 'Digital Recreation',
      description: 'Generate beautiful digital versions of traditional kolam patterns'
    },
    {
      icon: '📚',
      title: 'Educational Insights',
      description: 'Understand the cultural and mathematical significance of South Indian art'
    }
  ];

  return (
    <section id="features" className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Powerful Features</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Experience the perfect fusion of traditional art and cutting-edge technology
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-gradient-to-br from-orange-50 to-yellow-50 p-6 rounded-xl hover:shadow-lg transition-shadow animate-fade-in-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesGrid;