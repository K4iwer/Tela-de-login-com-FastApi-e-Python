import axios from 'axios';
import type { LoginRequest, RegisterRequest, LoginResponse, RegisterResponse, User } from '@/types/api';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Para enviar cookies automaticamente
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar CSRF token nos headers quando disponível
api.interceptors.request.use((config) => {
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrf_access_token='))
    ?.split('=')[1];
  
  if (csrfToken) {
    config.headers['X-CSRF-TOKEN'] = csrfToken;
  }
  
  return config;
});

export const authApi = {
  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await api.post('/login', data);
    return response.data;
  },

  register: async (data: RegisterRequest): Promise<RegisterResponse> => {
    const response = await api.post('/register', data);
    return response.data;
  },

  logout: async (): Promise<{ message: string }> => {
    const response = await api.post('/logout');
    return response.data;
  },

  getUser: async (userId: number): Promise<User> => {
    const response = await api.get(`/user/${userId}`);
    return response.data;
  },

  refreshToken: async (): Promise<{ message: string }> => {
    const response = await api.post('/refresh');
    return response.data;
  },

  getStatus: async (): Promise<{ status: string }> => {
    const response = await api.get('/status');
    return response.data;
  },
};

export default api;