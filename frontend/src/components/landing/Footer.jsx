import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-4 gap-8">
          <div className="col-span-2">
            <div className="text-2xl font-bold text-orange-400 mb-4">🎨 KolamGPT</div>
            <p className="text-gray-300 mb-4">
              Bridging the gap between traditional South Indian kolam art and modern technology.
              Discover the mathematical beauty and cultural significance of kolam patterns.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-orange-400 transition-colors">
                <span className="sr-only">Facebook</span>
                📘
              </a>
              <a href="#" className="text-gray-400 hover:text-orange-400 transition-colors">
                <span className="sr-only">Twitter</span>
                🐦
              </a>
              <a href="#" className="text-gray-400 hover:text-orange-400 transition-colors">
                <span className="sr-only">Instagram</span>
                📷
              </a>
            </div>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li><a href="#features" className="text-gray-400 hover:text-orange-400 transition-colors">Features</a></li>
              <li><a href="#how-it-works" className="text-gray-400 hover:text-orange-400 transition-colors">How It Works</a></li>
              <li><a href="#contact" className="text-gray-400 hover:text-orange-400 transition-colors">Contact</a></li>
              <li><a href="/analyze" className="text-gray-400 hover:text-orange-400 transition-colors">Try Now</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">About</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-400 hover:text-orange-400 transition-colors">About Kolam Art</a></li>
              <li><a href="#" className="text-gray-400 hover:text-orange-400 transition-colors">Cultural Significance</a></li>
              <li><a href="#" className="text-gray-400 hover:text-orange-400 transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="text-gray-400 hover:text-orange-400 transition-colors">Terms of Service</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-8 pt-8 text-center">
          <p className="text-gray-400">
            © 2024 KolamGPT. Preserving the beauty of traditional art through technology.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;