import api from './api';
import { AuthResponse } from '../types/models';

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api';

export const authService = {
  async register(email: string, password: string): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/register', { email, password });
    return response.data;
  },

  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/login', { email, password });
    return response.data;
  },

  getGoogleOAuthUrl(): string {
    return `${API_BASE_URL}/auth/google`;
  },
};
