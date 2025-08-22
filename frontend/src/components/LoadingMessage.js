import React from 'react';

const LoadingMessage = ({ jobData }) => {
  const { status, total_images = 0, completed_images = 0 } = jobData;

  const getStatusText = () => {
    switch (status) {
      case 'generating_prompt':
        return 'Enhancing your prompt with AI...';
      case 'generating_images':
        return `Creating your images... (${completed_images}/${total_images})`;
      case 'creating_zip':
        return 'Packaging your images...';
      case 'completed':
        return 'Images ready!';
      default:
        return 'Processing your request...';
    }
  };

  return (
    <div className="message assistant-message">
      <div className="message-content">
        <div className="simple-loading">
          <div className="loading-spinner"></div>
          <span>{getStatusText()}</span>
        </div>

      </div>
    </div>
  );
};

export default LoadingMessage;
