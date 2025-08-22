import React from 'react';

const AssistantMessage = ({ message }) => {
  return (
    <div className="message assistant-message">
      <div className="message-content">
        <p>{message.content}</p>
        
        {message.images && message.images.length > 0 && (
          <div className="generated-images">
            <h4>🖼️ Generated Images:</h4>
            <div className="image-grid">
              {message.images.map((image, index) => (
                <div key={index} className="image-item">
                  <div className="image-thumbnail">
                    <img 
                      src={`https://via.placeholder.com/200x200/4a5568/ffffff?text=Image+${index + 1}`} 
                      alt={image.type}
                      onError={(e) => {
                        e.target.src = `data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" fill="%234a5568"/><text x="100" y="100" text-anchor="middle" dy="0.3em" fill="white" font-family="Arial" font-size="14">Image ${index + 1}</text></svg>`;
                      }}
                    />
                  </div>
                  <span className="image-label">{image.type}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {message.downloadLink && (
          <div className="download-section">
            <button className="download-button" onClick={() => window.open(message.downloadLink, '_blank')}>
              📦 Download ZIP file
            </button>
          </div>
        )}

        <div className="message-timestamp">
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};

export default AssistantMessage;
