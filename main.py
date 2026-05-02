"""
Main entry point for Vercel deployment
This file should be at the root of the backend directory
"""
import sys
import os

# Ensure the app directory is in the path
sys.path.insert(0, os.path.dirname(__file__))

from app.main import app

# Export for Vercel
handler = app
