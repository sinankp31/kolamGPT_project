import React, { useRef, useEffect } from 'react';
import ChatMessage from '../ChatMessage/ChatMessage';

const ChatWindow = ({ messages }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          <div className="text-4xl mb-4">🎨</div>
          <p className="text-lg">Welcome to KolamGPT!</p>
          <p className="text-sm">Upload a kolam image or ask me anything about traditional kolam art.</p>
        </div>
      ) : (
        messages.map((msg, index) => (
          <ChatMessage key={index} msg={msg} />
        ))
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatWindow;