import { useState, useEffect, useCallback } from 'react';
import { reportAPI, uploadAPI, reviewAPI, chatAPI } from '../services/api';

export function useReports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchReports = useCallback(async (skip = 0, limit = 20) => {
    setLoading(true);
    setError(null);
    try {
      const response = await reportAPI.list(skip, limit);
      setReports(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch reports');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchReports();
  }, [fetchReports]);

  return { reports, loading, error, refetch: fetchReports };
}

export function useDashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchDashboard = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await reportAPI.getDashboard();
      setDashboard(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch dashboard');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboard();
  }, [fetchDashboard]);

  return { dashboard, loading, error, refetch: fetchDashboard };
}

export function useReport(id) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchReport = useCallback(async () => {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const response = await reportAPI.get(id);
      setReport(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch report');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchReport();
  }, [fetchReport]);

  const deleteReport = async () => {
    try {
      await reportAPI.delete(id);
      return { success: true };
    } catch (err) {
      return { success: false, error: err.response?.data?.detail };
    }
  };

  return { report, loading, error, refetch: fetchReport, deleteReport };
}

export function useUpload() {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);
  const [uploadedReport, setUploadedReport] = useState(null);

  const uploadFile = async (file) => {
    setUploading(true);
    setProgress(0);
    setError(null);
    setUploadedReport(null);

    try {
      const response = await uploadAPI.upload(file);
      setUploadedReport(response.data);
      setProgress(100);

      // Start polling for processing status
      pollProcessingStatus(response.data.id);

      return { success: true, report: response.data };
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed');
      setUploading(false);
      return { success: false, error: err.response?.data?.detail };
    }
  };

  const pollProcessingStatus = async (reportId) => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await uploadAPI.getStatus(reportId);
        const status = response.data.status;

        if (status === 'completed' || status === 'failed') {
          clearInterval(pollInterval);
          // Refresh reports list
          const event = new CustomEvent('report-updated', { detail: { reportId } });
          window.dispatchEvent(event);
        }
      } catch (err) {
        clearInterval(pollInterval);
      }
    }, 2000);

    // Stop polling after 5 minutes
    setTimeout(() => clearInterval(pollInterval), 5 * 60 * 1000);
  };

  return { uploading, progress, error, uploadedReport, uploadFile };
}

export function useReview(reportId) {
  const [review, setReview] = useState(null);
  const [sections, setSections] = useState([]);
  const [issues, setIssues] = useState([]);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const [demoMode, setDemoMode] = useState(false);

  const analyzeReport = useCallback(async () => {
    if (!reportId) return;
    setAnalyzing(true);
    setError(null);

    try {
      const response = await reviewAPI.analyze(reportId);
      setDemoMode(response.data.demo_mode || false);
      setReview(response.data.analysis);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed');
    } finally {
      setAnalyzing(false);
    }
  }, [reportId]);

  const fetchReviewData = useCallback(async () => {
    if (!reportId) return;
    try {
      const response = await reviewAPI.getReviewData(reportId);
      if (response.data.review) {
        setReview(response.data.review);
        setSections(response.data.sections || []);
        setIssues(response.data.issues || []);
      }
    } catch (err) {
      // 404 just means no review exists yet - the user can trigger analysis
      console.error('Failed to fetch review data:', err);
    }
  }, [reportId]);

  useEffect(() => {
    fetchReviewData();
  }, [fetchReviewData]);

  return {
    review,
    sections,
    issues,
    analyzing,
    error,
    demoMode,
    analyzeReport,
    refetchReview: fetchReviewData,
  };
}

export function useImprovement() {
  const [improving, setImproving] = useState(false);
  const [error, setError] = useState(null);

  const improveText = async (text, type, instructions = null, context = null) => {
    setImproving(true);
    setError(null);

    try {
      const response = await reviewAPI.improveText({
        text,
        improvement_type: type,
        instructions,
        report_context: context,
      });
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Improvement failed');
      return null;
    } finally {
      setImproving(false);
    }
  };

  return { improving, error, improveText };
}

export function useChat(reportId) {
  const [messages, setMessages] = useState([]);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);
  const [suggestedQuestions, setSuggestedQuestions] = useState([]);
  const [context, setContext] = useState(null);
  const [demoMode, setDemoMode] = useState(false);

  // Load context when reportId changes
  useEffect(() => {
    if (reportId) {
      loadContext();
      loadSuggestedQuestions();
    }
  }, [reportId]);

  const loadContext = async () => {
    try {
      const response = await chatAPI.getContext(reportId);
      setContext(response.data);
    } catch (err) {
      console.error('Failed to load context:', err);
    }
  };

  const loadSuggestedQuestions = async () => {
    try {
      const response = await chatAPI.getSuggestedQuestions(reportId);
      setSuggestedQuestions(response.data.questions || []);
    } catch (err) {
      console.error('Failed to load questions:', err);
    }
  };

  const sendMessage = async (content) => {
    const userMessage = { role: 'user', content };
    setMessages((prev) => [...prev, userMessage]);
    setSending(true);
    setError(null);

    try {
      const response = await chatAPI.chat({
        messages: [...messages, userMessage],
        report_context: context?.extracted_text,
        report_summary: context?.review_summary,
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setSuggestedQuestions(response.data.suggested_questions || []);
      setDemoMode(response.data.demo_mode || false);

      return assistantMessage;
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send message');
      return null;
    } finally {
      setSending(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return {
    messages,
    sending,
    error,
    suggestedQuestions,
    context,
    demoMode,
    sendMessage,
    clearChat,
    loadSuggestedQuestions,
  };
}
