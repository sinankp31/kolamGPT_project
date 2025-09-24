import React from 'react';
import Header from '../components/landing/Header';
import HeroSection from '../components/landing/HeroSection';
import FeaturesGrid from '../components/landing/FeaturesGrid';
import HowItWorks from '../components/landing/HowItWorks';
import OurSolution from '../components/landing/OurSolution';
import ContactUs from '../components/landing/ContactUs';
import Footer from '../components/landing/Footer';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main>
        <HeroSection />
        <FeaturesGrid />
        <HowItWorks />
        <OurSolution />
        <ContactUs />
      </main>
      <Footer />
    </div>
  );
};

export default LandingPage;