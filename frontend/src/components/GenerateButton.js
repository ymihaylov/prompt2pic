import React from 'react';

const GenerateButton = ({ onClick, disabled, isLoading }) => {
  return (
    <div className="generate-button-container">
      <button
        className="generate-button"
        onClick={onClick}
        disabled={disabled}
        aria-label={isLoading ? "Generating images..." : "Generate images"}
      >
        {isLoading ? (
          <>
            <div className="button-spinner"></div>
            Generating...
          </>
        ) : (
          'Generate Images'
        )}
      </button>
    </div>
  );
};

export default GenerateButton;
