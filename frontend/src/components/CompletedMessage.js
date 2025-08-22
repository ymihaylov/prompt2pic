import React, { useState } from 'react';
import { ImageGenerationAPI, handleApiError } from '../services/api';
import ImageModal from './ImageModal';

const CompletedMessage = ({ jobData, timestamp }) => {
  const { images = {}, zip_path, job_id } = jobData;
  const [selectedImage, setSelectedImage] = useState(null);

  const handleDownload = async () => {
    if (!zip_path) {
      alert('Download not available yet. Please try again.');
      return;
    }

    try {
      await ImageGenerationAPI.downloadZip(zip_path, job_id);
    } catch (error) {
      const errorInfo = handleApiError(error, 'download');
      alert(errorInfo.message);
    }
  };

  const completedImages = Object.entries(images).filter(([_, image]) => image.status === 'completed');

  return (
    <div className="message assistant-message">
      <div className="message-content">
        <p>I've generated {completedImages.length} images for your business! Here's what I created:</p>

        {completedImages.length > 0 && (
          <div className="generated-images">
            <h4>🖼️ Generated Images:</h4>
            <div className="image-grid">
              {completedImages.map(([key, image]) => (
                <div key={key} className="image-item">
                  <div className="image-thumbnail" onClick={() => setSelectedImage(image)}>
                    <img 
                      src={`http://localhost:8000/${image.local_path}`} 
                      alt={`Generated ${image.type}`}
                      onError={(e) => {
                        e.target.src = `data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" fill="%234a5568"/><text x="100" y="100" text-anchor="middle" dy="0.3em" fill="white" font-family="Arial" font-size="14">Image ${key}</text></svg>`;
                      }}
                    />
                  </div>
                  <span className="image-label">
                    {image.type === 'hero' ? 'Hero Image' : 
                     image.type === 'about' ? 'About Section' : 
                     `Gallery ${image.type.split('_')[1] || key}`}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="download-section">
          <button 
            className="download-button"
            onClick={handleDownload}
            disabled={!zip_path}
          >
            📦 Download ZIP file
          </button>
        </div>

        <div className="message-timestamp">
          {timestamp ? timestamp.toLocaleTimeString() : new Date().toLocaleTimeString()}
        </div>
      </div>
      
      <ImageModal 
        image={selectedImage} 
        isOpen={!!selectedImage} 
        onClose={() => setSelectedImage(null)} 
      />
    </div>
  );
};

export default CompletedMessage;
