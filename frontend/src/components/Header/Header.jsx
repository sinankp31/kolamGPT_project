import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="flex items-center">
            <div className="text-2xl font-bold text-orange-600">🎨 KolamGPT</div>
          </Link>
          <nav className="flex space-x-6">
            <Link to="/" className="text-gray-700 hover:text-orange-600 transition-colors">
              Home
            </Link>
            <Link to="/analyze" className="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors">
              Analyze
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;