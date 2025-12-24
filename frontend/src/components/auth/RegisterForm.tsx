'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/auth';
import { validateRegisterForm } from '../../lib/validation';
import Input from '../ui/Input';
import Button from '../ui/Button';
import FormError from '../ui/FormError';

interface FormData {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

const RegisterForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState<boolean>(false);
  const [generalError, setGeneralError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState<boolean>(false);

  const router = useRouter();
  const { register } = useAuth();

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

    const { isValid, errors } = validateRegisterForm(
      formData.name,
      formData.email,
      formData.password,
      formData.confirmPassword
    );

    setErrors(errors);

    if (!isValid) {
      return;
    }

    setLoading(true);
    setGeneralError(null);

    try {
      await register(formData.email, formData.password, formData.name);
      router.push('/');
    } catch (error: any) {
      console.error('Registration error:', error);
      setGeneralError(error.message || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {generalError && <FormError message={generalError} />}

      <div>
        <Input
          type="text"
          id="name"
          name="name"
          label="Full Name"
          value={formData.name}
          onChange={handleChange}
          error={errors.name}
          placeholder="Enter your full name"
          required
        />
      </div>

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

      <div>
        <Input
          type={showConfirmPassword ? "text" : "password"}
          id="confirmPassword"
          name="confirmPassword"
          label="Confirm Password"
          value={formData.confirmPassword}
          onChange={handleChange}
          error={errors.confirmPassword}
          placeholder="Confirm your password"
          required
          showTogglePassword={true}
          onTogglePassword={() => setShowConfirmPassword(!showConfirmPassword)}
          toggleVisible={showConfirmPassword}
        />
      </div>

      <Button
        type="submit"
        className="w-full"
        disabled={loading}
        loading={loading}
      >
        {loading ? 'Creating Account...' : 'Register'}
      </Button>
    </form>
  );
};

export default RegisterForm;