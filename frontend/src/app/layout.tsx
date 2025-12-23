import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Header from '@/components/Header';
import { AuthProvider } from '@/contexts/auth';
import { TaskProvider } from '@/contexts/task';
import { ToastProvider } from '@/contexts/toast';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Todo App",
  description: "A full-featured todo application with task management",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <ToastProvider>
          <AuthProvider>
            <TaskProvider>
              <div className="min-h-screen bg-gray-50">
                <Header />
                {children}
              </div>
            </TaskProvider>
          </AuthProvider>
        </ToastProvider>
      </body>
    </html>
  );
}
