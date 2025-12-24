import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        secondary: {
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
        },
        priority: {
          high: '#ef4444',    // red
          medium: '#f59e0b',  // yellow
          low: '#10b981',     // green
        }
      },
    },
  },
  plugins: [],
};
export default config;