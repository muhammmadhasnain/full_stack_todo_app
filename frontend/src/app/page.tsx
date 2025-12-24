'use client';

import TaskInput from '@/components/TaskInput';
import TaskList from '@/components/TaskList';
import { useAuth } from '@/contexts/auth';

export default function Home() {
  const { user, isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">Tasks Add Form</h1>

        {isAuthenticated && user ? (
          <div className="space-y-6">
            <TaskInput />
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-600">Please login to manage your tasks.</p>
          </div>
        )}
      </main>
    </div>
  );
}