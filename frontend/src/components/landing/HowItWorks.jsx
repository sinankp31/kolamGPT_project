import React from 'react';

const HowItWorks = () => {
  const steps = [
    {
      step: 1,
      title: 'Upload Your Kolam',
      description: 'Take a photo or upload an image of your kolam pattern',
      icon: '📸'
    },
    {
      step: 2,
      title: 'AI Analysis',
      description: 'Our advanced AI analyzes dots, lines, symmetry, and patterns',
      icon: '🤖'
    },
    {
      step: 3,
      title: 'Get Insights',
      description: 'Receive detailed analysis of mathematical properties and cultural significance',
      icon: '💡'
    },
    {
      step: 4,
      title: 'Digital Recreation',
      description: 'Generate a beautiful digital version of your traditional art',
      icon: '🎨'
    }
  ];

  return (
    <section id="how-it-works" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">How It Works</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Simple steps to unlock the beauty and wisdom of traditional kolam art
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <div
              key={step.step}
              className="text-center animate-fade-in-up"
              style={{ animationDelay: `${index * 0.2}s` }}
            >
              <div className="bg-orange-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">
                {step.icon}
              </div>
              <div className="bg-orange-600 text-white w-8 h-8 rounded-full flex items-center justify-center mx-auto mb-4 text-sm font-bold">
                {step.step}
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">{step.title}</h3>
              <p className="text-gray-600">{step.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;