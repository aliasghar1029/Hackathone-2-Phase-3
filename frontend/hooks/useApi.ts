// hooks/useApi.ts
import { useState, useEffect } from 'react';
import { authApi } from '@/lib/auth-api';
import { tasksApi } from '@/lib/tasks-api';
import { chatApi } from '@/lib/chat-api';
import { verifyEndpoints } from '@/utils/verify-endpoints';

// Custom hook to provide access to all API services
export const useApi = () => {
  const [isConnected, setIsConnected] = useState<boolean | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Verify connection to backend
  useEffect(() => {
    const checkConnection = async () => {
      try {
        const result = await verifyEndpoints();
        setIsConnected(result.success);
      } catch (error) {
        console.error('Failed to verify endpoints:', error);
        setIsConnected(false);
      } finally {
        setLoading(false);
      }
    };

    checkConnection();
  }, []);

  return {
    auth: authApi,
    tasks: tasksApi,
    chat: chatApi,
    isConnected,
    loading,
    verifyEndpoints
  };
};

// Custom hook for authentication state
export const useAuthState = () => {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const storedToken = localStorage.getItem('auth_token');
    const storedUser = localStorage.getItem('user');

    if (storedToken) setToken(storedToken);
    if (storedUser) setUser(JSON.parse(storedUser));

    setLoading(false);
  }, []);

  const login = (userData: { token: string; user: any }) => {
    localStorage.setItem('auth_token', userData.token);
    localStorage.setItem('user', JSON.stringify(userData.user));
    setToken(userData.token);
    setUser(userData.user);
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
  };

  return {
    token,
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!token
  };
};