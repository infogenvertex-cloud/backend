import logging
import os
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base
from app.routers import auth, members, subscriptions, payments, dashboard, visitors
from app.services.scheduler_service import check_expiring_subscriptions

logging.basicConfig(level=logging.INFO)

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    scheduler.add_job(
        check_expiring_subscriptions,
        CronTrigger(hour=settings.SCHEDULER_HOUR, minute=settings.SCHEDULER_MINUTE),
        id="daily_expiry_check",
        replace_existing=True,
    )
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(title="Gym Management System", lifespan=lifespan)

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
    app.mount("/invoices", StaticFiles(directory="invoices"), name="invoices")

app.include_router(auth.router)
app.include_router(members.router)
app.include_router(subscriptions.router)
app.include_router(payments.router)
app.include_router(dashboard.router)
app.include_router(visitors.router)

# Health check endpoint for Vercel
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Gym Management API is running"}

# Vercel serverless function handler
handler = app
