import React from 'react';

// Helper components for icons
const HeartIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 016.364 0L12 7.636l1.318-1.318a4.5 4.5 0 016.364 6.364L12 20.364l-7.682-7.682a4.5 4.5 0 010-6.364z" />
    </svg>
);

const CommentIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
    </svg>
);

const ShareIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8m-4-6l-4-4m0 0L8 6m4-4v12" />
    </svg>
);

const SaveIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
    </svg>
);

const FeaturesGrid = () => {
  return (
    <section className="px-4 sm:px-8 md:px-16 py-16 rangoli-pattern relative">
      <div className="container mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">

        {/* Card 1 - Kolam Pattern */}
        <div className="relative aspect-[4/5] bg-cover bg-center rounded-2xl shadow-xl overflow-hidden" style={{backgroundImage: 'url("https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80")'}}>
          <div className="absolute inset-0 bg-black bg-opacity-40"></div>
          <div className="absolute inset-0 flex items-center justify-center p-6">
            <div className="bg-orange-400 p-6 rounded-lg text-black transform -rotate-6 shadow-lg">
              <p className="text-xl sm:text-2xl font-bold leading-tight">Creating genuine patterns as a kolam artist</p>
            </div>
          </div>
        </div>

        {/* Card 2 */}
        <div className="aspect-[4/5] bg-blue-100 rounded-2xl shadow-xl p-8 flex flex-col justify-between text-left relative overflow-hidden">
          <div>
            <p className="text-sm font-bold uppercase tracking-widest text-gray-500">PATTERN ANALYSIS.</p>
            <h3 className="text-3xl sm:text-4xl font-bold mt-2">The power of AI pattern recognition</h3>
          </div>
          <div className="absolute bottom-0 right-0 w-2/3 transform translate-x-1/4 translate-y-1/4 rotate-12 rounded-lg shadow-lg bg-white p-4">
            <div className="text-4xl">🔍</div>
          </div>
        </div>

        {/* Card 3 - Rangoli Design */}
        <div className="relative aspect-[4/5] bg-cover bg-center rounded-2xl shadow-xl overflow-hidden" style={{backgroundImage: 'url("https://images.unsplash.com/photo-1582515073490-39981397c445?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80")'}}>
          <div className="absolute inset-0 bg-black bg-opacity-30"></div>
           <div className="absolute inset-0 flex items-center justify-center p-6">
               <div className="bg-white/90 backdrop-blur-sm p-6 rounded-2xl shadow-2xl max-w-sm text-left">
                   <p className="text-base sm:text-lg text-gray-700 italic">"They have asked us many times about expanding the core Kolam brand into other cultural favourites. You have our word, we're on it. Please keep me posted on new additions."</p>
                   <p className="text-right font-bold mt-4">-Alisha Sacdney</p>
               </div>
           </div>
        </div>

        {/* Card 4 - Mandala Art */}
        <div className="relative aspect-[4/5] bg-cover bg-center rounded-2xl shadow-xl overflow-hidden" style={{backgroundImage: 'url("https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80")'}}>
          <div className="absolute inset-0 bg-black bg-opacity-20"></div>
            <div className="absolute inset-0 flex items-center justify-center p-6">
                <div className="bg-white p-4 rounded-2xl shadow-2xl w-full max-w-xs text-left">
                    <div className="flex items-center space-x-3 mb-3">
                        <div className="w-12 h-12 rounded-full border-2 border-gray-200 bg-gray-300 flex items-center justify-center">
                          <span className="text-sm font-bold">M</span>
                        </div>
                        <div>
                            <p className="font-bold">@mandalaartist</p>
                        </div>
                    </div>
                    <p>Ancient patterns meet modern design ✨</p>
                    <p className="text-gray-500 text-sm mt-1">(sacred geometry reveal)</p>
                    <div className="flex justify-between items-center mt-4 text-gray-600">
                       <div className="flex space-x-4">
                         <HeartIcon />
                         <span className="text-sm">2.1k</span>
                         <CommentIcon />
                         <span className="text-sm">156</span>
                         <ShareIcon />
                         <span className="text-sm">45</span>
                       </div>
                       <SaveIcon />
                    </div>
                </div>
            </div>
        </div>
      </div>
    </section>
  );
};

export default FeaturesGrid;