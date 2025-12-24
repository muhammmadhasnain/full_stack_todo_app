# Todo App Backend

This is the backend for the full-stack todo app, built with FastAPI.

## Deployment

### Deploying to Render

1. Create a new Web Service on Render
2. Connect to your GitHub repository
3. Set the runtime to Python
4. Set the build command to: `pip install -r requirements.txt`
5. Set the start command to: `uvicorn src.main:app --host=0.0.0.0 --port=$PORT`
6. Add your environment variables in the Render dashboard

### Deploying to Railway

1. Create a new project on Railway
2. Connect to your GitHub repository
3. Select the backend directory
4. Railway will automatically detect it's a Python app
5. Add your environment variables in the Railway dashboard

### Environment Variables

You'll need to set these environment variables:

- `DATABASE_URL`: PostgreSQL database URL
- `FRONTEND_URL`: URL of your deployed frontend (for CORS)
- `SECRET_KEY`: Secret key for JWT tokens
- `ALGORITHM`: Algorithm for JWT (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

## Local Development

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

