// frontend/src/components/TodoItem.tsx

'use client';

import React, { useState } from 'react';
import { Todo, UpdateTodoData } from '@/types/todo';
import { useTodo } from '@/contexts/TodoContext';

interface TodoItemProps {
  todo: Todo;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo }) => {
  const { updateTodo, deleteTodo, toggleTodo } = useTodo();
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');

  const handleToggle = async () => {
    await toggleTodo(todo.id);
  };

  const handleEdit = async () => {
    if (editTitle.trim() === '') return;

    const updateData: UpdateTodoData = {
      title: editTitle.trim(),
      description: editDescription.trim() || undefined,
    };

    await updateTodo(todo.id, updateData);
    setIsEditing(false);
  };

  const handleDelete = async () => {
    await deleteTodo(todo.id);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleEdit();
    } else if (e.key === 'Escape') {
      setIsEditing(false);
      setEditTitle(todo.title);
      setEditDescription(todo.description || '');
    }
  };

  return (
    <div className={`flex items-center p-4 mb-2 rounded-lg border ${
      todo.completed
        ? 'bg-green-50 border-green-200'
        : 'bg-white border-gray-200 shadow-sm'
    }`}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={handleToggle}
        className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500 mr-3 cursor-pointer"
        aria-label={`Mark todo "${todo.title}" as ${todo.completed ? 'incomplete' : 'complete'}`}
      />

      <div className="flex-1 min-w-0">
        {isEditing ? (
          <div className="space-y-2">
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              onKeyDown={handleKeyDown}
              className="w-full px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              autoFocus
            />
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Description (optional)"
              className="w-full px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mt-1"
              rows={2}
            />
          </div>
        ) : (
          <div>
            <h3 className={`text-lg font-medium ${
              todo.completed ? 'line-through text-gray-500' : 'text-gray-900'
            }`}>
              {todo.title}
            </h3>
            {todo.description && (
              <p className={`text-sm mt-1 ${
                todo.completed ? 'line-through text-gray-400' : 'text-gray-600'
              }`}>
                {todo.description}
              </p>
            )}
            <p className="text-xs text-gray-500 mt-1">
              Created: {new Date(todo.createdAt).toLocaleDateString()}
            </p>
          </div>
        )}
      </div>

      <div className="flex space-x-2 ml-4">
        {isEditing ? (
          <>
            <button
              onClick={handleEdit}
              className="px-3 py-1 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 text-sm"
              aria-label="Save changes"
            >
              Save
            </button>
            <button
              onClick={() => {
                setIsEditing(false);
                setEditTitle(todo.title);
                setEditDescription(todo.description || '');
              }}
              className="px-3 py-1 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 text-sm"
              aria-label="Cancel editing"
            >
              Cancel
            </button>
          </>
        ) : (
          <>
            <button
              onClick={() => setIsEditing(true)}
              className="px-3 py-1 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 text-sm"
              aria-label="Edit todo"
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              className="px-3 py-1 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 text-sm"
              aria-label="Delete todo"
            >
              Delete
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default TodoItem;