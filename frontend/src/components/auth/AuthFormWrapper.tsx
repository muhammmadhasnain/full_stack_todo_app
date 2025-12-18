'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface AuthFormWrapperProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  showNavigation?: boolean;
}

const AuthFormWrapper: React.FC<AuthFormWrapperProps> = ({
  title,
  subtitle,
  children,
  showNavigation = true,
}) => {
  const pathname = usePathname();
  const isLoginPage = pathname === '/login';
  const isRegisterPage = pathname === '/register';

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            {title}
          </h2>
          {subtitle && (
            <p className="mt-2 text-center text-sm text-gray-600">
              {subtitle}
            </p>
          )}
        </div>

        <div className="mt-8 bg-white py-8 px-4 shadow rounded-lg sm:px-10">
          {children}

          {showNavigation && (
            <div className="mt-6 text-center">
              {isLoginPage ? (
                <p className="text-sm text-gray-600">
                  Don't have an account?{' '}
                  <Link
                    href="/register"
                    className="font-medium text-blue-600 hover:text-blue-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded"
                    aria-label="Register for a new account"
                  >
                    Register here
                  </Link>
                </p>
              ) : isRegisterPage ? (
                <p className="text-sm text-gray-600">
                  Already have an account?{' '}
                  <Link
                    href="/login"
                    className="font-medium text-blue-600 hover:text-blue-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded"
                    aria-label="Sign in to your account"
                  >
                    Login here
                  </Link>
                </p>
              ) : null}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthFormWrapper;