import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center">
            <div className="text-2xl font-bold text-orange-600">🎨 KolamGPT</div>
          </div>
          <nav className="hidden md:flex space-x-8">
            <a href="#features" className="text-gray-700 hover:text-orange-600 transition-colors">Features</a>
            <a href="#how-it-works" className="text-gray-700 hover:text-orange-600 transition-colors">How It Works</a>
            <a href="#contact" className="text-gray-700 hover:text-orange-600 transition-colors">Contact</a>
          </nav>
          <Link
            to="/analyze"
            className="bg-orange-600 text-white px-6 py-2 rounded-lg hover:bg-orange-700 transition-colors font-medium"
          >
            Try Now
          </Link>
        </div>
      </div>
    </header>
  );
};

export default Header;