import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import auth, members, subscriptions, payments, dashboard, visitors

logging.basicConfig(level=logging.INFO)

# Initialize database tables
try:
    # Only try to create tables if we have a valid database connection
    if settings.DB_PASSWORD:
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables created successfully")
    else:
        logging.warning("Database password not set, skipping table creation")
except Exception as e:
    logging.error(f"Error creating database tables: {e}")
    # Don't fail the app startup, just log the error
    pass

app = FastAPI(title="Gym Management System")

# CORS Configuration - Allow frontend domains
allowed_origins = [
    "http://localhost:5006",
    "http://localhost:5007", 
    "http://localhost:3000",
    "https://frontend-three-swart-21e12w3z.vercel.app",  # Add your frontend URL
]

# Add production frontend URL from environment variable
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

# For Vercel deployment, be more permissive with CORS
if os.getenv("VERCEL"):  # Vercel sets this environment variable
    allowed_origins.extend([
        "https://*.vercel.app",
        "https://frontend-three-swart-21e12w3z.vercel.app"
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if os.getenv("VERCEL") else allowed_origins,  # Allow all origins in Vercel for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Only mount static files if directory exists (won't exist in Vercel)
if os.path.exists("invoices"):
    from fastapi.staticfiles import StaticFiles
    app.mount("/invoices", StaticFiles(directory="invoices"), name="invoices")

app.include_router(auth.router)
app.include_router(members.router)
app.include_router(subscriptions.router)
app.include_router(payments.router)
app.include_router(dashboard.router)
app.include_router(visitors.router)

# Health check endpoint for Vercel
@app.get("/")
def root():
    """Simple root endpoint that always works"""
    return {
        "status": "ok", 
        "message": "Gym Management API is running",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Detailed health check with database status"""
    try:
        # Test database connection
        from sqlalchemy import text
        from app.database import engine
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logging.error(f"Database health check failed: {e}")
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy", 
        "message": "Gym Management API is running",
        "database": db_status,
        "environment": "vercel" if os.getenv("VERCEL") else "local"
    }

# Debug endpoint
@app.get("/debug")
def debug_info():
    return {
        "vercel": bool(os.getenv("VERCEL")),
        "vercel_env": os.getenv("VERCEL_ENV"),
        "db_host": settings.DB_HOST,
        "db_port": settings.DB_PORT,
        "db_username": settings.DB_USERNAME,
        "db_password_set": bool(settings.DB_PASSWORD),
        "database_url_set": bool(settings.DATABASE_URL),
        "base_url": settings.BASE_URL
    }

# Vercel serverless function handler
handler = app
