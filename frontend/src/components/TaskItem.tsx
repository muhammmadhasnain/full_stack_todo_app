'use client';

import React, { useState } from 'react';
import { Task, UpdateTaskRequest, RecurrencePattern } from '@/types/task';
import { useAuth } from '@/contexts/auth';
import { useTask } from '@/contexts/task';
import { useToast } from '@/contexts/toast';
import RecurrencePatternForm from './RecurrencePatternForm';

interface TaskItemProps {
  task: Task;
}

const TaskItem: React.FC<TaskItemProps> = ({ task }) => {
  const { user } = useAuth();
  const { updateTask, deleteTask, toggleTaskCompletion } = useTask();
  const { showToast } = useToast();
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>(task.priority as 'low' | 'medium' | 'high');
  const [status, setStatus] = useState<'pending' | 'in-progress' | 'completed' | 'cancelled' | 'on_hold'>(task.status as 'pending' | 'in-progress' | 'completed' | 'cancelled' | 'on_hold');
  const [tags, setTags] = useState(task.tags || '');
  const [recurrencePattern, setRecurrencePattern] = useState<RecurrencePattern | undefined>(task.recurrencePattern);
  const [loading, setLoading] = useState(false);

  const handleToggleComplete = async () => {
    if (!user) return;

    setLoading(true);
    try {
      await toggleTaskCompletion(task.id, !task.completed);
      showToast(`Task ${!task.completed ? 'completed' : 'marked as pending'} successfully!`, 'success');
    } catch (err) {
      console.error('Error toggling task completion:', err);
      showToast('Failed to update task. Please try again.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!user) return;

    if (window.confirm('Are you sure you want to delete this task?')) {
      setLoading(true);
      try {
        await deleteTask(task.id);
        showToast('Task deleted successfully!', 'success');
      } catch (err) {
        console.error('Error deleting task:', err);
        showToast('Failed to delete task. Please try again.', 'error');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleSaveEdit = async () => {
    if (!user) return;

    setLoading(true);
    try {
      const updateData: UpdateTaskRequest = {
        title,
        description: description || undefined,
        priority,
        status,
        tags: tags || undefined,
        recurrencePattern: recurrencePattern || undefined,
      };

      await updateTask(task.id, updateData);
      setIsEditing(false);
      showToast('Task updated successfully!', 'success');
    } catch (err) {
      console.error('Error updating task:', err);
      showToast('Failed to update task. Please try again.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelEdit = () => {
    setTitle(task.title);
    setDescription(task.description || '');
    setPriority(task.priority as 'low' | 'medium' | 'high');
    setStatus(task.status as 'pending' | 'in-progress' | 'completed' | 'cancelled' | 'on_hold');
    setTags(task.tags || '');
    setRecurrencePattern(task.recurrencePattern);
    setIsEditing(false);
  };

  if (!user) {
    return <div>Please log in to manage tasks</div>;
  }

  // Determine priority color
  const priorityColor = task.priority === 'high'
    ? 'priority-high bg-red-100 text-red-800'
    : task.priority === 'medium'
      ? 'priority-medium bg-yellow-100 text-yellow-800'
      : 'priority-low bg-green-100 text-green-800';

  // Format due date if exists
  const formattedDueDate = task.dueDate
    ? new Date(task.dueDate).toLocaleString()
    : null;

  return (
    <div className={`border rounded-lg p-4 mb-3 shadow-sm ${task.completed ? 'bg-gray-50' : 'bg-white'}`}>
      {isEditing ? (
        <div className="space-y-3">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 text-lg font-medium"
            required
          />

          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            rows={2}
          />

          <input
            type="text"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            placeholder="Enter tags (comma-separated)"
            className="w-full px-3 py-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
          />

          <div className="space-y-4">
            <div className="flex flex-wrap items-center gap-2">
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as 'low' | 'medium' | 'high')}
                className="px-2 py-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>

              <select
                value={status}
                onChange={(e) => setStatus(e.target.value as 'pending' | 'in-progress' | 'completed' | 'cancelled' | 'on_hold')}
                className="px-2 py-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="pending">Pending</option>
                <option value="in-progress">In Progress</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
                <option value="on_hold">On Hold</option>
              </select>

              <button
                onClick={handleSaveEdit}
                disabled={loading}
                className="px-3 py-1 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
              >
                Save
              </button>

              <button
                onClick={handleCancelEdit}
                disabled={loading}
                className="px-3 py-1 bg-gray-500 text-white rounded-md hover:bg-gray-600 disabled:opacity-50"
              >
                Cancel
              </button>
            </div>

            <RecurrencePatternForm
              recurrencePattern={recurrencePattern}
              onPatternChange={setRecurrencePattern}
            />
          </div>
        </div>
      ) : (
        <>
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-3 flex-1">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={handleToggleComplete}
                disabled={loading}
                className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />

              <div className="flex-1">
                <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                  {task.title}
                </h3>

                {task.description && (
                  <p className={`mt-1 text-sm ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                    {task.description}
                  </p>
                )}

                <div className="mt-2 flex flex-wrap gap-2">
                  <span className={`text-xs px-2 py-1 rounded-full ${priorityColor}`}>
                    {priority}
                  </span>

                  <span className={`text-xs px-2 py-1 rounded-full ${
                    task.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                    task.status === 'in-progress' ? 'bg-blue-100 text-blue-800' :
                    task.status === 'completed' ? 'bg-green-100 text-green-800' :
                    task.status === 'cancelled' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {task.status.replace('-', ' ')}
                  </span>

                  {task.tags && (
                    <span className="text-xs px-2 py-1 bg-gray-100 text-gray-800 rounded-full">
                      {task.tags}
                    </span>
                  )}

                  {formattedDueDate && (
                    <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                      Due: {formattedDueDate}
                    </span>
                  )}

                  {task.recurrencePattern && (
                    <span className="text-xs px-2 py-1 bg-purple-100 text-purple-800 rounded-full">
                      {task.recurrencePattern.type || 'Recurring'}
                    </span>
                  )}
                </div>

                <div className="mt-2 text-xs text-gray-500">
                  Created: {new Date(task.createdAt).toLocaleString()}
                  {task.completedAt && (
                    <span>, Completed: {new Date(task.completedAt).toLocaleString()}</span>
                  )}
                </div>
              </div>
            </div>

            <div className="flex space-x-1 ml-2">
              <button
                onClick={() => setIsEditing(true)}
                disabled={loading}
                className="p-1 text-gray-500 hover:text-blue-600 disabled:opacity-50"
                aria-label="Edit task"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </button>

              <button
                onClick={handleDelete}
                disabled={loading}
                className="p-1 text-gray-500 hover:text-red-600 disabled:opacity-50"
                aria-label="Delete task"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
          
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default TaskItem;