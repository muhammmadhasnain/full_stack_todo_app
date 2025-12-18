# Authentication Pages Feature

This feature implements user authentication functionality for the Todo app, including login and registration pages.

## Components

### Core Components
- `LoginForm.tsx` - Handles user login with email and password
- `RegisterForm.tsx` - Handles user registration with name, email, and password
- `AuthFormWrapper.tsx` - Provides consistent layout and navigation between auth pages

### UI Components
- `Input.tsx` - Custom input component with password toggle functionality
- `Button.tsx` - Custom button component with loading state
- `FormError.tsx` - Displays form validation and error messages

### Utilities
- `validation.ts` - Contains validation functions for forms
- `auth.ts` - Contains auth-related utility functions

## Features Implemented

### User Story 1 - Create Account (Priority: P1)
- Registration form with name, email, and password fields
- Password complexity validation (8+ chars, uppercase, lowercase, number, special char)
- Password confirmation field
- Form validation and error handling
- Loading indicators during submission
- Password masking with toggle visibility
- Redirect to home page after successful registration

### User Story 2 - Sign In to Account (Priority: P1)
- Login form with email and password fields
- Form validation and error handling
- Loading indicators during submission
- Password masking with toggle visibility
- Redirect to home page after successful login

### User Story 3 - Navigate Between Auth Pages (Priority: P2)
- Clear navigation links between login and registration pages
- Consistent form wrapper component
- Responsive design for all screen sizes

## Validation Rules

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character (@$!%*?&)

### Email Validation
- Standard email format validation
- Required field validation

### Name Validation
- Minimum 2 characters
- Required field validation

## Security Features
- Password fields are masked by default
- Password visibility toggle for user convenience
- Form validation to prevent empty submissions
- Integration with existing authentication context

## Responsive Design
- Mobile-first approach using Tailwind CSS
- Responsive layout that works on all screen sizes
- Accessible form elements with proper labeling

## Integration
- Uses existing `AuthProvider` and `useAuth` hook
- Integrates with existing API service via `taskService`
- Consistent with existing app styling and design system