#!/usr/bin/env python3
"""
Test TiDB connection script
Run this to verify your TiDB connection is working before deployment
"""

import sys
from sqlalchemy import create_engine, text
from app.config import settings

def test_connection():
    print("🔍 Testing TiDB Connection...")
    print(f"📍 Host: gateway01.ap-northeast-1.prod.aws.tidbcloud.com")
    print(f"🔌 Port: 4000")
    print(f"📊 Database: gym_db")
    print()
    
    try:
        # Create engine
        print("⏳ Creating database engine...")
        engine = create_engine(settings.database_url, echo=False)
        
        # Test connection
        print("⏳ Connecting to TiDB...")
        with engine.connect() as connection:
            # Test query
            result = connection.execute(text("SELECT VERSION() as version, DATABASE() as db"))
            row = result.fetchone()
            
            print("✅ Connection successful!")
            print(f"📌 TiDB Version: {row[0]}")
            print(f"📌 Current Database: {row[1]}")
            print()
            
            # Check if gym_db exists
            result = connection.execute(text("SHOW DATABASES LIKE 'gym_db'"))
            db_exists = result.fetchone()
            
            if db_exists:
                print("✅ Database 'gym_db' exists")
                
                # Check tables
                connection.execute(text("USE gym_db"))
                result = connection.execute(text("SHOW TABLES"))
                tables = result.fetchall()
                
                if tables:
                    print(f"✅ Found {len(tables)} tables:")
                    for table in tables:
                        print(f"   - {table[0]}")
                else:
                    print("⚠️  No tables found (will be created on first run)")
            else:
                print("⚠️  Database 'gym_db' does not exist")
                print("💡 Run this SQL command in TiDB Cloud:")
                print("   CREATE DATABASE gym_db;")
            
            print()
            print("🎉 TiDB connection test completed successfully!")
            return True
            
    except Exception as e:
        print("❌ Connection failed!")
        print(f"Error: {str(e)}")
        print()
        print("🔧 Troubleshooting:")
        print("1. Check your DB_* or DATABASE_URL settings in .env file")
        print("2. Verify TiDB cluster is running in TiDB Cloud")
        print("3. Check username and password are correct")
        print("4. Ensure 'gym_db' database exists")
        print("5. Check network connectivity")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
