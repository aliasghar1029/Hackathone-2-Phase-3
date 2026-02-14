// lib/auth-api.ts
import { apiClient } from './api';

export interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface UserResponse {
  user: User;
  token: string;
}

export interface UserCredentials {
  email: string;
  password: string;
}

export interface UserSignupData extends UserCredentials {
  name: string;
}

// Authentication API functions
export const authApi = {
  // Sign up a new user
  signup: async (userData: UserSignupData): Promise<{ data?: UserResponse; error?: string }> => {
    return apiClient.post<UserResponse>('/api/auth/signup', userData);
  },

  // Sign in an existing user
  signin: async (credentials: UserCredentials): Promise<{ data?: UserResponse; error?: string }> => {
    return apiClient.post<UserResponse>('/api/auth/signin', credentials);
  },

  // Check if user is authenticated (by verifying token)
  checkAuth: async (): Promise<boolean> => {
    const token = localStorage.getItem('authToken');
    if (!token) return false;

    try {
      // We could make a request to a protected endpoint to verify the token
      // For now, we'll just return true if a token exists
      // In a real implementation, you might have a /me endpoint
      return true;
    } catch (error) {
      console.error('Token verification failed:', error);
      return false;
    }
  },

  // Logout user
  logout: (): void => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
  },

  // Store authentication data
  storeAuthData: (data: UserResponse): void => {
    localStorage.setItem('auth_token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
  },

  // Get stored user data
  getStoredUser: (): User | null => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  // Get stored token
  getStoredToken: (): string | null => {
    return localStorage.getItem('auth_token');
  },
};