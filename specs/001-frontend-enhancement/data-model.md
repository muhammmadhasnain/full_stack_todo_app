# Data Model: Frontend Enhancement

## Task Entity

### Fields
- `id: number` - Unique identifier for the task
- `title: string` - Task title (required, max 255 characters)
- `description: string | null` - Task description (nullable)
- `status: "pending" | "in-progress" | "completed" | "cancelled" | "on_hold"` - Task status
- `priority: "low" | "medium" | "high"` - Task priority level
- `due_date: Date | null` - Due date for the task (nullable, ISO string from backend)
- `user_id: number` - Associated user ID
- `created_at: Date` - Creation timestamp (ISO string from backend)
- `updated_at: Date` - Last update timestamp (ISO string from backend)
- `completed_at: Date | null` - Completion timestamp (nullable, ISO string from backend)
- `is_recurring: boolean` - Whether the task is recurring
- `recurrence_pattern: RecurrencePattern | null` - Recurrence pattern if applicable

### Validation Rules
- Title is required and must be 1-255 characters
- Status must be one of the allowed values
- Priority must be low, medium, or high
- Due date must be a valid future date if provided
- User ID must match authenticated user

### State Transitions
- `pending` → `in-progress` → `completed` (or `cancelled`)
- `in-progress` → `pending` (if returned to pending)
- `completed` → `pending` (if uncompleted)
- `cancelled` → `pending` (if reopened)

## User Entity

### Fields
- `id: number` - Unique identifier for the user
- `email: string` - User's email address
- `created_at: Date` - Account creation timestamp (ISO string from backend)
- `updated_at: Date` - Last update timestamp (ISO string from backend)
- `is_active: boolean` - Whether the account is active

### Validation Rules
- Email must be valid and unique
- ID must match authenticated user for access

## RecurrencePattern Entity

### Fields
- `id: number` - Unique identifier for the pattern
- `pattern_type: string` - Type of recurrence (daily, weekly, monthly, yearly)
- `interval: number` - Interval between occurrences
- `end_condition_type: string` - How the recurrence ends (count, date, never)
- `end_count: number | null` - Number of occurrences before ending (nullable)
- `end_date: Date | null` - Date to end recurrence (nullable)
- `user_id: number` - Associated user ID

### Validation Rules
- Pattern type must be one of allowed values
- Interval must be positive
- End conditions must be consistent

## Authentication Response

### Fields
- `access_token: string` - JWT access token
- `token_type: string` - Token type (usually "bearer")
- `refresh_token: string` - JWT refresh token
- `user: User` - User profile information

## Task List Response

### Fields
- `tasks: Task[]` - Array of task objects
- `total: number` - Total number of tasks matching filters

## API Response Format

### Success Response
- `data: any` - The returned data
- `status: number` - HTTP status code

### Error Response
- `error: { code: string, message: string, details?: string }` - Error information