import React, { useEffect, useRef } from 'react';
import UserMessage from './UserMessage';
import AssistantMessage from './AssistantMessage';
import LoadingMessage from './LoadingMessage';
import CompletedMessage from './CompletedMessage';
import ErrorMessage from './ErrorMessage';

const MessageList = ({ messages, isLoading, onRetry }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const renderMessage = (message) => {
    switch (message.type) {
      case 'user':
        return <UserMessage key={message.id} message={message} />;
      
      case 'loading':
        return <LoadingMessage key={message.id} jobData={message.jobData} />;
      
      case 'assistant-completed':
        return <CompletedMessage key={message.id} jobData={message.jobData} timestamp={message.timestamp} />;
      
      case 'assistant-error':
        return (
          <ErrorMessage 
            key={message.id} 
            error={message.error} 
            jobId={message.jobData?.job_id}
            onRetry={() => {
              // Find the corresponding user message to retry
              const userMessageIndex = messages.findIndex(m => m.id === message.id) - 1;
              if (userMessageIndex >= 0 && messages[userMessageIndex].type === 'user') {
                onRetry(messages[userMessageIndex]);
              }
            }}
          />
        );
      
      case 'assistant':
      default:
        return <AssistantMessage key={message.id} message={message} />;
    }
  };

  return (
    <div className="messages-container">
      <div className="messages-list">
        {messages.length === 0 && !isLoading ? (
          <div className="welcome-screen">
            <div className="welcome-content">
              <div className="welcome-icon">🎨</div>
              <h2 className="welcome-title">AI Image Generator</h2>
              <p className="welcome-subtitle">
                Create stunning visuals for your business with the power of AI
              </p>
              <div className="welcome-features">
                <div className="feature">✨ Professional quality images</div>
                <div className="feature">🚀 Generated in seconds</div>
                <div className="feature">💼 Perfect for websites & marketing</div>
              </div>
              <p className="welcome-cta">
                Describe your business below to get started!
              </p>
            </div>
          </div>
        ) : (
          <>
            {messages.map(renderMessage)}
            {isLoading && (
              <div className="loading-indicator">
                <div className="loading-spinner"></div>
                <span>Starting generation...</span>
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default MessageList;
