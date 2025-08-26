import React from 'react';

const ModelSelectors = ({ 
  llmModel, 
  imageModel, 
  galleryImages, 
  onLlmModelChange, 
  onImageModelChange, 
  onGalleryImagesChange,
  disabled 
}) => {
  const llmOptions = [
    { label: 'Simulation', value: 'simulation' },
    { label: 'GPT-4o mini', value: 'openai' },
    { label: 'Ollama (Local)', value: 'ollama' }
  ];
  const imageOptions = [
    { label: 'Simulation', value: 'simulation' },
    { label: 'GPT Image 1', value: 'openai' }
  ];
  const galleryOptions = Array.from({ length: 15 }, (_, i) => i + 1);

  return (
    <div className="model-selectors">
      <div className="selector-group">
        <label htmlFor="llm-model" className="selector-label">LLM Model</label>
        <select
          id="llm-model"
          className="model-selector"
          value={llmModel}
          onChange={(e) => onLlmModelChange(e.target.value)}
          disabled={disabled}
          aria-label="Select LLM Model"
        >
          {llmOptions.map(option => (
            <option key={option.value} value={option.value}>{option.label}</option>
          ))}
        </select>
      </div>

      <div className="selector-group">
        <label htmlFor="image-model" className="selector-label">Image Model</label>
        <select
          id="image-model"
          className="model-selector"
          value={imageModel}
          onChange={(e) => onImageModelChange(e.target.value)}
          disabled={disabled}
          aria-label="Select Image Model"
        >
          {imageOptions.map(option => (
            <option key={option.value} value={option.value}>{option.label}</option>
          ))}
        </select>
      </div>

      <div className="selector-group">
        <label htmlFor="gallery-images" className="selector-label">Gallery Images</label>
        <select
          id="gallery-images"
          className="model-selector"
          value={galleryImages}
          onChange={(e) => onGalleryImagesChange(parseInt(e.target.value))}
          disabled={disabled}
          aria-label="Select number of gallery images"
        >
          {galleryOptions.map(option => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default ModelSelectors;
