import React, { useState } from 'react';
import BusinessDescriptionInput from './BusinessDescriptionInput';
import ModelSelectors from './ModelSelectors';
import GenerateButton from './GenerateButton';
import '../styles/InputArea.css';

const InputArea = ({ onSendMessage, isLoading }) => {
  const [formData, setFormData] = useState({
    businessDescription: '',
    llmModel: 'simulation',
    imageModel: 'simulation',
    galleryImages: 1
  });

  const [errors, setErrors] = useState({});

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: null
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.businessDescription.trim()) {
      newErrors.businessDescription = 'Please describe your business and vision';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validateForm() && !isLoading) {
      onSendMessage(formData);
      setFormData(prev => ({
        ...prev,
        businessDescription: ''
      }));
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="input-area">
      <div className="input-container">
        <BusinessDescriptionInput
          value={formData.businessDescription}
          onChange={(value) => handleInputChange('businessDescription', value)}
          onKeyDown={handleKeyDown}
          error={errors.businessDescription}
          disabled={isLoading}
        />
        
        <div className="controls-section">
          <ModelSelectors
            llmModel={formData.llmModel}
            imageModel={formData.imageModel}
            galleryImages={formData.galleryImages}
            onLlmModelChange={(value) => handleInputChange('llmModel', value)}
            onImageModelChange={(value) => handleInputChange('imageModel', value)}
            onGalleryImagesChange={(value) => handleInputChange('galleryImages', value)}
            disabled={isLoading}
          />
          
          <GenerateButton
            onClick={handleSubmit}
            disabled={isLoading || !formData.businessDescription.trim()}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  );
};

export default InputArea;
