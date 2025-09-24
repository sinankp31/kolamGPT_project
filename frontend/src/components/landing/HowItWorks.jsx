import React from 'react';

// --- SVG Icons for the pixelated effect ---

// Pixelated Hand Cursor Icon
const PixelHandIcon = () => (
    <svg width="48" height="48" viewBox="0 0 24 24" fill="black" xmlns="http://www.w3.org/2000/svg">
        <path d="M6 3H9V4H10V5H11V6H12V9H11V10H10V11H9V12H8V15H7V18H6V3Z" />
        <path d="M9 3H12V4H13V5H14V6H15V7H16V9H15V10H14V11H13V12H12V13H11V15H10V18H9V3Z" />
    </svg>
);

// Pixelated Hourglass Icon
const PixelHourglassIcon = () => (
    <svg width="48" height="48" viewBox="0 0 24 24" fill="black" xmlns="http://www.w3.org/2000/svg">
        <path d="M7 5H17V6H16V7H15V8H14V9H13V10H12V11H11V12H12V13H13V14H14V15H15V16H16V17H17V18H7V17H8V16H9V15H10V14H11V13H12V12H11V11H10V10H9V9H8V8H7V7H8V6H7V5Z" />
        <path fillRule="evenodd" clipRule="evenodd" d="M8 6H16V7H8V6ZM8 17H16V16H8V17Z" />
    </svg>
);


// --- Main Component ---

function HowItWorksSection() {
  const steps = [
    {
      number: 1,
      title: "Upload your kolam",
      description: "Upload a photo of your kolam pattern for instant AI analysis",
    },
    {
      number: 2,
      title: "AI analysis begins",
      description: "Our advanced AI examines symmetry, patterns, and cultural elements",
    },
    {
      number: 3,
      title: "Get detailed insights",
      description: "Receive comprehensive analysis with suggestions and cultural context!",
    },
  ];

  return (
    <section className="bg-violet-200 w-full min-h-screen flex items-center justify-center font-sans p-4 sm:p-8 overflow-hidden">
      <div className="container mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

        {/* Left Side: Receipt */}
        <div className="relative flex justify-center items-center">
            {/* The main receipt element with rotation and shadow */}
            <div className="relative bg-white shadow-2xl w-full max-w-md transform -rotate-3 p-8 pt-12 pb-12">
                {/* Jagged top edge */}
                <div className="absolute top-0 left-0 right-0 h-4 bg-repeat-x" style={{
                    backgroundImage: `radial-gradient(circle at bottom, transparent 8px, white 8px)`,
                    backgroundSize: '20px 20px',
                    backgroundPosition: '5px 0'
                }}></div>

                {/* Jagged bottom edge */}
                <div className="absolute bottom-0 left-0 right-0 h-4 bg-repeat-x" style={{
                    backgroundImage: `radial-gradient(circle at top, transparent 8px, white 8px)`,
                    backgroundSize: '20px 20px',
                    backgroundPosition: '5px 0'
                }}></div>

                {/* Pixel Icons */}
                <div className="absolute -top-4 -left-10 transform rotate-12">
                    <PixelHandIcon />
                </div>
                <div className="absolute -bottom-8 -right-8 transform -rotate-12">
                    <PixelHourglassIcon />
                </div>

                {/* Receipt Content */}
                <div className="text-center font-mono">
                    <h3 className="font-bold text-lg tracking-widest">YOUR KOLAM ANALYSIS RECEIPT!</h3>
                    <p className="my-4 text-gray-400 tracking-[0.2em]">∗ ∗ ∗ ∗ ∗ ∗ ∗ ∗ ∗ ∗ ∗</p>
                </div>

                <div className="space-y-6 my-8 text-left">
                    {steps.map((step) => (
                        <div key={step.number} className="flex items-start space-x-4">
                            <div className="flex-shrink-0 w-10 h-10 bg-violet-800 text-white font-bold text-xl rounded-full flex items-center justify-center">
                                {step.number}
                            </div>
                            <div>
                                <h4 className="font-bold text-lg">{step.title}</h4>
                                <p className="text-gray-600">{step.description}</p>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="text-center font-mono">
                    <p className="my-4 text-gray-400 tracking-[0.2em]">∗ ∗ ∗ ∗ ∗ ∗ ∗ ∗ ∗ ∗ ∗</p>
                    <p className="font-bold text-sm">THANK YOU! HAPPY CREATING :)</p>
                    <div className="flex justify-center items-end h-10 mt-4 space-x-px">
                        {/* Barcode simulation */}
                        {[...Array(50)].map((_, i) => (
                            <div key={i} className="bg-black w-0.5" style={{ height: `${Math.random() * 80 + 20}%`}}></div>
                        ))}
                    </div>
                </div>
            </div>
        </div>

        {/* Right Side: Text Content */}
        <div className="text-center lg:text-left">
          <h2 className="text-5xl sm:text-6xl md:text-7xl font-black leading-tight text-gray-900">
            I'm intrigued.
            <br />
            How does this work?
          </h2>
          <button
            onClick={() => window.location.href = '#'}
            className="inline-block mt-8 bg-red-500 text-white text-sm sm:text-base font-bold py-4 px-10 rounded-lg shadow-lg hover:bg-red-600 transition-transform hover:scale-105"
          >
            START ANALYZING NOW
          </button>
        </div>

      </div>
    </section>
  );
}

export default HowItWorksSection;