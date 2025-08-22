import React from 'react';

const UserMessage = ({ message }) => {
  return (
    <div className="message user-message">
      <div className="message-content">
        <p>{message.content}</p>
        <div className="message-settings">
          <span className="setting-tag">LLM: {
            message.settings.llmModel === 'openai' ? 'GPT-4o mini' : 
            message.settings.llmModel === 'ollama' ? 'Ollama (Local)' : 
            'Simulation'
          }</span>
          <span className="setting-tag">Image: {message.settings.imageModel === 'openai' ? 'DALL-E 3' : 'Simulation'}</span>
          <span className="setting-tag">Gallery: {message.settings.galleryImages} images</span>
        </div>
        <div className="message-timestamp">
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

export default UserMessage;
