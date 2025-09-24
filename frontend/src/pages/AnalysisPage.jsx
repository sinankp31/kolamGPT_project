import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header/Header';
import ChatWindow from '../components/ChatWindow/ChatWindow';
import MessageInput from '../components/MessageInput/MessageInput';
import { chatAPI } from '../services/api';
import { useTheme } from '../hooks/useTheme';

const AnalysisPage = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: 'Hello! I\'m KolamGPT, your AI assistant for traditional South Indian kolam art. You can ask me questions about kolam patterns, techniques, cultural significance, or upload images for analysis. How can I help you today?',
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const chatEndRef = useRef(null);

  const handleSendMessage = async (text, image) => {
    if (!text.trim() && !image) return;

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: text,
      image: image?.preview,
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await chatAPI.sendMessage(text, image);
      const botMessage = {
        id: Date.now() + 1,
        sender: 'bot',
        text: response.response || response.response_text || 'Sorry, I couldn\'t generate a response.',
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        sender: 'bot',
        text: 'Sorry, I encountered an error. Please try again.',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoHome = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header
        theme={theme}
        toggleTheme={toggleTheme}
        showHomeButton={true}
        onHomeClick={handleGoHome}
      />
      <div className="flex flex-col h-screen">
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          chatEndRef={chatEndRef}
        />
        <MessageInput
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
};

export default AnalysisPage;