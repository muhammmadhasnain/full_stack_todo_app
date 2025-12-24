'use client';

import React from 'react';
import UserProfile from '@/components/UserProfile';
import { useAuth } from '@/contexts/auth';
import { useRouter } from 'next/navigation';

const ProfilePage: React.FC = () => {
  const { user, loading, isAuthenticated } = useAuth();
  const router = useRouter();

  React.useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, loading, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Redirect will happen in useEffect
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Profile</h1>
      <UserProfile />
    </div>
  );
};

export default ProfilePage;