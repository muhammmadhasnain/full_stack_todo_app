# Data Model: Backend Todo App API

## Entity: User
**Description**: Represents a registered user with authentication credentials

**Fields**:
- `id` (UUID/Integer): Primary key, unique identifier
- `email` (String): User's email address, unique, required
- `hashed_password` (String): BCrypt hashed password, required
- `created_at` (DateTime): Account creation timestamp, auto-generated
- `updated_at` (DateTime): Last update timestamp, auto-generated
- `is_active` (Boolean): Account status, default: true

**Relationships**:
- One-to-Many: User → Tasks (user.tasks)
- One-to-Many: User → RecurrencePatterns (user.recurrence_patterns)

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Password must meet minimum security requirements (handled by auth service)

## Entity: Task
**Description**: Represents a todo item with all specified attributes

**Fields**:
- `id` (UUID/Integer): Primary key, unique identifier
- `user_id` (UUID/Integer): Foreign key to User, required
- `title` (String, max 255): Task title, required
- `description` (Text, optional): Detailed task description
- `status` (String/Enum): Task status ('pending', 'completed'), default: 'pending'
- `priority` (String/Enum): Task priority ('low', 'medium', 'high'), required
- `due_date` (DateTime, optional): Task deadline
- `created_at` (DateTime): Task creation timestamp, auto-generated
- `updated_at` (DateTime): Last update timestamp, auto-generated
- `completed_at` (DateTime, optional): When task was marked as completed
- `is_recurring` (Boolean): Whether this task has recurrence, default: false

**Relationships**:
- Many-to-One: Task → User (task.user)
- One-to-Many: Task → TaskTags (task.tags)
- Many-to-One: Task → RecurrencePattern (task.recurrence_pattern, optional)

**Validation Rules**:
- Title must not be empty
- Priority must be one of the allowed values ('low', 'medium', 'high')
- User_id must reference an existing, active user
- Due date (if provided) must be in the future

## Entity: TaskTag
**Description**: Represents tags that can be associated with tasks

**Fields**:
- `id` (UUID/Integer): Primary key, unique identifier
- `task_id` (UUID/Integer): Foreign key to Task, required
- `tag_name` (String, max 50): The tag name, required
- `created_at` (DateTime): Tag creation timestamp, auto-generated

**Relationships**:
- Many-to-One: TaskTag → Task (task_tag.task)
- Many-to-One: TaskTag → User (through task, for data isolation)

**Validation Rules**:
- Tag_name must not be empty
- Each task can have up to 10 tags
- Tag names must be unique per task

## Entity: RecurrencePattern
**Description**: Defines how often a task should repeat

**Fields**:
- `id` (UUID/Integer): Primary key, unique identifier
- `user_id` (UUID/Integer): Foreign key to User, required
- `pattern_type` (String/Enum): Type of recurrence ('daily', 'weekly', 'monthly', 'yearly'), required
- `interval` (Integer): Interval multiplier (e.g., every 2 weeks), default: 1
- `end_condition_type` (String/Enum): How recurrence ends ('never', 'after_count', 'on_date'), required
- `end_count` (Integer, optional): Number of occurrences for 'after_count' type
- `end_date` (Date, optional): End date for 'on_date' type
- `created_at` (DateTime): Pattern creation timestamp, auto-generated
- `updated_at` (DateTime): Last update timestamp, auto-generated

**Relationships**:
- Many-to-One: RecurrencePattern → User (recurrence_pattern.user)
- One-to-Many: RecurrencePattern → Tasks (recurrence_pattern.tasks)

**Validation Rules**:
- If end_condition_type is 'after_count', end_count must be provided and > 0
- If end_condition_type is 'on_date', end_date must be provided and in the future
- Pattern_type must be one of the allowed values
- User_id must reference an existing, active user

## State Transitions

### Task Status Transitions
- `pending` → `completed`: When user marks task as complete
- `completed` → `pending`: When user unmarks task as complete

### User Activation Transitions
- `active` → `inactive`: When account is deactivated
- `inactive` → `active`: When account is reactivated

## Database Indexes

1. **User table**:
   - Index on `email` (unique)

2. **Task table**:
   - Index on `user_id` (for user-specific queries)
   - Index on `status` (for filtering)
   - Index on `priority` (for filtering)
   - Index on `due_date` (for date-based queries)
   - Index on `created_at` (for chronological ordering)
   - Composite index on `(user_id, status)` (for user's tasks by status)

3. **TaskTag table**:
   - Index on `task_id` (for task's tags lookup)
   - Index on `tag_name` (for tag-based searches)
   - Composite index on `(task_id, tag_name)` (for unique constraint)

4. **RecurrencePattern table**:
   - Index on `user_id` (for user-specific patterns)