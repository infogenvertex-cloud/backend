import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# For Vercel deployment, simplify the database URL (remove SSL cert path issues)
database_url = settings.DATABASE_URL

# If running on Vercel, remove the ssl_ca parameter as it causes path issues
# TiDB Cloud still requires SSL, but we'll use ssl_verify_cert and ssl_verify_identity
if os.getenv("VERCEL") or os.getenv("VERCEL_ENV"):
    if "ssl_ca=" in database_url:
        # Remove ssl_ca parameter but keep other SSL parameters
        parts = database_url.split("?")
        if len(parts) > 1:
            base_url = parts[0]
            params = parts[1].split("&")
            # Filter out ssl_ca parameter
            filtered_params = [p for p in params if not p.startswith("ssl_ca=")]
            database_url = f"{base_url}?{'&'.join(filtered_params)}" if filtered_params else base_url

engine = create_engine(database_url, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


