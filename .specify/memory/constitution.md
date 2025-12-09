<!--
Sync Impact Report:
- Version change: N/A → 1.0.0 (initial constitution)
- Added sections: All principles and governance sections
- Templates requiring updates: N/A (initial creation)
- Follow-up TODOs: None
-->
# Todo App Full-Stack Constitution

## Core Principles

### I. Full-Stack Monorepo Architecture
Codebase follows a monorepo structure with clear separation between frontend and backend. Frontend (Next.js 16+) and backend (FastAPI) must maintain independent deployability while sharing common specifications. All code changes must consider both frontend and backend impacts.

### II. Spec-Driven Development (NON-NEGOTIABLE)
All features must be specified in the specs/ directory before implementation begins. Specifications must include API contracts, database schemas, and UI requirements. Code that doesn't align with specifications requires spec updates first.

### III. JWT-Based Authentication Security
All API endpoints must implement JWT token verification using Better Auth. User data isolation is mandatory - each user can only access their own data. Authentication must be implemented at the API gateway level with proper token validation.

### IV. Type Safety and Validation
All API requests and responses must use strict type validation via Pydantic (backend) and TypeScript (frontend). Database models must be validated through SQLModel with proper constraints. Client-server communication must be type-safe.

### V. Responsive UI/UX Standards
Frontend must be responsive across mobile, tablet, and desktop. All user interactions must provide appropriate loading states and error handling. Accessibility standards (WCAG) must be followed for all UI components.

### VI. Database-First Design
All data models must be defined in SQLModel first, with migrations properly handled. Database schema changes must be backward compatible and include migration strategies. Neon Serverless PostgreSQL must be the single source of truth for all persistent data.

## Technology Stack Requirements

The project must adhere to the specified technology stack:
- Frontend: Next.js 16+ with App Router, TypeScript, Tailwind CSS
- Backend: Python FastAPI, SQLModel ORM, Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT tokens
- Spec-Driven: Claude Code + Spec-Kit Plus
- Database: Neon Serverless PostgreSQL with proper connection pooling

All dependencies must be documented in package.json (frontend) and requirements.txt (backend) with specific version constraints to ensure reproducible builds.

## API Contract Standards

REST API endpoints must follow consistent patterns as specified in the API documentation:
- GET /api/{user_id}/tasks: List all tasks for user
- POST /api/{user_id}/tasks: Create a new task
- GET /api/{user_id}/tasks/{id}: Get task details
- PUT /api/{user_id}/tasks/{id}: Update a task
- DELETE /api/{user_id}/tasks/{id}: Delete a task
- PATCH /api/{user_id}/tasks/{id}/complete: Toggle completion status

All endpoints must require JWT authentication and enforce user data isolation. Proper HTTP status codes must be returned for all responses.

## Development Workflow

Code changes must follow the spec-driven workflow:
1. Update specifications in specs/ directory if requirements change
2. Implement backend API endpoints first
3. Update database models as needed
4. Implement frontend components and pages
5. Test authentication and authorization flows
6. Verify responsive design across devices

All pull requests must include unit tests, integration tests, and specification alignment verification. Frontend and backend changes must be tested together in the integrated environment.

## Governance

This constitution supersedes all other development practices and guidelines. Amendments require documentation of the change, approval from project maintainers, and a migration plan for existing code. All code reviews must verify compliance with these principles. New features must follow the spec-driven approach outlined in the project documentation.

**Version**: 1.0.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09