---
name: backend-development
description: Implement all backend features for the full-stack todo app using FastAPI, SQLModel, Neon Serverless PostgreSQL, and JWT authentication. Use this Skill when building API endpoints, database models, or handling authentication and security.


---

# Backend Development Skill

## Overview
This Skill governs all backend development for the full-stack todo app. It includes Python FastAPI development, SQLModel ORM, Neon Serverless PostgreSQL, JWT-based authentication with Better Auth, and strict compliance with the project constitution.

---

## Core Capabilities

### 1. FastAPI Development
- Create REST API endpoints following the specified patterns:
  - GET /api/{user_id}/tasks: List all tasks for user
  - POST /api/{user_id}/tasks: Create a new task
  - GET /api/{user_id}/tasks/{id}: Get task details
  - PUT /api/{user_id}/tasks/{id}: Update a task
  - DELETE /api/{user_id}/tasks/{id}: Delete a task
  - PATCH /api/{user_id}/tasks/{id}/complete: Toggle completion status
- Implement proper HTTP status codes for all responses
- Handle request validation and response serialization with Pydantic
- Create API documentation with automatic OpenAPI generation
- Implement proper error handling and custom exception responses

### 2. Database-First Design with SQLModel
- Define all data models using SQLModel with proper constraints
- Implement database relationships and foreign key constraints
- Create proper indexes for optimized queries
- Follow database-first design principles as specified in the constitution
- Ensure backward compatibility for schema changes
- Implement proper migration strategies

### 3. JWT-Based Authentication Security
- Implement JWT token verification for all API endpoints
- Ensure user data isolation - each user can only access their own data
- Implement proper token validation at the API gateway level
- Create authentication middleware to protect endpoints
- Handle token expiration and refresh mechanisms

### 4. Type Safety and Validation
- Use strict type validation via Pydantic for all API requests and responses
- Validate database models through SQLModel with proper constraints
- Ensure type-safe client-server communication
- Implement proper request/response schemas

### 5. Neon Serverless PostgreSQL Integration
- Configure proper connection pooling for database connections
- Implement efficient database queries with proper indexing
- Handle database transactions appropriately
- Follow best practices for Neon Serverless PostgreSQL usage
- Ensure database schema changes are properly managed

## Technology Stack
- Python FastAPI framework
- SQLModel ORM for database models
- Pydantic for request/response validation
- Neon Serverless PostgreSQL for database
- JWT tokens for authentication
- Better Auth integration

## Development Standards

### API Contract Standards
- Follow consistent REST API patterns as specified in the constitution
- All endpoints must require JWT authentication
- Enforce user data isolation at the API level
- Return proper HTTP status codes for all responses
- Implement proper error taxonomy with appropriate status codes

### Security
- Implement authentication at the API gateway level
- Ensure proper token validation for all requests
- Validate user permissions to access specific data
- Follow JWT best practices for token management
- Protect against common security vulnerabilities

### Type Safety
- Use Pydantic models for all request/response validation
- Implement strict type checking throughout the backend
- Ensure database models match API contracts
- Validate all inputs before database operations

## Implementation Guidelines

### API Endpoint Structure
- Organize endpoints in logical modules
- Implement proper path parameter validation
- Create reusable dependency injection patterns
- Follow consistent naming conventions for endpoints
- Document all endpoints with proper examples

### Database Model Design
- Define all models using SQLModel with proper relationships
- Implement proper validation constraints
- Create appropriate indexes for performance
- Follow database-first design approach
- Ensure models align with API contracts

### Authentication Implementation
- Create authentication middleware for protected endpoints
- Implement user data isolation at the database query level
- Ensure JWT tokens are properly validated
- Handle authentication errors appropriately
- Implement proper session management

## Quality Assurance
- All API endpoints must implement JWT authentication
- Proper user data isolation must be enforced
- Type safety must be maintained throughout the codebase
- Database models must follow SQLModel best practices
- API contracts must align with frontend requirements
- Error handling must be comprehensive and consistent