import React, { useState } from 'react';
import Header from '../components/Header/Header';
import ChatWindow from '../components/ChatWindow/ChatWindow';
import MessageInput from '../components/MessageInput/MessageInput';
import AnalysisDisplay from '../components/AnalysisDisplay/AnalysisDisplay';
import LoadingIndicator from '../components/common/LoadingIndicator';

const AnalysisPage = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleSendMessage = async (text, image) => {
    const userMessage = {
      sender: 'user',
      text: text,
      image: image?.preview
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      let response;

      if (image) {
        // Handle image analysis
        const formData = new FormData();
        formData.append('image', image.file);
        if (text) {
          formData.append('prompt', text);
        }

        response = await fetch('/api/chat', {
          method: 'POST',
          body: formData,
        });
      } else {
        // Handle text-only chat
        response = await fetch('/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ prompt: text }),
        });
      }

      const data = await response.json();

      if (response.ok) {
        const botMessage = {
          sender: 'bot',
          text: data.response
        };
        setMessages(prev => [...prev, botMessage]);
      } else {
        const errorMessage = {
          sender: 'bot',
          text: `Error: ${data.error || 'Something went wrong'}`
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage = {
        sender: 'bot',
        text: 'Sorry, I encountered an error. Please try again.'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleImageSelect = (imageData) => {
    setSelectedImage(imageData);
  };

  const handleAnalyzeKolam = async () => {
    if (!selectedImage) return;

    setIsLoading(true);

    try {
      // Convert image to base64
      const response = await fetch(selectedImage.preview);
      const blob = await response.blob();
      const base64 = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.readAsDataURL(blob);
      });

      const analysisResponse = await fetch('/api/analyze_kolam', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image_data: base64 }),
      });

      const data = await analysisResponse.json();

      if (analysisResponse.ok) {
        setAnalysisResult(data);
      } else {
        alert(`Analysis failed: ${data.error}`);
      }
    } catch (error) {
      alert('Failed to analyze image. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="max-w-6xl mx-auto py-8 px-4">
        {analysisResult ? (
          <AnalysisDisplay analysis={analysisResult} />
        ) : (
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <div className="h-96 flex flex-col">
              <ChatWindow messages={messages} />
              {isLoading && (
                <div className="flex justify-center p-4">
                  <LoadingIndicator />
                </div>
              )}
            </div>
            <MessageInput
              onSendMessage={handleSendMessage}
              onImageSelect={handleImageSelect}
              selectedImage={selectedImage}
              isLoading={isLoading}
            />
            {selectedImage && (
              <div className="p-4 border-t bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <img
                      src={selectedImage.preview}
                      alt="Selected"
                      className="w-12 h-12 object-cover rounded"
                    />
                    <span className="text-sm text-gray-600">{selectedImage.file.name}</span>
                  </div>
                  <button
                    onClick={handleAnalyzeKolam}
                    disabled={isLoading}
                    className="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors disabled:opacity-50"
                  >
                    {isLoading ? 'Analyzing...' : 'Analyze Kolam'}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalysisPage;