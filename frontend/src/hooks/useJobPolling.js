import { useState, useEffect, useCallback, useRef } from 'react';
import { ImageGenerationAPI, handleApiError } from '../services/api';

const useJobPolling = (onJobUpdate, onJobComplete, onJobError) => {
  const [activeJobs, setActiveJobs] = useState(new Map());
  const intervalsRef = useRef(new Map());

  const startPolling = useCallback((jobId, initialData = null) => {
    // Don't start polling if already polling this job
    if (intervalsRef.current.has(jobId)) {
      return;
    }

    // Add job to active jobs
    setActiveJobs(prev => new Map(prev.set(jobId, initialData || { status: 'init' })));

    const pollJob = async () => {
      try {
        const jobData = await ImageGenerationAPI.getJobStatus(jobId);
        
        // Update active jobs state
        setActiveJobs(prev => new Map(prev.set(jobId, jobData)));
        
        // Call update callback
        if (onJobUpdate) {
          onJobUpdate(jobId, jobData);
        }

        // Check if job is complete or failed
        if (jobData.status === 'completed') {
          clearInterval(intervalsRef.current.get(jobId));
          intervalsRef.current.delete(jobId);
          
          if (onJobComplete) {
            onJobComplete(jobId, jobData);
          }
          
          // Keep completed job in activeJobs but stop polling
          return;
        }

        if (jobData.status === 'failed') {
          clearInterval(intervalsRef.current.get(jobId));
          intervalsRef.current.delete(jobId);
          
          const error = {
            message: jobData.error || 'Job failed',
            status: 'job_failed',
            code: 'JOB_FAILED'
          };
          
          if (onJobError) {
            onJobError(jobId, error, jobData);
          }
          
          // Remove failed job from active jobs
          setActiveJobs(prev => {
            const newMap = new Map(prev);
            newMap.delete(jobId);
            return newMap;
          });
          
          return;
        }

      } catch (error) {
        console.error(`Polling error for job ${jobId}:`, error);
        
        // Handle polling errors
        const errorInfo = handleApiError(error, 'polling');
        
        // Stop polling on repeated errors
        clearInterval(intervalsRef.current.get(jobId));
        intervalsRef.current.delete(jobId);
        
        if (onJobError) {
          onJobError(jobId, errorInfo);
        }
        
        // Remove job from active jobs on error
        setActiveJobs(prev => {
          const newMap = new Map(prev);
          newMap.delete(jobId);
          return newMap;
        });
      }
    };

    // Wait 1 second, then start polling every 3 seconds
    setTimeout(() => {
      pollJob();
      const intervalId = setInterval(pollJob, 3000);
      intervalsRef.current.set(jobId, intervalId);
    }, 1000);

  }, [onJobUpdate, onJobComplete, onJobError]);

  const stopPolling = useCallback((jobId) => {
    if (intervalsRef.current.has(jobId)) {
      clearInterval(intervalsRef.current.get(jobId));
      intervalsRef.current.delete(jobId);
    }
    
    setActiveJobs(prev => {
      const newMap = new Map(prev);
      newMap.delete(jobId);
      return newMap;
    });
  }, []);

  const stopAllPolling = useCallback(() => {
    intervalsRef.current.forEach((intervalId) => {
      clearInterval(intervalId);
    });
    intervalsRef.current.clear();
    setActiveJobs(new Map());
  }, []);

  const getJobData = useCallback((jobId) => {
    return activeJobs.get(jobId);
  }, [activeJobs]);

  const isJobActive = useCallback((jobId) => {
    return activeJobs.has(jobId);
  }, [activeJobs]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      intervalsRef.current.forEach((intervalId) => {
        clearInterval(intervalId);
      });
      intervalsRef.current.clear();
    };
  }, []);

  // Cleanup on page visibility change
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden) {
        // Optionally pause polling when page is hidden
        // For now, keep polling to ensure we don't miss updates
      } else {
        // Resume polling if needed
        // Could implement exponential backoff here
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  return {
    activeJobs: Array.from(activeJobs.entries()),
    startPolling,
    stopPolling,
    stopAllPolling,
    getJobData,
    isJobActive
  };
};

export default useJobPolling;
