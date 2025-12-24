// frontend/src/components/TodoList.tsx

'use client';

import React from 'react';
import { useTodo } from '@/contexts/TodoContext';
import TodoItem from './TodoItem';
import TodoFilter from './TodoFilter';
import AddTodoForm from './AddTodoForm';

const TodoList: React.FC = () => {
  const { state } = useTodo();

  // Filter todos based on status
  const filteredTodos = state.todos.filter(todo => {
    if (state.filters.status === 'active') {
      return !todo.completed;
    }
    if (state.filters.status === 'completed') {
      return todo.completed;
    }
    return true; // 'all' status
  });

  // Further filter by search term
  const searchedTodos = filteredTodos.filter(todo => {
    if (!state.filters.search) return true;
    const searchTerm = state.filters.search.toLowerCase();
    return (
      todo.title.toLowerCase().includes(searchTerm) ||
      (todo.description && todo.description.toLowerCase().includes(searchTerm))
    );
  });

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">Todo App</h1>

      <AddTodoForm />

      <TodoFilter />

      {state.loading ? (
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
          <p className="mt-2 text-gray-600">Loading todos...</p>
        </div>
      ) : state.error ? (
        <div className="p-4 bg-red-100 text-red-700 rounded-md mb-4">
          Error: {state.error}
        </div>
      ) : (
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-gray-800">
              {searchedTodos.length} {searchedTodos.length === 1 ? 'Todo' : 'Todos'}
            </h2>
          </div>

          {searchedTodos.length === 0 ? (
            <div className="text-center py-8 bg-white rounded-lg border border-gray-200">
              <p className="text-gray-500">
                {state.filters.search || state.filters.status !== 'all'
                  ? 'No todos match your filters.'
                  : 'No todos yet. Add a new todo to get started!'}
              </p>
            </div>
          ) : (
            <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
              {searchedTodos.map(todo => (
                <TodoItem key={todo.id} todo={todo} />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TodoList;