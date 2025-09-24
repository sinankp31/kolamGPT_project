import React from 'react';

const Header = ({ onStartAnalyzing, showNav = true }) => {
  return (
    <header className="py-6 px-4 sm:px-8 md:px-16" style={{background: 'linear-gradient(135deg, #FFF8DC 0%, #FFE4B5 100%)'}}>
      <div className="container mx-auto flex justify-between items-center">
        <div className="font-black text-3xl tracking-wider text-orange-800 hover:text-orange-900 transition-all duration-300 hover:scale-105 cursor-pointer">
          KOD
        </div>
        {showNav && (
          <nav className="hidden lg:flex items-center space-x-10">
            {['OUR SOLUTION', 'HOW IT WORKS', 'CONTACT US'].map((item) => (
              <a href="#" key={item} className="text-sm font-black tracking-widest text-orange-700 hover:text-orange-900 transition-all duration-300 hover:scale-105 hover:text-orange-800 relative group">
                {item}
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-orange-600 transition-all duration-300 group-hover:w-full"></span>
              </a>
            ))}
          </nav>
        )}
        <button
          onClick={onStartAnalyzing}
          className="bg-gradient-to-r from-orange-500 to-red-500 text-white text-sm font-black py-3 px-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 hover:from-orange-600 hover:to-red-600"
        >
          {showNav ? 'START ANALYZING' : 'HOME'}
        </button>
      </div>
    </header>
  );
};

export default Header;