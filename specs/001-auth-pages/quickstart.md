# Quickstart Guide: Authentication Pages

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- Next.js 16+ environment
- Better Auth configured in the project
- PostgreSQL database (Neon Serverless)

## Setup Authentication Pages

### 1. Install Dependencies

```bash
npm install next react react-dom typescript @types/react @types/node
npm install better-auth
# For form validation
npm install zod react-hook-form
# For styling
npm install tailwindcss postcss autoprefixer
```

### 2. Create Authentication Pages

Create the following files in your Next.js app directory:

**app/login/page.tsx:**
```tsx
import LoginForm from '@/components/auth/LoginForm';

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
        </div>
        <LoginForm />
      </div>
    </div>
  );
}
```

**app/register/page.tsx:**
```tsx
import RegisterForm from '@/components/auth/RegisterForm';

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create a new account
          </h2>
        </div>
        <RegisterForm />
      </div>
    </div>
  );
}
```

### 3. Create Authentication Components

**components/auth/LoginForm.tsx:**
```tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { authenticateUser } from '@/lib/auth';

// Define validation schema
const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(1, 'Password is required'),
});

type LoginFormInputs = z.infer<typeof loginSchema>;

export default function LoginForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormInputs>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormInputs) => {
    setLoading(true);
    setError('');

    try {
      const result = await authenticateUser(data.email, data.password);

      if (result.success) {
        // Redirect to home page after successful login
        router.push('/');
        router.refresh();
      } else {
        // Show generic error message to prevent user enumeration
        setError('Invalid email or password');
      }
    } catch (err) {
      setError('An error occurred during authentication');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}

      <div className="rounded-md shadow-sm -space-y-px">
        <div>
          <input
            id="email"
            type="email"
            className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
              errors.email ? 'border-red-300' : 'border-gray-300'
            } placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
            placeholder="Email address"
            {...register('email')}
          />
          {errors.email && (
            <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
          )}
        </div>
        <div>
          <input
            id="password"
            type="password"
            className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
              errors.password ? 'border-red-300' : 'border-gray-300'
            } placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
            placeholder="Password"
            {...register('password')}
          />
          {errors.password && (
            <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
          )}
        </div>
      </div>

      <div>
        <button
          type="submit"
          disabled={loading}
          className={`group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white ${
            loading
              ? 'bg-indigo-400'
              : 'bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
          }`}
        >
          {loading ? 'Signing in...' : 'Sign in'}
        </button>
      </div>

      <div className="text-sm text-center">
        <a href="/register" className="font-medium text-indigo-600 hover:text-indigo-500">
          Don't have an account? Register here
        </a>
      </div>
    </form>
  );
}
```

**components/auth/RegisterForm.tsx:**
```tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { registerUser } from '@/lib/auth';

// Define validation schema with password complexity
const registerSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters').max(50, 'Name must be less than 50 characters'),
  email: z.string().email('Please enter a valid email address'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
      'Password must contain uppercase, lowercase, number, and special character'),
  confirmPassword: z.string().min(1, 'Please confirm your password'),
})
.refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type RegisterFormInputs = z.infer<typeof registerSchema>;

export default function RegisterForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormInputs>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormInputs) => {
    setLoading(true);
    setError('');

    try {
      const result = await registerUser({
        name: data.name,
        email: data.email,
        password: data.password
      });

      if (result.success) {
        // Redirect to home page after successful registration
        router.push('/');
        router.refresh();
      } else {
        // Handle registration errors
        setError(result.message || 'Registration failed');
      }
    } catch (err) {
      setError('An error occurred during registration');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}

      <div className="rounded-md shadow-sm -space-y-px">
        <div>
          <input
            id="name"
            type="text"
            className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
              errors.name ? 'border-red-300' : 'border-gray-300'
            } placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
            placeholder="Full name"
            {...register('name')}
          />
          {errors.name && (
            <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
          )}
        </div>
        <div>
          <input
            id="email"
            type="email"
            className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
              errors.email ? 'border-red-300' : 'border-gray-300'
            } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
            placeholder="Email address"
            {...register('email')}
          />
          {errors.email && (
            <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
          )}
        </div>
        <div>
          <input
            id="password"
            type="password"
            className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
              errors.password ? 'border-red-300' : 'border-gray-300'
            } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
            placeholder="Password"
            {...register('password')}
          />
          {errors.password && (
            <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
          )}
        </div>
        <div>
          <input
            id="confirmPassword"
            type="password"
            className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
              errors.confirmPassword ? 'border-red-300' : 'border-gray-300'
            } placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
            placeholder="Confirm password"
            {...register('confirmPassword')}
          />
          {errors.confirmPassword && (
            <p className="mt-1 text-sm text-red-600">{errors.confirmPassword.message}</p>
          )}
        </div>
      </div>

      <div>
        <button
          type="submit"
          disabled={loading}
          className={`group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white ${
            loading
              ? 'bg-indigo-400'
              : 'bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
          }`}
        >
          {loading ? 'Creating account...' : 'Create account'}
        </button>
      </div>

      <div className="text-sm text-center">
        <a href="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
          Already have an account? Sign in here
        </a>
      </div>
    </form>
  );
}
```

### 4. Backend API Endpoints

Create the authentication API endpoints in your backend:

**backend/src/api/auth.py:**
```python
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional

from backend.src.models.user import User
from backend.src.database import get_session
from backend.src.config import SECRET_KEY, ALGORITHM

router = APIRouter()
security = HTTPBearer()

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class RegisterResponse(BaseModel):
    success: bool
    user: Optional[dict] = None
    token: Optional[str] = None
    message: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    user: Optional[dict] = None
    token: Optional[str] = None
    message: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)  # 24 hour token
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=RegisterResponse)
def register_user(request: RegisterRequest, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == request.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = hash_password(request.password)  # Implement proper password hashing
    user = User(
        name=request.name,
        email=request.email,
        password_hash=hashed_password
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create token
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = create_access_token(token_data)

    return RegisterResponse(
        success=True,
        user={"id": user.id, "email": user.email, "name": user.name},
        token=token,
        message="User registered successfully"
    )

@router.post("/login", response_model=LoginResponse)
def login_user(request: LoginRequest, session: Session = Depends(get_session)):
    # Find user by email
    user = session.exec(select(User).where(User.email == request.email)).first()
    if not user or not verify_password(request.password, user.password_hash):  # Implement password verification
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create token
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = create_access_token(token_data)

    return LoginResponse(
        success=True,
        user={"id": user.id, "email": user.email, "name": user.name},
        token=token,
        message="Login successful"
    )

def hash_password(password: str) -> str:
    # Implement proper password hashing (e.g., using bcrypt)
    pass

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Implement password verification
    pass
```

### 5. Run the Application

```bash
# For the frontend
cd frontend
npm run dev

# For the backend
cd backend
uvicorn main:app --reload
```

## Environment Configuration

Create a `.env` file in your project root:

```env
# JWT Configuration
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/todoapp

# Better Auth Configuration
BETTER_AUTH_SECRET=your-better-auth-secret
BETTER_AUTH_URL=http://localhost:3000
```

## Testing Authentication

1. Navigate to `http://localhost:3000/register` to create a new account
2. Use valid credentials that meet password requirements
3. After registration, you'll be redirected to the home page
4. Navigate to `http://localhost:3000/login` to sign in with your credentials
5. Verify that validation errors appear for invalid inputs
6. Test password recovery functionality