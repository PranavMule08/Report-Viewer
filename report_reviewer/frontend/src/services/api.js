import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// Auth APIs
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login/json', data),
  logout: () => api.post('/auth/logout'),
  getMe: () => api.get('/auth/me'),
};

// Report APIs
export const reportAPI = {
  list: (skip = 0, limit = 20) => api.get('/reports', { params: { skip, limit } }),
  get: (id) => api.get(`/reports/${id}`),
  getDashboard: () => api.get('/reports/dashboard'),
  getReview: (id) => api.get(`/reports/${id}/review`),
  delete: (id) => api.delete(`/reports/${id}`),
  getText: (id) => api.get(`/reports/${id}/text`),
  getCategoryScores: (id) => api.get(`/reviews/categories/scores?report_id=${id}`),
};

// Upload APIs
export const uploadAPI = {
  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/upload/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getStatus: (id) => api.get(`/upload/status/${id}`),
  listUploads: () => api.get('/upload/files'),
};

// Review APIs
export const reviewAPI = {
  analyze: (reportId) => api.post(`/reviews/${reportId}/analyze`),
  getReviewData: (reportId) => api.get(`/reviews/${reportId}/review-data`),
  improveText: (data) => api.post('/reviews/improve', data),
};

// Chat APIs
export const chatAPI = {
  chat: (data) => api.post('/chat', data),
  getSuggestedQuestions: (reportId) => api.get(`/chat/suggested-questions?report_id=${reportId}`),
  getContext: (reportId) => api.get(`/chat/context/${reportId}`),
};

// Config
export const configAPI = {
  get: () => api.get('/config'),
};
