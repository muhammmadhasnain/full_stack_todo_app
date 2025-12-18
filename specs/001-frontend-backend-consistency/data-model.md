# Data Model: Frontend-Backend Consistency

## Overview
This document defines the unified data models that will ensure consistency between frontend and backend systems after implementing the required changes.

## Entity: Task
**Description**: Represents a user task with consistent fields across frontend and backend

### Fields
- `id`: UUID string (primary identifier, globally unique)
- `title`: string (required, task title)
- `description`: string (optional, task description)
- `status`: string enum ('pending' | 'in-progress' | 'completed' | 'cancelled' | 'on_hold')
- `priority`: string enum ('low' | 'medium' | 'high')
- `due_date`: datetime (optional, ISO 8601 format)
- `tags`: string (optional, comma-separated tags)
- `is_recurring`: boolean (indicates if task is recurring)
- `recurrence_pattern`: object (optional, recurrence configuration)
- `user_id`: UUID string (foreign key to User)
- `created_at`: datetime (ISO 8601 format, creation timestamp)
- `updated_at`: datetime (ISO 8601 format, last update timestamp)
- `completed_at`: datetime (optional, ISO 8601 format, completion timestamp)

### Validation Rules
- `title` must be 1-255 characters
- `status` must be one of the defined enum values
- `priority` must be one of the defined enum values
- `due_date` must be a valid datetime if provided
- `user_id` must reference an existing user
- `created_at` is set on creation and never modified
- `updated_at` is updated on every modification

### State Transitions
- Status can transition from 'pending' → 'in-progress' → 'completed' or 'cancelled'
- Status can transition from 'in-progress' → 'pending' or 'completed' or 'cancelled'
- Status can transition from 'completed' → 'pending' (to re-open)
- `completed_at` is set when status becomes 'completed', cleared when status changes from 'completed'

## Entity: User
**Description**: Represents a system user with consistent fields across frontend and backend

### Fields
- `id`: UUID string (primary identifier, globally unique)
- `name`: string (user's display name)
- `email`: string (user's email address, unique)
- `created_at`: datetime (ISO 8601 format, creation timestamp)
- `updated_at`: datetime (ISO 8601 format, last update timestamp)
- `is_active`: boolean (indicates if user account is active)

### Validation Rules
- `email` must be a valid email format and unique
- `name` must be 1-100 characters
- `email` and `name` are required fields
- `is_active` defaults to true

## Entity: API Response
**Description**: Standardized structure for API responses to ensure consistency

### Fields
- `access_token`: string (JWT access token)
- `token_type`: string (token type, typically "bearer")
- `refresh_token`: string (JWT refresh token)
- `user`: User object (user profile information)

### Task List Response
- `tasks`: array of Task objects
- `total`: number (total count of tasks matching filters)

## Relationship: Task - User
- One User can have many Tasks (one-to-many)
- Task.user_id references User.id
- Cascade delete: deleting a User removes all their Tasks
- Foreign key constraint ensures referential integrity