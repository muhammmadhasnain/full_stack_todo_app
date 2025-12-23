'use client';

import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { taskService } from '../lib/api';
import { User, TokenResponse } from '@/types/task';

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  // Check for existing tokens on initial load
  useEffect(() => {
    const initializeAuth = async () => {
      const storedAccessToken = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
      const storedRefreshToken = typeof window !== 'undefined' ? localStorage.getItem('refresh_token') : null;

      if (storedAccessToken && storedRefreshToken) {
        // Verify if the token is still valid by trying to get user profile
        try {
          const userProfile = await taskService.getUserProfile();
          setUser(userProfile);
          taskService.setTokens(storedAccessToken, storedRefreshToken);
          setToken(storedAccessToken);
          setIsAuthenticated(true);
        } catch (error) {
          // If token verification fails, clear stored tokens
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          console.error('Token verification failed:', error);
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response: TokenResponse = await taskService.login({ email, password });

      // Store both access and refresh tokens
      taskService.setTokens(response.access_token, response.refresh_token);
      setToken(response.access_token);
      setUser(response.user);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (email: string, password: string, name: string) => {
    try {
      const response: TokenResponse = await taskService.register({ email, password, name });

      // Store both access and refresh tokens
      taskService.setTokens(response.access_token, response.refresh_token);
      setToken(response.access_token);
      setUser(response.user);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = () => {
    taskService.clearTokens();
    setUser(null);
    setToken(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    token,
    login,
    register,
    logout,
    isAuthenticated,
    loading,
  };

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>;
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};