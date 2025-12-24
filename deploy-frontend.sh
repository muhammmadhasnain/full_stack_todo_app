#!/bin/bash
# Deployment script for the full-stack todo app frontend

echo "Starting deployment of the frontend to Vercel..."

# Navigate to frontend directory
cd frontend

# Install Vercel CLI if not already installed
npm install -g vercel

# Check if logged in to Vercel
if ! vercel whoami &> /dev/null; then
    echo "You need to log in to Vercel first."
    echo "Please run 'vercel login' in your terminal and follow the instructions."
    exit 1
fi

echo "Logged in to Vercel successfully!"

# Deploy to Vercel
echo "Deploying to Vercel..."
vercel --prod

echo "Frontend deployment completed!"
echo "Remember to set the NEXT_PUBLIC_API_URL environment variable in your Vercel dashboard"
echo "to point to your deployed backend API."