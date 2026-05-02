"""
Main entry point for Vercel deployment
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the FastAPI app
from app.main import app

# Vercel expects 'app' to be exported at module level
# This is the ASGI application
__all__ = ['app']
