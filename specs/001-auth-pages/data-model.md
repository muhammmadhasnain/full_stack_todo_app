# Data Model: Authentication Pages

## User Entity

### Core Attributes
- **id** (string/UUID): Unique identifier for the user
- **name** (string): User's display name (required, 2-50 chars)
- **email** (string): User's email address (required, unique, valid format)
- **password** (string): Hashed password (required, meets complexity requirements)
- **createdAt** (datetime): Account creation timestamp
- **updatedAt** (datetime): Last update timestamp
- **emailVerified** (boolean): Whether email has been verified
- **isActive** (boolean): Whether account is active

### Validation Rules
- Email: Must be unique and valid email format
- Password: Minimum 8 characters with uppercase, lowercase, number, and special character
- Name: 2-50 characters, no special characters except spaces
- All required fields must be present during registration

### State Transitions
- Unregistered → Registered (upon successful account creation)
- Registered → Email Verified (upon email verification)
- Active → Inactive (upon account deactivation)

## Session Entity

### Core Attributes
- **id** (string/UUID): Unique session identifier
- **userId** (string): Reference to user who owns the session
- **token** (string): JWT token value
- **expiresAt** (datetime): Token expiration time
- **createdAt** (datetime): Session creation timestamp
- **lastAccessed** (datetime): Last time session was used
- **userAgent** (string): Browser/device information
- **ipAddress** (string): IP address of session origin

### Validation Rules
- Token must be valid JWT format
- Session must not be expired
- IP address must be valid format
- User must be active to create session

### State Transitions
- Created → Active (when user logs in)
- Active → Expired (when token expires)
- Active → Revoked (when user logs out)

## Authentication Response Models

### Registration Response
- **success** (boolean): Whether registration was successful
- **user** (object): User object with public information (id, email, name)
- **token** (string): JWT authentication token
- **message** (string): Success message

### Login Response
- **success** (boolean): Whether login was successful
- **user** (object): User object with public information
- **token** (string): JWT authentication token
- **message** (string): Result message
- **redirectUrl** (string): URL to redirect after successful authentication

### Error Response
- **success** (boolean): Always false for error responses
- **error** (string): Error code (e.g., "INVALID_CREDENTIALS", "VALIDATION_ERROR")
- **message** (string): Human-readable error message
- **details** (object): Field-specific validation errors (when applicable)

## Form Data Models

### Registration Form Data
- **name** (string): User's display name (2-50 chars)
- **email** (string): Valid email address
- **password** (string): Password meeting complexity requirements
- **confirmPassword** (string): Must match password field

### Login Form Data
- **email** (string): Valid email address
- **password** (string): User's password

### Validation Schema
- All fields required
- Email format validation using standard regex
- Password complexity validation (8+ chars, upper, lower, number, special)
- Password confirmation match validation