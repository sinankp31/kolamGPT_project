import React, { useState, useRef } from 'react';
import { Upload, X } from 'lucide-react';

const ImageUpload = ({ onImageSelect, selectedImage, className = '' }) => {
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFile = (file) => {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        onImageSelect({
          file,
          preview: e.target.result
        });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleRemove = () => {
    onImageSelect(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className={className}>
      {!selectedImage ? (
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
            dragActive
              ? 'border-orange-500 bg-orange-50'
              : 'border-gray-300 hover:border-orange-400 hover:bg-gray-50'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={handleClick}
        >
          <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <p className="text-lg font-medium text-gray-900 mb-2">
            Upload your kolam image
          </p>
          <p className="text-gray-600 mb-4">
            Drag and drop an image here, or click to select
          </p>
          <p className="text-sm text-gray-500">
            Supports JPG, PNG, GIF up to 10MB
          </p>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            className="hidden"
          />
        </div>
      ) : (
        <div className="relative">
          <img
            src={selectedImage.preview}
            alt="Selected kolam"
            className="w-full h-64 object-cover rounded-lg"
          />
          <button
            onClick={handleRemove}
            className="absolute top-2 right-2 bg-red-500 text-white p-2 rounded-full hover:bg-red-600 transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
          <div className="absolute bottom-2 left-2 bg-black bg-opacity-50 text-white px-3 py-1 rounded text-sm">
            {selectedImage.file.name}
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;