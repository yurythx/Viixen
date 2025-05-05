// src/lib/auth.ts
import { api } from './api';

export const login = async (email: string, password: string) => {
  const response = await api.post('/v1/auth/jwt/create/', { email, password });
  const accessToken = response.data.access;
  const refreshToken = response.data.refresh;
  localStorage.setItem('access_token', accessToken);
  localStorage.setItem('refresh_token', refreshToken);
  return accessToken;
};

export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};