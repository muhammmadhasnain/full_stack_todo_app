'use client';

import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { Task, TaskFilter, CreateTaskRequest, UpdateTaskRequest } from '@/types/task';
import { taskService } from '../lib/api';
import { useAuth } from './auth';

interface TaskContextType {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  fetchTasks: (filters?: TaskFilter) => Promise<void>;
  createTask: (taskData: CreateTaskRequest) => Promise<Task>;
  updateTask: (taskId: string, taskData: UpdateTaskRequest) => Promise<Task>;
  deleteTask: (taskId: string) => Promise<void>;
  toggleTaskCompletion: (taskId: string, completed: boolean) => Promise<Task>;
}

const TaskContext = createContext<TaskContextType | undefined>(undefined);

interface TaskProviderProps {
  children: ReactNode;
}

export const TaskProvider: React.FC<TaskProviderProps> = ({ children }) => {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async (filters?: TaskFilter) => {
    if (!user) return;

    setLoading(true);
    setError(null);

    try {
      const tasksData = await taskService.getTasks(user.id, filters);
      setTasks(tasksData);
    } catch (err) {
      console.error('Error fetching tasks:', err);
      setError('Failed to load tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const createTask = async (taskData: CreateTaskRequest): Promise<Task> => {
    if (!user) throw new Error('User not authenticated');

    // Optimistic update: add task to the list immediately
    const tempId = `temp-${Date.now()}`;
    const optimisticTask = {
      id: tempId,
      title: taskData.title,
      description: taskData.description,
      status: taskData.status || 'pending',
      priority: taskData.priority || 'medium',
      tags: taskData.tags,
      dueDate: taskData.dueDate,
      completed: false,
      completedAt: undefined,
      recurrencePattern: taskData.recurrencePattern,
      userId: user.id,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    } as Task;

    setTasks(prev => [optimisticTask, ...prev]);

    try {
      const newTask = await taskService.createTask(user.id, taskData);
      // Replace the temporary task with the actual one
      setTasks(prev => prev.map(task => task.id === tempId ? newTask : task));
      return newTask;
    } catch (err) {
      // If the API call fails, remove the optimistic task
      setTasks(prev => prev.filter(task => task.id !== tempId));
      console.error('Error creating task:', err);
      setError('Failed to create task. Please try again.');
      throw err;
    }
  };

  const updateTask = async (taskId: string, taskData: UpdateTaskRequest): Promise<Task> => {
    if (!user) throw new Error('User not authenticated');

    // Optimistic update: update the task immediately
    setTasks(prev => prev.map(task =>
      task.id === taskId
        ? { ...task, ...taskData, updatedAt: new Date().toISOString() }
        : task
    ));

    try {
      const updatedTask = await taskService.updateTask(user.id, taskId, taskData);
      // Update with the actual data from the server
      setTasks(prev => prev.map(task => task.id === taskId ? updatedTask : task));
      return updatedTask;
    } catch (err) {
      // If the API call fails, revert the optimistic update
      setError('Failed to update task. Please try again.');
      throw err;
    }
  };

  const deleteTask = async (taskId: string) => {
    if (!user) return;

    // Optimistic update: remove the task immediately
    const taskToDelete = tasks.find(task => task.id === taskId);
    if (!taskToDelete) return;

    setTasks(prev => prev.filter(task => task.id !== taskId));

    try {
      await taskService.deleteTask(user.id, taskId);
    } catch (err) {
      // If the API call fails, restore the task
      setTasks(prev => [taskToDelete, ...prev]);
      console.error('Error deleting task:', err);
      setError('Failed to delete task. Please try again.');
      throw err;
    }
  };

  const toggleTaskCompletion = async (taskId: string, completed: boolean): Promise<Task> => {
    if (!user) throw new Error('User not authenticated');

    // Optimistic update: toggle the completion status immediately
    setTasks(prev => prev.map(task =>
      task.id === taskId
        ? {
            ...task,
            completed,
            completedAt: completed ? new Date().toISOString() : undefined,
            updatedAt: new Date().toISOString()
          }
        : task
    ));

    try {
      const updatedTask = await taskService.toggleTaskComplete(user.id, taskId, completed);
      // Update with the actual data from the server
      setTasks(prev => prev.map(task => task.id === taskId ? updatedTask : task));
      return updatedTask;
    } catch (err) {
      // If the API call fails, revert the optimistic update
      setError('Failed to update task. Please try again.');
      throw err;
    }
  };

  // Fetch tasks when user changes
  useEffect(() => {
    if (user) {
      fetchTasks();
    } else {
      setTasks([]);
    }
  }, [user]);

  const value = {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  };

  return <TaskContext.Provider value={value}>{children}</TaskContext.Provider>;
};

export const useTask = () => {
  const context = useContext(TaskContext);
  if (context === undefined) {
    throw new Error('useTask must be used within a TaskProvider');
  }
  return context;
};