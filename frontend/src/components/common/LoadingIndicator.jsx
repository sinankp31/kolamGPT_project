import React from 'react';

const LoadingIndicator = ({ size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  return (
    <div className={`animate-spin rounded-full border-2 border-gray-300 border-t-orange-500 ${sizeClasses[size]} ${className}`}></div>
  );
};

export default LoadingIndicator;