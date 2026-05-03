import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# Use the database_url property from settings
database_url = settings.database_url

print(f"Connecting to database: {database_url.replace(settings.DB_PASSWORD, '***') if settings.DB_PASSWORD else database_url}")

try:
    engine = create_engine(database_url, pool_pre_ping=True, pool_recycle=3600)
    # Test the connection
    with engine.connect() as conn:
        conn.execute("SELECT 1")
    print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")
    print("Falling back to SQLite...")
    engine = create_engine("sqlite:///./gym.db", pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


