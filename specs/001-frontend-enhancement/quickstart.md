# Quickstart Guide: Frontend Enhancement

## Overview

This guide provides a quick introduction to implementing the missing frontend features that correspond to the backend's existing capabilities. The frontend enhancement project focuses on implementing advanced authentication, task filtering and pagination, task status management, and recurrence patterns.

## Prerequisites

- Node.js 18+ installed
- Next.js 14+ with App Router
- TypeScript 5.3+
- Tailwind CSS
- Better Auth client
- date-fns for date handling

## Setup

1. Install required dependencies:

```bash
npm install date-fns @types/date-fns
```

2. Ensure your API client is updated to handle the new response formats from the backend:

```typescript
// In your API client (e.g., lib/api.ts)
// Make sure it can handle the new task model with status, priority, due_date, etc.
```

## Key Implementation Areas

### 1. Enhanced Authentication System

Implement automatic token refresh and user profile management:

```typescript
// Example token refresh implementation
const refreshToken = async () => {
  try {
    const response = await apiClient.post('/auth/refresh');
    const { access_token, refresh_token, user } = response.data.data;

    // Update tokens in storage
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);

    return { access_token, refresh_token, user };
  } catch (error) {
    // Handle refresh failure - redirect to login
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login';
    throw error;
  }
};
```

### 2. Advanced Task Filtering and Pagination

Update your task list component to support filtering and pagination:

```typescript
// Example filtering and pagination parameters
interface TaskFilterParams {
  status?: 'pending' | 'in-progress' | 'completed' | 'cancelled' | 'on_hold';
  priority?: 'low' | 'medium' | 'high';
  dueDateFrom?: string; // ISO date string
  dueDateTo?: string;   // ISO date string
  skip?: number;
  limit?: number;
}

const fetchTasks = async (filters: TaskFilterParams = {}) => {
  const params = new URLSearchParams();

  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined) {
      params.append(key, String(value));
    }
  });

  const response = await apiClient.get(`/tasks?${params.toString()}`);
  return response.data.data;
};
```

### 3. Task Status Management

Update your task components to handle the full range of statuses:

```typescript
// Task status options
const taskStatusOptions = [
  { value: 'pending', label: 'Pending' },
  { value: 'in-progress', label: 'In Progress' },
  { value: 'completed', label: 'Completed' },
  { value: 'cancelled', label: 'Cancelled' },
  { value: 'on_hold', label: 'On Hold' }
];

const taskPriorityOptions = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' }
];
```

### 4. Recurrence Pattern Support

Implement recurrence pattern handling in your task forms:

```typescript
// Example recurrence pattern structure
interface RecurrencePattern {
  pattern_type: 'daily' | 'weekly' | 'monthly' | 'yearly';
  interval: number;
  end_condition_type: 'count' | 'date' | 'never';
  end_count?: number;
  end_date?: string; // ISO date string
}
```

## API Integration

Use the API contracts defined in the `contracts/` directory to ensure compatibility with the backend:

- Refer to `task-api-contracts.yaml` for task management endpoints
- Refer to `auth-api-contracts.yaml` for authentication endpoints
- Implement proper error handling based on the defined error response format

## Testing

1. Verify token refresh works by waiting for token expiration
2. Test advanced filtering with various combinations
3. Confirm all task statuses are properly handled
4. Validate recurrence pattern creation and display
5. Ensure proper error handling throughout the application

## Next Steps

After implementing the core features:

1. Add loading indicators for all async operations
2. Implement proper error boundaries and user feedback
3. Add accessibility features (ARIA attributes, keyboard navigation)
4. Optimize performance for large task lists
5. Add data import/export capabilities