# API Contracts

This directory contains the API contract definitions for the frontend enhancement project, based on the backend capabilities.

## Contract Files

1. **task-api-contracts.yaml** - Defines the API contracts for task management operations including:
   - Advanced filtering and pagination
   - Full task CRUD operations with status, priority, due dates, and recurrence patterns
   - Task completion toggling
   - Proper error handling and response formats

2. **auth-api-contracts.yaml** - Defines the API contracts for authentication operations including:
   - User registration and login
   - Token refresh functionality
   - User profile management
   - Logout functionality

## Purpose

These contracts serve as the interface specification between the frontend and backend, ensuring consistency in:
- Request/response formats
- Data structures
- Error handling
- Authentication flows
- API endpoint paths and parameters

## Usage

Frontend developers should implement against these contracts to ensure compatibility with the backend API. The contracts follow OpenAPI 3.0 specification and can be used with various API client generation tools.