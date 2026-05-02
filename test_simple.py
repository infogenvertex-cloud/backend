"""
Simple test endpoint to debug Vercel deployment
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World", "status": "working"}

@app.get("/test")
def test():
    import os
    return {
        "message": "Test endpoint",
        "vercel": os.getenv("VERCEL"),
        "vercel_env": os.getenv("VERCEL_ENV"),
        "database_url_set": bool(os.getenv("DATABASE_URL"))
    }