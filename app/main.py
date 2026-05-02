import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import auth, members, subscriptions, payments, dashboard, visitors

logging.basicConfig(level=logging.INFO)

# Initialize database tables
try:
    Base.metadata.create_all(bind=engine)
    logging.info("Database tables created successfully")
except Exception as e:
    logging.error(f"Error creating database tables: {e}")

app = FastAPI(title="Gym Management System")

# CORS Configuration - Allow both local and production URLs
allowed_origins = [
    "http://localhost:5006",
    "http://localhost:5007",
    "http://localhost:3000",
]

# Add production frontend URL from environment variable
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

# For Vercel deployment, allow all vercel.app domains in development
if os.getenv("VERCEL_ENV") == "preview" or os.getenv("VERCEL_ENV") == "development":
    allowed_origins.append("https://*.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if os.getenv("VERCEL_ENV") != "production" else [frontend_url] if frontend_url else allowed_origins,
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
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Gym Management API is running"}

# Vercel serverless function handler
handler = app
