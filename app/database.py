import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# For Vercel deployment, handle database URL properly
database_url = settings.DATABASE_URL

# If running on Vercel and using TiDB, modify the connection string
if os.getenv("VERCEL") and "tidbcloud.com" in database_url:
    # For TiDB on Vercel, use SSL without certificate file
    if "ssl_ca=" in database_url:
        # Remove ssl_ca parameter and use ssl_verify_cert=false for Vercel
        parts = database_url.split("?")
        if len(parts) > 1:
            base_url = parts[0]
            params = parts[1].split("&")
            # Filter out ssl_ca parameter and modify SSL settings for Vercel
            filtered_params = []
            for p in params:
                if not p.startswith("ssl_ca="):
                    if p.startswith("ssl_verify_cert="):
                        filtered_params.append("ssl_verify_cert=false")
                    elif p.startswith("ssl_verify_identity="):
                        filtered_params.append("ssl_verify_identity=false")
                    else:
                        filtered_params.append(p)
            
            # Add SSL mode if not present
            if not any(p.startswith("ssl_") for p in filtered_params):
                filtered_params.append("ssl_disabled=false")
            
            database_url = f"{base_url}?{'&'.join(filtered_params)}"

try:
    engine = create_engine(database_url, pool_pre_ping=True, pool_recycle=3600)
except Exception as e:
    # Fallback to SQLite for development/testing
    print(f"Database connection failed: {e}")
    print("Falling back to SQLite...")
    engine = create_engine("sqlite:///./gym.db", pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


