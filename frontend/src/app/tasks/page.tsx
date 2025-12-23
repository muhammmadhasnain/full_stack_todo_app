'use client';

import TaskInput from '@/components/TaskInput';
import TaskList from '@/components/TaskList';
import { useAuth } from '@/contexts/auth';

const TasksPage: React.FC = () => {
  const { user, isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">My Tasks</h1>

        {isAuthenticated && user ? (
          <div className="space-y-6">
            <TaskInput />
            <TaskList />
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-600">Please login to manage your tasks.</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default TasksPage;