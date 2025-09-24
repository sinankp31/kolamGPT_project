import React, { useState, useRef } from 'react';
import { Upload, Image as ImageIcon } from 'lucide-react';

const ImageUpload = ({ onAnalyze, isLoading }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onload = (e) => setPreview(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      const uploadedImage = {
        file: selectedFile,
        data: preview.split(',')[1], // base64 data
        preview: preview,
      };
      onAnalyze(uploadedImage);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onload = (e) => setPreview(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  return (
    <div className="mb-6">
      <div
        className="border-4 border-dashed border-orange-300 bg-gradient-to-br from-orange-50 to-yellow-50 rounded-2xl p-8 text-center cursor-pointer hover:border-orange-400 hover:from-orange-100 hover:to-yellow-100 transition-all duration-300 transform hover:scale-105 shadow-lg"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => fileInputRef.current?.click()}
      >
        {preview ? (
          <div className="space-y-4">
            <div className="relative inline-block">
              <img src={preview} alt="Preview" className="max-w-full max-h-64 mx-auto rounded-xl shadow-lg border-4 border-white" />
              <div className="absolute -top-2 -right-2 bg-green-400 text-white rounded-full p-2 shadow-lg">
                <span className="text-sm">✨</span>
              </div>
            </div>
            <p className="text-sm text-orange-700 font-medium">Click to change image or drag a new one</p>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="relative">
              <div className="text-6xl mb-4">🎨</div>
              <div className="absolute -top-2 -right-2 bg-pink-400 text-white rounded-full p-1 text-xs">
                ✨
              </div>
            </div>
            <div>
              <p className="text-xl font-bold text-gray-800 mb-2">Drop your kolam masterpiece here!</p>
              <p className="text-orange-600 font-medium">Or click to browse your files</p>
              <p className="text-sm text-gray-600 mt-2">Supported: JPG, PNG, GIF • Max 10MB</p>
            </div>
          </div>
        )}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          className="hidden"
        />
      </div>
      {selectedFile && (
        <div className="mt-6 text-center">
          <button
            onClick={handleUpload}
            disabled={isLoading}
            className="bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 disabled:from-gray-400 disabled:to-gray-500 text-white px-8 py-3 rounded-xl font-bold text-lg transition-all duration-300 transform hover:scale-105 shadow-xl hover:shadow-2xl"
          >
            {isLoading ? (
              <span className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Analyzing Your Art...
              </span>
            ) : (
              <span className="flex items-center gap-2">
                🔍 Analyze My Kolam!
              </span>
            )}
          </button>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;