'use client';

import TaskInput from '@/components/TaskInput';

import TaskList from '@/components/TaskList';
import { useAuth } from '@/contexts/auth';

const TasksPage: React.FC = () => {
  const { user, isAuthenticated } = useAuth();

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 font-sans">
      <main className="flex min-h-screen w-full max-w-4xl flex-col py-8 px-4 bg-white">
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">My Tasks</h1>

        {isAuthenticated && user ? (
          <>

            
           
            <TaskList /> 
           
          </>
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