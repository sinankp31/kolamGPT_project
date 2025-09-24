import React, { useState } from 'react';
import { contactFormApi } from '../../services/api';

const ContactUs = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    category: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState('');
  const [submitError, setSubmitError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear any previous messages when user starts typing
    if (submitMessage || submitError) {
      setSubmitMessage('');
      setSubmitError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitMessage('');
    setSubmitError('');

    try {
      const result = await contactFormApi(formData);
      setSubmitMessage(result.message || 'Thank you for your message! We\'ll get back to you soon.');
      // Reset form on success
      setFormData({ fullName: '', email: '', category: '' });
    } catch (error) {
      setSubmitError(error.message || 'Failed to send message. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-purple-300 p-6 flex items-center justify-center">
      <div className="bg-purple-300 rounded-3xl p-8 lg:p-12 max-w-6xl w-full mx-auto">
        <div className="flex flex-col lg:flex-row gap-8 lg:gap-16">
          {/* Left Section */}
          <div className="flex-1 lg:max-w-2xl">
            {/* Main Heading */}
            <h1 className="text-3xl lg:text-5xl font-black text-gray-800 mb-8 leading-tight">
              Came for the patterns, stayed<br />
              for the{' '}
              <span className="bg-purple-600 text-white px-3 py-1 rounded-lg inline-block transform -rotate-1">
                analysis!
              </span>
              <span className="inline-block ml-2">
                🎨
              </span>
            </h1>

            {/* Social Section */}
            <div className="mb-8">
              <p className="text-gray-800 font-semibold text-sm tracking-wider mb-4">
                FOLLOW OUR JOURNEY:
              </p>
              <div className="flex gap-4">
                <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-sm border-2 border-gray-200 hover:shadow-md transition-shadow">
                  <svg className="w-6 h-6 text-pink-500" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                  </svg>
                </div>
                <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-sm border-2 border-gray-200 hover:shadow-md transition-shadow">
                  <svg className="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                  </svg>
                </div>
              </div>
            </div>

            {/* Copyright */}
            <p className="text-gray-700 text-sm">
              © Team Horizon. All rights reserved
            </p>
          </div>

          {/* Right Section - Newsletter Form */}
          <div className="lg:max-w-sm w-full">
            <h2 className="text-gray-800 font-semibold text-lg mb-4">
              Contact Us
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              <input
                type="text"
                name="fullName"
                placeholder="Full Name"
                value={formData.fullName}
                onChange={handleInputChange}
                className="w-full px-6 py-3 rounded-full border-none outline-none text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-orange-300"
                required
                disabled={isSubmitting}
              />

              <input
                type="email"
                name="email"
                placeholder="Email Address"
                value={formData.email}
                onChange={handleInputChange}
                className="w-full px-6 py-3 rounded-full border-none outline-none text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-orange-300"
                required
                disabled={isSubmitting}
              />

              <select
                name="category"
                value={formData.category}
                onChange={handleInputChange}
                className="w-full px-6 py-3 rounded-full border-none outline-none text-gray-800 bg-white appearance-none cursor-pointer focus:ring-2 focus:ring-orange-300"
                required
                disabled={isSubmitting}
              >
                <option value="">I'm a...</option>
                <option value="kolam-artist">Kolam Artist</option>
                <option value="art-student">Art Student</option>
                <option value="cultural-enthusiast">Cultural Enthusiast</option>
                <option value="educator">Educator</option>
                <option value="other">Other</option>
              </select>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white font-bold py-3 px-6 rounded-full transition-colors duration-200 mt-6 disabled:cursor-not-allowed"
              >
                {isSubmitting ? 'SENDING...' : 'SUBMIT'}
              </button>

              {/* Success Message */}
              {submitMessage && (
                <div className="mt-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">
                  <div className="flex items-center">
                    <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    {submitMessage}
                  </div>
                </div>
              )}

              {/* Error Message */}
              {submitError && (
                <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
                  <div className="flex items-center">
                    <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    {submitError}
                  </div>
                </div>
              )}
            </form>

            {/* Bottom Links */}
            <div className="flex flex-wrap gap-6 mt-6 text-sm text-gray-800">
              <a href="#" className="hover:text-gray-600 transition-colors">
                Terms of Use
              </a>
              <a href="#" className="hover:text-gray-600 transition-colors">
                Privacy Policy
              </a>
              <a href="#" className="hover:text-gray-600 transition-colors">
                Support
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContactUs;