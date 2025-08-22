import React, { useState, useEffect, useCallback } from 'react';
import MessageList from './MessageList';
import InputArea from './InputArea';
import { ImageGenerationAPI, handleApiError } from '../services/api';
import useJobPolling from '../hooks/useJobPolling';
import '../styles/Chat.css';

const ChatContainer = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasActiveJob, setHasActiveJob] = useState(false);

  // Job polling callbacks
  const handleJobUpdate = useCallback((jobId, jobData) => {
    setMessages(prev => prev.map(msg => {
      if (msg.jobId === jobId && (msg.type === 'loading' || msg.type === 'assistant-loading')) {
        return {
          ...msg,
          jobData,
          type: 'loading'
        };
      }
      return msg;
    }));
  }, []);

  const handleJobComplete = useCallback((jobId, jobData) => {
    setMessages(prev => prev.map(msg => {
      if (msg.jobId === jobId) {
        return {
          ...msg,
          type: 'assistant-completed',
          jobData,
          timestamp: new Date()
        };
      }
      return msg;
    }));
    setHasActiveJob(false);
  }, []);

  const handleJobError = useCallback((jobId, error, jobData = null) => {
    setMessages(prev => prev.map(msg => {
      if (msg.jobId === jobId) {
        return {
          ...msg,
          type: 'assistant-error',
          error,
          jobData,
          timestamp: new Date()
        };
      }
      return msg;
    }));
    setHasActiveJob(false);
  }, []);

  // Initialize job polling
  const { startPolling, stopAllPolling } = useJobPolling(
    handleJobUpdate,
    handleJobComplete,
    handleJobError
  );

  // Start with empty messages
  useEffect(() => {
    setMessages([]);
  }, []);

  const handleSendMessage = useCallback(async (formData) => {
    const userMessageId = Date.now();
    const newUserMessage = {
      id: userMessageId,
      type: 'user',
      content: formData.businessDescription,
      settings: {
        llmModel: formData.llmModel,
        imageModel: formData.imageModel,
        galleryImages: formData.galleryImages
      },
      timestamp: new Date()
    };

    // Add user message immediately
    setMessages(prev => [...prev, newUserMessage]);
    setIsLoading(true);
    setHasActiveJob(true);

    try {
      // Start image generation job
      const jobResponse = await ImageGenerationAPI.startImageGeneration({
        prompt: formData.businessDescription,
        gallery_count: formData.galleryImages,
        llm_model: formData.llmModel,
        image_model: formData.imageModel
      });

      const { job_id } = jobResponse;

      // Add loading message
      const loadingMessage = {
        id: Date.now() + 1,
        type: 'loading',
        jobId: job_id,
        jobData: {
          job_id,
          status: 'init',
          message: 'Job started',
          total_images: formData.galleryImages,
          completed_images: 0
        },
        timestamp: new Date()
      };

      setMessages(prev => [...prev, loadingMessage]);

      // Start polling for job status
      startPolling(job_id, loadingMessage.jobData);

    } catch (error) {
      console.error('Failed to start image generation:', error);
      const errorInfo = handleApiError(error, 'start generation');
      
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant-error',
        error: errorInfo,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
      setHasActiveJob(false);
    } finally {
      setIsLoading(false);
    }
  }, [startPolling]);

  const handleRetry = useCallback((originalMessage) => {
    if (originalMessage.type === 'user' && originalMessage.settings) {
      handleSendMessage({
        businessDescription: originalMessage.content,
        ...originalMessage.settings
      });
    }
  }, [handleSendMessage]);

  // Cleanup polling on unmount
  useEffect(() => {
    return () => {
      stopAllPolling();
    };
  }, [stopAllPolling]);

  return (
    <div className="chat-container">
      <MessageList 
        messages={messages} 
        isLoading={isLoading} 
        onRetry={handleRetry}
      />
      <InputArea onSendMessage={handleSendMessage} isLoading={isLoading || hasActiveJob} />
    </div>
  );
};

export default ChatContainer;
