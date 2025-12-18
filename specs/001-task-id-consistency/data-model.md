# Data Model: Task ID Type Consistency

## Entities

### Task
- **id**: UUID (primary key) - Unique identifier for the task
- **title**: string - Title of the task
- **description**: string (optional) - Detailed description of the task
- **completed**: boolean - Completion status of the task
- **user_id**: UUID (foreign key) - Reference to the user who owns the task
- **created_at**: datetime - Timestamp when task was created
- **updated_at**: datetime - Timestamp when task was last updated

**Validation rules**:
- id: Must be a valid UUID format
- title: Required, max length 255 characters
- user_id: Must reference an existing user UUID

**Relationships**:
- Many tasks belong to one user (user_id → User.id)

### User
- **id**: UUID (primary key) - Unique identifier for the user
- **email**: string - User's email address
- **name**: string - User's display name
- **created_at**: datetime - Timestamp when user was created
- **updated_at**: datetime - Timestamp when user was last updated

**Validation rules**:
- id: Must be a valid UUID format
- email: Required, valid email format, unique

## State Transitions

### Task State Transitions
- **Creation**: New task with completed=False
- **Update**: Task properties can be modified (title, description)
- **Completion Toggle**: completed status can be toggled (False ↔ True)
- **Deletion**: Task is removed from system

## Database Schema Changes

### Task Table Migration
- Change primary key from integer `id` to UUID `id`
- Change foreign key from integer `user_id` to UUID `user_id`
- Maintain all other columns and constraints
- Update indexes to work with UUID columns