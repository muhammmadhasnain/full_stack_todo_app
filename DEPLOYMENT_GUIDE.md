# Full-Stack Todo App Deployment Guide

This guide provides instructions for deploying both the frontend (Next.js) and backend (FastAPI) components of the todo app.

## Architecture Overview

- **Frontend**: Next.js 16+ application deployed to Vercel
- **Backend**: FastAPI application deployed to Render, Railway, or similar platform
- **Database**: PostgreSQL (can be deployed separately or as an add-on)

## Prerequisites

- Git repository with your code
- Accounts on deployment platforms (Vercel for frontend, Render/Railway for backend)
- Environment variables ready for deployment

## Deployment Steps

### 1. Deploy the Backend

#### Option A: Deploy to Render

1. Create a new Web Service on Render
2. Connect to your GitHub repository
3. Set the runtime to Python
4. Set the build command to: `pip install -r requirements.txt`
5. Set the start command to: `uvicorn src.main:app --host=0.0.0.0 --port=$PORT`
6. Add environment variables in the Render dashboard:
   - `DATABASE_URL`: PostgreSQL database URL
   - `FRONTEND_URL`: URL of your deployed frontend (e.g., `https://your-app.vercel.app`)
   - `SECRET_KEY`: Secret key for JWT tokens
   - `ALGORITHM`: Algorithm for JWT (default: HS256)
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

#### Option B: Deploy to Railway

1. Create a new project on Railway
2. Connect to your GitHub repository
3. Select the backend directory
4. Railway will automatically detect it's a Python app
5. Add environment variables in the Railway dashboard (same as Render)

### 2. Deploy the Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Vercel CLI (if not already installed):
   ```bash
   npm install -g vercel
   ```

3. Log in to Vercel:
   ```bash
   vercel login
   ```

4. Deploy the application:
   ```bash
   vercel --prod
   ```

5. Add environment variables in the Vercel project settings:
   - `NEXT_PUBLIC_API_URL`: URL of your deployed backend API (e.g., `https://your-backend.onrender.com`)

### 3. Environment Variables Reference

#### Backend Environment Variables

- `DATABASE_URL`: PostgreSQL database URL (format: `postgresql://user:password@host:port/database`)
- `FRONTEND_URL`: URL of your deployed frontend (for CORS)
- `SECRET_KEY`: Secret key for JWT tokens (generate with `openssl rand -hex 32`)
- `ALGORITHM`: Algorithm for JWT (default: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: `30`)
- `DEBUG`: Enable/disable debug mode (default: `False`)

#### Frontend Environment Variables

- `NEXT_PUBLIC_API_URL`: URL of your deployed backend API

## Database Setup

For production, you'll need a PostgreSQL database. You can:

1. Use a managed service like Neon, AWS RDS, or Google Cloud SQL
2. Use Render's or Railway's built-in PostgreSQL add-ons
3. Use a separate PostgreSQL provider

Make sure to run database migrations when deploying. You can add this as a deployment script if needed.

## Post-Deployment Steps

1. Verify both frontend and backend are accessible
2. Test API endpoints by visiting your backend URL (e.g., `https://your-backend.onrender.com/health`)
3. Register a new user and test the application functionality
4. Check browser console and server logs for any errors

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure `FRONTEND_URL` in your backend environment variables matches your deployed frontend URL exactly
2. **API Connection Errors**: Verify `NEXT_PUBLIC_API_URL` in your frontend environment variables
3. **Database Connection Errors**: Check that your `DATABASE_URL` is properly formatted and accessible

### Debugging Tips

1. Check the deployment logs in your hosting platform dashboard
2. Test API endpoints directly in your browser (e.g., `/health` endpoint)
3. Use browser developer tools to check for API errors in the Network tab

## Scaling Considerations

- Monitor your database connection pool size as traffic increases
- Consider implementing caching for frequently accessed data
- Set up proper logging and monitoring for production issues
- Implement proper error handling and user feedback