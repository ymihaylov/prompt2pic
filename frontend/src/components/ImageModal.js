import React, { useEffect } from 'react';

const ImageModal = ({ image, isOpen, onClose }) => {
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === 'Escape') onClose();
    };
    
    if (isOpen) {
      document.addEventListener('keydown', handleEsc);
    }
    
    return () => document.removeEventListener('keydown', handleEsc);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="image-modal-overlay" onClick={onClose}>
      <div className="image-modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>
        <img 
          src={`http://localhost:8000/${image.local_path}`} 
          alt={`Generated ${image.type}`}
          className="modal-image"
        />
      </div>
    </div>
  );
};

export default ImageModal;
