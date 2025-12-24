# Deploying the Frontend to Vercel

## Prerequisites

- Vercel CLI installed (`npm install -g vercel`)
- A Vercel account

## Deployment Steps

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Log in to Vercel:
   ```bash
   vercel login
   ```

3. Deploy the application:
   ```bash
   vercel --prod
   ```

## Environment Variables

Make sure to set these environment variables in your Vercel project settings:

- `NEXT_PUBLIC_API_URL`: URL of your deployed backend API (e.g., `https://your-backend.onrender.com`)

## Important Notes

- The frontend is built with Next.js 16+ using the App Router
- The frontend expects the backend API to be available at the URL specified in `NEXT_PUBLIC_API_URL`
- For development, you can run `npm run dev` in the frontend directory
- For production build, run `npm run build`