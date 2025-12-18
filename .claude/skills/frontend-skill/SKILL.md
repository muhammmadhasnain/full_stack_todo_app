---
name: frontend-development
description: Implement all frontend features for the full-stack todo app using Next.js 16+, App Router, TypeScript, Tailwind CSS, and Better Auth. Use this Skill when building UI, integrating APIs, or handling authentication.
---

# Frontend Development Skill

## Overview
This Skill governs all frontend development for the full-stack todo app. It includes Next.js 16+ App Router, TypeScript type safety, Tailwind CSS styling, authentication with Better Auth, and strict compliance with the project constitution.

---

## Core Capabilities

### 1. Next.js 16+ with App Router
- Create and manage pages using Next.js 16 App Router
- Implement client and server components appropriately
- Handle route parameters and dynamic routing
- Implement loading states and error boundaries
- Follow best practices for component organization and data fetching

### 2. Responsive UI/UX Implementation
- Create responsive designs that work across mobile, tablet, and desktop
- Implement proper loading states for all user interactions
- Provide appropriate error handling and user feedback
- Follow WCAG accessibility standards for all UI components
- Use Tailwind CSS for consistent styling

### 3. Authentication Integration
- Implement Better Auth for user authentication
- Create protected routes that require authentication
- Handle JWT token management
- Implement login, signup, and logout flows
- Ensure proper session management

### 4. API Integration
- Connect to backend REST API endpoints following the specified patterns:
  - GET /api/{user_id}/tasks: List all tasks for user
  - POST /api/{user_id}/tasks: Create a new task
  - GET /api/{user_id}/tasks/{id}: Get task details
  - PUT /api/{user_id}/tasks/{id}: Update a task
  - DELETE /api/{user_id}/tasks/{id}: Delete a task
  - PATCH /api/{user_id}/tasks/{id}/complete: Toggle completion status
- Implement proper type safety with TypeScript interfaces
- Handle API errors gracefully
- Implement proper loading and error states

### 5. State Management
- Manage application state using React hooks and context
- Implement proper data flow between components
- Handle form state and validation
- Manage user session state

## Technology Stack
- Next.js 16+ with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- Better Auth for authentication
- Responsive design principles

## Development Standards

### Type Safety
- All API requests and responses must use strict type validation
- Define TypeScript interfaces for all data structures
- Ensure client-server communication is type-safe
- Validate all props and parameters

### UI/UX Standards
- Follow responsive UI/UX standards from the constitution
- Provide appropriate loading states for all user interactions
- Implement proper error handling and user feedback
- Ensure accessibility compliance (WCAG standards)

### Security
- Ensure authentication is properly implemented at the UI level
- Protect sensitive user data in the frontend
- Validate user inputs before sending to backend
- Handle authentication tokens securely

## Implementation Guidelines

### Component Structure
- Organize components in a logical folder structure
- Create reusable UI components
- Separate presentational and container components
- Implement proper component composition

### API Integration
- Create a centralized API client for backend communication
- Implement proper error handling for API calls
- Use appropriate HTTP methods as specified in the constitution
- Ensure all endpoints require proper authentication

### Testing Considerations
- Write unit tests for components
- Implement integration tests for API interactions
- Test responsive behavior across different screen sizes
- Verify authentication flows work correctly

## Quality Assurance
- All UI must be responsive across mobile, tablet, and desktop
- Proper loading states must be implemented for all async operations
- Error handling must be comprehensive and user-friendly
- Accessibility standards must be followed
- Type safety must be maintained throughout the codebase