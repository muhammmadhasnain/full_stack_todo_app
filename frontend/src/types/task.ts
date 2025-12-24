// Task interface for frontend
export interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'in-progress' | 'completed' | 'cancelled' | 'on_hold';
  priority: 'low' | 'medium' | 'high';
  tags?: string;  // Comma-separated string
  dueDate?: string; // ISO date string
  completed: boolean;
  completedAt?: string; // ISO date string
  recurrencePattern?: RecurrencePattern;
  userId: string;
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
}

export interface RecurrencePattern {
  type: 'daily' | 'weekly' | 'monthly' | 'yearly';
  interval: number;
  end_date?: string; // ISO date string
  occurrences?: number;
  days_of_week?: number[]; // 0-6 where 0 is Sunday
  days_of_month?: number[]; // 1-31
}

// API Request/Response types
export interface CreateTaskRequest {
  title: string;
  description?: string;
  status?: 'pending' | 'in-progress' | 'completed' | 'cancelled' | 'on_hold';
  priority?: 'low' | 'medium' | 'high';
  tags?: string;
  dueDate?: string;
  recurrencePattern?: RecurrencePattern;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  status?: 'pending' | 'in-progress' | 'completed' | 'cancelled' | 'on_hold';
  priority?: 'low' | 'medium' | 'high';
  tags?: string;
  dueDate?: string;
  recurrencePattern?: RecurrencePattern;
}

export interface TaskFilter {
  status?: 'pending' | 'in-progress' | 'completed' | 'cancelled' | 'on_hold';
  priority?: 'low' | 'medium' | 'high';
  tags?: string;
  has_recurrence?: boolean;
  due_date_start?: string;
  due_date_end?: string;
  completed?: boolean;
  search?: string;
  skip?: number;
  limit?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface ToggleCompleteRequest {
  completed: boolean;
}

export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: string;
  };
}

// User interface
export interface User {
  id: string;
  email: string;
  name: string;  // Make name required
  createdAt: string;
  updatedAt: string;
  is_active?: boolean;
}

// API Response types
export interface TaskResponse extends Task {}
export interface UserResponse extends User {}
export interface TokenResponse {
  access_token: string;
  token_type: string;
  refresh_token: string;
  user: User;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface RefreshTokenResponse {
  access_token: string;
  token_type: string;
}