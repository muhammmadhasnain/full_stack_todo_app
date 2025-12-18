# API Contracts: Authentication Pages

## Authentication API Endpoints

### User Registration
**Endpoint**: `POST /api/auth/register`

**Request**:
```json
{
  "name": "string (2-50 chars)",
  "email": "string (valid email format)",
  "password": "string (8+ chars with upper, lower, number, special)"
}
```

**Successful Response (200)**:
```json
{
  "success": true,
  "user": {
    "id": "string (UUID)",
    "email": "string",
    "name": "string"
  },
  "token": "string (JWT)",
  "message": "string"
}
```

**Error Response (400)**:
```json
{
  "success": false,
  "error": "string (error code)",
  "message": "string (user-friendly message)",
  "details": {
    "field": "string (specific validation errors)"
  }
}
```

### User Login
**Endpoint**: `POST /api/auth/login`

**Request**:
```json
{
  "email": "string (valid email format)",
  "password": "string"
}
```

**Successful Response (200)**:
```json
{
  "success": true,
  "user": {
    "id": "string (UUID)",
    "email": "string",
    "name": "string"
  },
  "token": "string (JWT)",
  "message": "string",
  "redirectUrl": "string (URL to redirect after login)"
}
```

**Error Response (401)**:
```json
{
  "success": false,
  "error": "INVALID_CREDENTIALS",
  "message": "Invalid email or password"
}
```

### Get Current User
**Endpoint**: `GET /api/auth/me`

**Headers**:
```
Authorization: Bearer {token}
```

**Successful Response (200)**:
```json
{
  "id": "string (UUID)",
  "email": "string",
  "name": "string",
  "createdAt": "string (ISO date)",
  "lastLoginAt": "string (ISO date)"
}
```

**Error Response (401)**:
```json
{
  "success": false,
  "error": "UNAUTHORIZED",
  "message": "Authentication token required or invalid"
}
```

### Password Reset Request
**Endpoint**: `POST /api/auth/forgot-password`

**Request**:
```json
{
  "email": "string (valid email format)"
}
```

**Successful Response (200)**:
```json
{
  "success": true,
  "message": "Password reset email sent if account exists"
}
```

### Password Reset
**Endpoint**: `POST /api/auth/reset-password`

**Request**:
```json
{
  "token": "string (password reset token)",
  "newPassword": "string (8+ chars with upper, lower, number, special)"
}
```

**Successful Response (200)**:
```json
{
  "success": true,
  "message": "Password updated successfully"
}
```

## Validation Rules

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one number (0-9)
- At least one special character (@$!%*?&)
- No maximum length limit (within reasonable bounds)

### Email Requirements
- Valid email format (user@domain.tld)
- Maximum 254 characters
- Unique across all users

### Name Requirements
- 2-50 characters
- Alphanumeric with spaces allowed
- No special characters except spaces

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Request data failed validation |
| INVALID_CREDENTIALS | 401 | Login credentials are incorrect |
| EMAIL_EXISTS | 409 | Email already registered |
| UNAUTHORIZED | 401 | Missing or invalid authentication |
| TOKEN_EXPIRED | 401 | Authentication token has expired |
| USER_NOT_FOUND | 404 | Requested user does not exist |
| RATE_LIMITED | 429 | Too many requests from this IP |

## Authentication Headers

All protected endpoints require the following header:
```
Authorization: Bearer {JWT_TOKEN}
```

## Session Management

- JWT tokens expire after 24 hours of inactivity
- Tokens are refreshed automatically during active use
- Sessions are invalidated on logout
- Concurrent sessions are allowed