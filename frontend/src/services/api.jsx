import axios from 'axios';

const API_BASE_URL = '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      // Only redirect if not already on login/signup page
      if (!window.location.pathname.includes('/login') && !window.location.pathname.includes('/signup')) {
        window.location.href = '/login';
      }
    }
    // Ensure error message is properly formatted
    if (error.response?.data?.detail) {
      error.message = error.response.data.detail;
    } else if (error.response?.data?.message) {
      error.message = error.response.data.message;
    } else if (!error.message) {
      error.message = 'An error occurred. Please try again.';
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login/json', data),
};

// User APIs
export const userAPI = {
  getMe: () => api.get('/users/me'),
  getStats: () => api.get('/users/me/stats'),
  update: (data) => api.put('/users/me', data),
};

// Resume APIs
export const resumeAPI = {
  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/resume/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getAll: () => api.get('/resume/'),
  getOne: (id) => api.get(`/resume/${id}`),
  delete: (id) => api.delete(`/resume/${id}`),
};

// Job APIs
export const jobAPI = {
  create: (data) => api.post('/job/', data),
  getAll: () => api.get('/job/'),
  getOne: (id) => api.get(`/job/${id}`),
  delete: (id) => api.delete(`/job/${id}`),
};

// Analysis APIs
export const analysisAPI = {
  analyze: (resumeId, jobId) => api.post('/analysis/analyze', { resume_id: resumeId, job_id: jobId }),
  getHistory: (limit = 10) => api.get(`/analysis/?limit=${limit}`),
  getOne: (id) => api.get(`/analysis/${id}`),
  delete: (id) => api.delete(`/analysis/${id}`),
};

// Dashboard APIs
export const dashboardAPI = {
  getStats: () => api.get('/dashboard/stats'),
};

export default api;

