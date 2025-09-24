import React from 'react';

// SVG Icon for the hand pointer
const HandPointerIcon = () => (
    <svg
        xmlns="http://www.w3.org/2000/svg"
        width="48"
        height="48"
        viewBox="0 0 24 24"
        fill="white"
        className="transform -scale-x-100 rotate-12"
    >
        <path d="M15.5 13.5c0-1.22-.44-2.33-1.15-3.22.25-.56.39-1.17.39-1.78 0-2.21-1.79-4-4-4s-4 1.79-4 4c0 .61.14 1.22.39 1.78C6.44 11.17 6 12.28 6 13.5V18c0 .83.67 1.5 1.5 1.5h1.42c.32-.89 1.17-1.5 2.08-1.5s1.76.61 2.08 1.5h1.42c.83 0 1.5-.67 1.5-1.5v-4.5zM10.74 5.5c.69 0 1.25.56 1.25 1.25S11.43 8 10.74 8s-1.25-.56-1.25-1.25S10.05 5.5 10.74 5.5zM12 12.5c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/>
    </svg>
);

// Component to render list items with underlined text
const ListItem = ({ children }) => {
    // This is a simple parser. For a real app, you might use a more robust library.
    const parts = children.split(/(\[.*?\])/g).filter(part => part);

    return (
        <li className="mb-2">
            <span className="mr-2">•</span>
            {parts.map((part, index) => {
                if (part.startsWith('[') && part.endsWith(']')) {
                    return <span key={index} className="underline decoration-2">{part.slice(1, -1)}</span>;
                }
                return <span key={index}>{part}</span>;
            })}
        </li>
    );
};


function OurSolution() {
  return (
    <section className="bg-red-500 w-full min-h-screen flex items-center justify-center font-sans p-4 sm:p-8">
      <div className="container mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">

        {/* Left Side: Text Content */}
        <div className="text-white text-center lg:text-left">
          <h2 className="text-5xl sm:text-6xl md:text-7xl font-black leading-tight">
            5, 4, 3, 2, 1
            <br />
            That's how quickly we analyze your kolam patterns!
          </h2>
          <p className="mt-8 text-lg sm:text-xl max-w-xl mx-auto lg:mx-0">
            Take control of your kolam creation. You decide when, what, and how often to analyze. Whether you're an artist perfecting your patterns or a student learning traditional art, we've got you. 🎨
          </p>
          <button
            onClick={() => window.location.href = '#'}
            className="inline-block mt-12 bg-green-300 text-black text-sm sm:text-base font-bold py-4 px-10 rounded-lg shadow-lg hover:bg-green-400 transition-transform hover:scale-105"
          >
            START ANALYZING NOW
          </button>
        </div>

        {/* Right Side: Cards */}
        <div className="relative h-[600px] flex items-center justify-center">

          {/* Kolam Artists Card (White) */}
          <div className="absolute bg-white text-black p-6 sm:p-8 rounded-2xl shadow-2xl w-full max-w-sm transform -rotate-6">
            <div className="flex items-center mb-4">
              <span className="w-4 h-4 bg-green-400 rounded-full mr-3"></span>
              <h3 className="font-bold text-sm tracking-widest">KOLAM ARTISTS</h3>
            </div>
            <ul className="text-gray-700">
                <ListItem>Creating [traditional patterns]</ListItem>
                <ListItem>Learning [cultural significance]</ListItem>
                <ListItem>Perfecting your [symmetry]</ListItem>
                <ListItem>Exploring [regional styles]</ListItem>
                <ListItem>Too [busy] to analyze manually</ListItem>
                <ListItem>Preparing for [festivals]</ListItem>
                <ListItem>Documenting your [artwork]</ListItem>
                <ListItem>Catching up on [techniques]</ListItem>
            </ul>
             <div className="absolute top-10 right-[-20px] text-4xl transform rotate-12">
                🎨
             </div>
          </div>

          {/* Art Students Card (Black) */}
          <div className="absolute bg-black text-white p-6 sm:p-8 rounded-2xl shadow-2xl w-full max-w-sm transform rotate-6 translate-x-4 translate-y-24 sm:translate-x-12 sm:translate-y-32">
            <div className="flex items-center mb-4">
              <span className="w-4 h-4 bg-white rounded-full mr-3"></span>
              <h3 className="font-bold text-sm tracking-widest">ART STUDENTS</h3>
            </div>
            <ul className="">
                <ListItem>Understanding [pattern complexity]</ListItem>
                <ListItem>Learning [cultural history]</ListItem>
                <ListItem>Practicing [geometric designs]</ListItem>
                <ListItem>Needing instant [feedback]</ListItem>
                <ListItem>Exploring [different styles]</ListItem>
                <ListItem>Testing [creative variations]</ListItem>
                <ListItem>Responding to [assignments]</ListItem>
                <ListItem>Aiding in [skill development]</ListItem>
            </ul>
            <div className="absolute bottom-[-30px] right-[-10px]">
                <HandPointerIcon />
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}

export default OurSolution;