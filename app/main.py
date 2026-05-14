import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import auth, members, payments, dashboard, visitors, expiring, revenue

logging.basicConfig(level=logging.INFO)

# Initialize database tables
try:
    if settings.DB_PASSWORD:
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables created successfully")
    else:
        logging.warning("Database password not set, skipping table creation")
except Exception as e:
    logging.error(f"Error creating database tables: {e}")
    pass

app = FastAPI(title="Gym Management System")

# CORS Configuration - Allow all origins for API access
# Using wildcard with credentials=False is the safest approach for Vercel
origins = [
    "https://frontend-three-swart-2tke12jw3z.vercel.app",
    "http://localhost:5173",
    "http://localhost:5006",
    "http://localhost:3000",
]

# Add wildcard support for Vercel preview deployments
if os.getenv("VERCEL_ENV") == "production":
    origins.append("https://*.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Only mount static files if directory exists (won't exist in Vercel)
if os.path.exists("invoices"):
    from fastapi.staticfiles import StaticFiles
    app.mount("/invoices", StaticFiles(directory="invoices"), name="invoices")

app.include_router(auth.router)
app.include_router(members.router)
app.include_router(payments.router)
app.include_router(dashboard.router)
app.include_router(visitors.router)
app.include_router(expiring.router)
app.include_router(revenue.router)

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
