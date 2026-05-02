import sys
from pathlib import Path

# Add parent directory to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

# Import and export the FastAPI app
from app.main import app

# Vercel expects 'app' to be exported
__all__ = ['app']



