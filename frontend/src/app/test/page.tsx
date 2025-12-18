'use client';

import React from 'react';
import TaskInput from '@/components/TaskInput';
import TaskList from '@/components/TaskList';
import { useAuth } from '@/contexts/auth';

const TestPage: React.FC = () => {
  const { user, isAuthenticated } = useAuth();

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Test Page</h1>

      {isAuthenticated && user ? (
        <div className="space-y-8">
          <TaskInput />
          <TaskList />
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-gray-600">Please log in to test the features.</p>
        </div>
      )}
    </div>
  );
};

export default TestPage;