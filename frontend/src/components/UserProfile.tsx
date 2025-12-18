'use client';

import React from 'react';
import { useAuth } from '@/contexts/auth';
import { format } from 'date-fns';

const UserProfile: React.FC = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[200px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">Please log in to view your profile.</p>
      </div>
    );
  }

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">User Profile</h2>

      <div className="space-y-4">
        <div className="flex items-center">
          <span className="font-medium text-gray-700 w-32">Email:</span>
          <span className="text-gray-900">{user.email}</span>
        </div>

        <div className="flex items-center">
          <span className="font-medium text-gray-700 w-32">ID:</span>
          <span className="text-gray-900">{user.id}</span>
        </div>

        <div className="flex items-center">
          <span className="font-medium text-gray-700 w-32">Status:</span>
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            user.is_active
              ? 'bg-green-100 text-green-800'
              : 'bg-red-100 text-red-800'
          }`}>
            {user.is_active ? 'Active' : 'Inactive'}
          </span>
        </div>

        <div className="flex items-center">
          <span className="font-medium text-gray-700 w-32">Created:</span>
          <span className="text-gray-900">
            {user.createdAt ? format(new Date(user.createdAt), 'MMM d, yyyy h:mm a') : 'N/A'}
          </span>
        </div>

        <div className="flex items-center">
          <span className="font-medium text-gray-700 w-32">Updated:</span>
          <span className="text-gray-900">
            {user.updatedAt ? format(new Date(user.updatedAt), 'MMM d, yyyy h:mm a') : 'N/A'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;