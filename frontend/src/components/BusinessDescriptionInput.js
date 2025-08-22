import React, { useRef, useEffect } from 'react';

const BusinessDescriptionInput = ({ value, onChange, onKeyDown, error, disabled }) => {
  const textareaRef = useRef(null);

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
    }
  }, [value]);

  return (
    <div className="business-description-section">
      <textarea
        ref={textareaRef}
        className={`business-description-input ${error ? 'error' : ''}`}
        placeholder="Describe your business and website vision..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={onKeyDown}
        disabled={disabled}
        rows="2"
        aria-label="Business description"
        aria-describedby={error ? "description-error" : undefined}
      />
      {error && (
        <div id="description-error" className="input-error" role="alert">
          {error}
        </div>
      )}
      <div className="input-hint">
        Press Ctrl/Cmd + Enter to generate images
      </div>
    </div>
  );
};

export default BusinessDescriptionInput;
