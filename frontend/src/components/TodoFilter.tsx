// frontend/src/components/TodoFilter.tsx

'use client';

import React from 'react';
import { TodoFilters } from '@/types/todo';
import { useTodo } from '@/contexts/TodoContext';

const TodoFilter: React.FC = () => {
  const { state, setFilters } = useTodo();

  const handleStatusChange = (status: 'all' | 'active' | 'completed') => {
    setFilters({ ...state.filters, status });
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilters({ ...state.filters, search: e.target.value });
  };

  return (
    <div className="mb-6 p-4 bg-white rounded-lg shadow-md border border-gray-200">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">Filter Todos</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Status
          </label>
          <div className="flex space-x-4">
            {(['all', 'active', 'completed'] as const).map((status) => (
              <button
                key={status}
                onClick={() => handleStatusChange(status)}
                className={`px-4 py-2 rounded-md capitalize ${
                  state.filters.status === status
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
                }`}
                aria-pressed={state.filters.status === status}
              >
                {status}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
            Search
          </label>
          <input
            type="text"
            id="search"
            value={state.filters.search || ''}
            onChange={handleSearchChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Search todos..."
          />
        </div>
      </div>
    </div>
  );
};

export default TodoFilter;