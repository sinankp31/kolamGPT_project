import React from 'react';

const Footer = () => {
  return (
    <section className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-16">
      <div className="max-w-6xl mx-auto text-center">

        {/* Main Heading */}
        <h1 className="text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-black text-gray-900 leading-tight mb-8">
          <span className="block">Precision of AI analysis.</span>
          <span className="block">Creativity of human artistry.</span>
          <span className="block">Heritage of traditional patterns.</span>
        </h1>

        {/* Subheading */}
        <div className="max-w-2xl mx-auto">
          <p className="text-base sm:text-lg lg:text-xl text-gray-600 leading-relaxed">
            Your kolam patterns tell stories of culture, tradition, and creativity.
            It's time to unlock their full potential, with a little help from Team Horizon.
          </p>
        </div>

      </div>
    </section>
  );
};

export default Footer;