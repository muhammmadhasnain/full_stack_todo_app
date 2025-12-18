// frontend/tests/unit/task-item.test.tsx

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import TaskItem from '@/components/TaskItem';
import { Task } from '@/types/task';
import { TaskProvider } from '@/contexts/task';
import { AuthProvider } from '@/contexts/auth';

// Mock the useTask and useAuth hooks
jest.mock('@/contexts/task', () => ({
  ...jest.requireActual('@/contexts/task'),
  useTask: () => ({
    updateTask: jest.fn(),
    deleteTask: jest.fn(),
    toggleTaskCompletion: jest.fn(),
  }),
}));

jest.mock('@/contexts/auth', () => ({
  ...jest.requireActual('@/contexts/auth'),
  useAuth: () => ({
    user: { id: 'test-user-id', name: 'Test User' },
    isAuthenticated: true,
  }),
}));

const mockTask: Task = {
  id: '1',
  title: 'Test Task',
  description: 'Test Description',
  priority: 'medium',
  tags: 'test,example',
  dueDate: new Date('2023-12-31').toISOString(),
  completed: false,
  completedAt: null,
  recurrencePattern: 'none',
  userId: 'test-user-id',
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
};

const renderWithProviders = (component: React.ReactNode) => {
  return render(
    <AuthProvider>
      <TaskProvider>
        {component}
      </TaskProvider>
    </AuthProvider>
  );
};

describe('TaskItem Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders task title and description', () => {
    renderWithProviders(<TaskItem task={mockTask} />);

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
  });

  test('displays priority with correct styling', () => {
    renderWithProviders(<TaskItem task={mockTask} />);

    const priorityElement = screen.getByText('medium');
    expect(priorityElement).toBeInTheDocument();
  });

  test('toggles completion status when checkbox is clicked', async () => {
    const { useTask } = require('@/contexts/task');
    const mockToggleCompletion = jest.fn();
    useTask.mockReturnValue({
      updateTask: jest.fn(),
      deleteTask: jest.fn(),
      toggleTaskCompletion: mockToggleCompletion,
    });

    renderWithProviders(<TaskItem task={{ ...mockTask, completed: false }} />);

    const checkbox = screen.getByRole('checkbox');
    fireEvent.click(checkbox);

    await waitFor(() => {
      expect(mockToggleCompletion).toHaveBeenCalledWith(mockTask.id, true);
    });
  });

  test('enters edit mode when edit button is clicked', () => {
    renderWithProviders(<TaskItem task={mockTask} />);

    const editButton = screen.getByLabelText('Edit task');
    fireEvent.click(editButton);

    // Check if input fields appear (in edit mode)
    const titleInput = screen.getByDisplayValue('Test Task');
    expect(titleInput).toBeInTheDocument();
  });

  test('shows confirmation dialog when delete button is clicked', () => {
    // Mock window.confirm
    window.confirm = jest.fn(() => true);

    const { useTask } = require('@/contexts/task');
    const mockDeleteTask = jest.fn();
    useTask.mockReturnValue({
      updateTask: jest.fn(),
      deleteTask: mockDeleteTask,
      toggleTaskCompletion: jest.fn(),
    });

    renderWithProviders(<TaskItem task={mockTask} />);

    const deleteButton = screen.getByLabelText('Delete task');
    fireEvent.click(deleteButton);

    expect(window.confirm).toHaveBeenCalledWith('Are you sure you want to delete this task?');
    expect(mockDeleteTask).toHaveBeenCalledWith(mockTask.id);
  });

  test('displays recurrence pattern if available', () => {
    const taskWithRecurrence = { ...mockTask, recurrencePattern: 'daily' };
    renderWithProviders(<TaskItem task={taskWithRecurrence} />);

    expect(screen.getByText('daily')).toBeInTheDocument();
  });

  test('displays due date if available', () => {
    renderWithProviders(<TaskItem task={mockTask} />);

    expect(screen.getByText(/Due:/)).toBeInTheDocument();
  });

  test('displays tags if available', () => {
    renderWithProviders(<TaskItem task={mockTask} />);

    expect(screen.getByText('test,example')).toBeInTheDocument();
  });
});