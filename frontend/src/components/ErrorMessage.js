import React from 'react';

const ErrorMessage = ({ error, onRetry }) => {
  return (
    <div className="message assistant-message">
      <div className="message-content">
        <p style={{ color: '#ef4444' }}>❌ {error.message}</p>
        
        <div className="error-actions" style={{ marginTop: '12px' }}>
          <button 
            className="retry-button"
            onClick={onRetry}
            style={{
              backgroundColor: '#a6adff',
              color: '#212121',
              padding: '8px 16px',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontWeight: '600',
              textTransform: 'uppercase',
              fontSize: '12px'
            }}
          >
            🔄 Try Again
          </button>
        </div>

        <div className="message-timestamp">
          {new Date().toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;
