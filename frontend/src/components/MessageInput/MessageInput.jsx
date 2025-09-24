import React, { useState } from 'react';
import { Send, Image } from 'lucide-react';
import IconButton from '../common/IconButton';
import ImageUpload from '../ImageUpload/ImageUpload';

const MessageInput = ({ onSendMessage, onImageSelect, selectedImage, isLoading }) => {
  const [message, setMessage] = useState('');
  const [showImageUpload, setShowImageUpload] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() || selectedImage) {
      onSendMessage(message, selectedImage);
      setMessage('');
      setShowImageUpload(false);
    }
  };

  const handleImageSelect = (imageData) => {
    onImageSelect(imageData);
    setShowImageUpload(false);
  };

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      {showImageUpload && (
        <div className="mb-4">
          <ImageUpload
            onImageSelect={handleImageSelect}
            selectedImage={selectedImage}
            className="max-w-md mx-auto"
          />
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex items-end gap-2">
        <div className="flex-1">
          <div className="relative">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask about kolam art or upload an image to analyze..."
              className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none"
              rows={1}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
            <button
              type="button"
              onClick={() => setShowImageUpload(!showImageUpload)}
              className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 text-gray-400 hover:text-orange-500 transition-colors"
            >
              <Image size={20} />
            </button>
          </div>
        </div>
        <IconButton
          icon={Send}
          onClick={handleSubmit}
          disabled={isLoading || (!message.trim() && !selectedImage)}
          className={`p-3 ${isLoading || (!message.trim() && !selectedImage) ? 'opacity-50 cursor-not-allowed' : 'hover:bg-orange-600'}`}
        />
      </form>
    </div>
  );
};

export default MessageInput;