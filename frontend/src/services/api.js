import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout
});

// API service for image generation
export class ImageGenerationAPI {
  /**
   * Start image generation job
   * @param {Object} payload - Generation request
   * @param {string} payload.prompt - User's business description
   * @param {number} payload.gallery_count - Number of gallery images (1-15)
   * @param {string} payload.llm_model - LLM model to use
   * @param {string} payload.image_model - Image model to use
   * @returns {Promise<Object>} Job start response with job_id
   */
  static async startImageGeneration(payload) {
    try {
      const response = await api.post('/images/generate/async/celery', payload);
      return response.data;
    } catch (error) {
      console.error('Failed to start image generation:', error);
      throw error;
    }
  }

  /**
   * Poll job status
   * @param {string} jobId - Job ID to check status for
   * @returns {Promise<Object>} Job status response
   */
  static async getJobStatus(jobId) {
    try {
      const response = await api.get(`/jobs/status/${jobId}`);
      return response.data;
    } catch (error) {
      console.error('Failed to get job status:', error);
      throw error;
    }
  }

  /**
   * Download ZIP file
   * @param {string} zipPath - Path to ZIP file
   * @param {string} jobId - Job ID for filename
   * @returns {Promise<void>}
   */
  static async downloadZip(zipPath, jobId) {
    try {
      const response = await api.get(`/${zipPath}`, {
        responseType: 'blob'
      });
      
      const blob = new Blob([response.data]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `images_${jobId}.zip`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      console.error('Download failed:', error);
      throw error;
    }
  }
}

// Error handling utilities
export const handleApiError = (error, context = '') => {
  console.error(`API Error${context ? ` in ${context}` : ''}:`, error);
  
  let userMessage = "Something went wrong. Please try again.";
  
  if (error.response?.status === 429) {
    userMessage = "Server is busy. Please wait a moment and try again.";
  } else if (error.response?.status === 400) {
    userMessage = "Invalid request. Please check your inputs.";
  } else if (error.response?.status === 404) {
    userMessage = "Service not found. Please check if the server is running.";
  } else if (error.response?.status >= 500) {
    userMessage = "Server error. Please try again later.";
  } else if (error.code === 'NETWORK_ERROR' || !navigator.onLine) {
    userMessage = "No internet connection. Please check your network.";
  } else if (error.code === 'TIMEOUT') {
    userMessage = "Request timed out. Please try again.";
  }
  
  return {
    message: userMessage,
    status: error.response?.status,
    code: error.code
  };
};

export default ImageGenerationAPI;
