import React from 'react';

const IconButton = ({ icon: Icon, onClick, className = '', size = 20, ...props }) => {
  return (
    <button
      onClick={onClick}
      className={`p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors ${className}`}
      {...props}
    >
      <Icon size={size} />
    </button>
  );
};

export default IconButton;