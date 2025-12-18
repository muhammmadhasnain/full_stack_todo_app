'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/auth';
import RegisterForm from '@/components/auth/RegisterForm';
import AuthFormWrapper from '@/components/auth/AuthFormWrapper';

const RegisterPage: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  // Redirect ko render ke baad execute karna
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
      title="Create a new account"
      subtitle="Enter your details to get started with your todo list"
    >
      <RegisterForm />
    </AuthFormWrapper>
  );
};

export default RegisterPage;
