// frontend/tests/integration/api.test.ts

import { taskService } from '@/lib/api';
import { Task, CreateTaskRequest, UpdateTaskRequest } from '@/types/task';

// Mock the fetch API
global.fetch = jest.fn();

describe('API Integration Tests', () => {
  beforeEach(() => {
    (global.fetch as jest.Mock).mockClear();
  });

  describe('Task API', () => {
    const mockUserId = '123e4567-e89b-12d3-a456-426614174000';
    const mockTask: Task = {
      id: '123e4567-e89b-12d3-a456-426614174001',
      title: 'Test Task',
      description: 'Test Description',
      priority: 'medium',
      completed: false,
      userId: mockUserId,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    test('should fetch tasks', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => [mockTask],
      });

      const tasks = await taskService.getTasks(mockUserId);

      expect(tasks).toHaveLength(1);
      expect(tasks[0].title).toBe('Test Task');
      expect(global.fetch).toHaveBeenCalledWith(
        `http://localhost:8000/api/${mockUserId}/tasks`,
        expect.objectContaining({
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
          }),
        })
      );
    });

    test('should create a task', async () => {
      const newTaskData: CreateTaskRequest = {
        title: 'New Task',
        description: 'New Description',
        priority: 'high',
      };

      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockTask,
      });

      const createdTask = await taskService.createTask(mockUserId, newTaskData);

      expect(createdTask.title).toBe('Test Task');
      expect(global.fetch).toHaveBeenCalledWith(
        `http://localhost:8000/api/${mockUserId}/tasks`,
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(newTaskData),
        })
      );
    });

    test('should update a task', async () => {
      const updateData: UpdateTaskRequest = {
        title: 'Updated Task',
        priority: 'low',
      };

      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ ...mockTask, ...updateData }),
      });

      const updatedTask = await taskService.updateTask(mockUserId, mockTask.id, updateData);

      expect(updatedTask.title).toBe('Updated Task');
      expect(global.fetch).toHaveBeenCalledWith(
        `http://localhost:8000/api/${mockUserId}/tasks/${mockTask.id}`,
        expect.objectContaining({
          method: 'PUT',
          body: JSON.stringify(updateData),
        })
      );
    });

    test('should delete a task', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        status: 204,
      });

      await taskService.deleteTask(mockUserId, mockTask.id);

      expect(global.fetch).toHaveBeenCalledWith(
        `http://localhost:8000/api/${mockUserId}/tasks/${mockTask.id}`,
        expect.objectContaining({
          method: 'DELETE',
        })
      );
    });

    test('should toggle task completion', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ ...mockTask, completed: true }),
      });

      const toggledTask = await taskService.toggleTaskComplete(mockUserId, mockTask.id, true);

      expect(toggledTask.completed).toBe(true);
      expect(global.fetch).toHaveBeenCalledWith(
        `http://localhost:8000/api/${mockUserId}/tasks/${mockTask.id}/complete`,
        expect.objectContaining({
          method: 'PATCH',
          body: JSON.stringify({ completed: true }),
        })
      );
    });
  });
});