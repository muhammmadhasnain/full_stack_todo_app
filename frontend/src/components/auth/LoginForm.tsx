'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/auth';
import { validateLoginForm } from '../../lib/validation';
import Input from '../ui/Input';
import Button from '../ui/Button';
import FormError from '../ui/FormError';

interface FormData {
  email: string;
  password: string;
}

const LoginForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState<boolean>(false);
  const [generalError, setGeneralError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState<boolean>(false);

  const router = useRouter();
  const { login } = useAuth();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));

    // Clear error when user starts typing
    if (errors[name as keyof FormData]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const { isValid, errors } = validateLoginForm(
      formData.email,
      formData.password
    );

    setErrors(errors);

    if (!isValid) {
      return;
    }

    setLoading(true);
    setGeneralError(null);

    try {
      await login(formData.email, formData.password);
      router.push('/');
    } catch (error: any) {
      console.error('Login error:', error);
      setGeneralError(error.message || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {generalError && <FormError message={generalError} />}

      <div>
        <Input
          type="email"
          id="email"
          name="email"
          label="Email Address"
          value={formData.email}
          onChange={handleChange}
          error={errors.email}
          placeholder="Enter your email"
          required
        />
      </div>

      <div>
        <Input
          type={showPassword ? "text" : "password"}
          id="password"
          name="password"
          label="Password"
          value={formData.password}
          onChange={handleChange}
          error={errors.password}
          placeholder="Enter your password"
          required
          showTogglePassword={true}
          onTogglePassword={() => setShowPassword(!showPassword)}
          toggleVisible={showPassword}
        />
      </div>

      <Button
        type="submit"
        className="w-full"
        disabled={loading}
        loading={loading}
      >
        {loading ? 'Signing In...' : 'Login'}
      </Button>
    </form>
  );
};

export default LoginForm;