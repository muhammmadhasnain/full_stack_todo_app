'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/auth';
import LoginForm from '@/components/auth/LoginForm';
import AuthFormWrapper from '@/components/auth/AuthFormWrapper';

const LoginPage: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  // Redirect AFTER render
  useEffect(() => {
    if (isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated, router]);

  // Redirect hone tak kuch render na ho
  if (isAuthenticated) {
    return null;
  }

  return (
    <AuthFormWrapper
      title="Sign in to your account"
      subtitle="Enter your credentials to access your todo list"
    >
      <LoginForm />
    </AuthFormWrapper>
  );
};

export default LoginPage;
