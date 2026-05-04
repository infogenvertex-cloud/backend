"""
Script to drop unused tables from the database.
This removes the old 'payments' table since payment data is now in subscriptions.

Run this script ONCE after confirming the merge is working correctly.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

# Load environment variables
load_dotenv()

def drop_unused_tables():
    # Get database URL from environment or use SQLite default
    database_url = os.getenv("DATABASE_URL", "sqlite:///./gym.db")
    print(f"Using database: {database_url}")
    
    engine = create_engine(database_url)
    inspector = inspect(engine)
    
    # List of tables to drop
    tables_to_drop = ["payments"]
    
    with engine.connect() as conn:
        print("\n=== Checking existing tables ===")
        existing_tables = inspector.get_table_names()
        print(f"Existing tables: {existing_tables}")
        
        print("\n=== Dropping unused tables ===")
        for table in tables_to_drop:
            if table in existing_tables:
                try:
                    print(f"Dropping table '{table}'...")
                    conn.execute(text(f"DROP TABLE {table}"))
                    conn.commit()
                    print(f"✅ Table '{table}' dropped successfully")
                except Exception as e:
                    print(f"❌ Error dropping table '{table}': {e}")
            else:
                print(f"⚠️  Table '{table}' does not exist, skipping")
        
        print("\n=== Verifying remaining tables ===")
        # Refresh inspector
        inspector = inspect(engine)
        remaining_tables = inspector.get_table_names()
        print(f"Remaining tables: {remaining_tables}")
        
        print("\n✅ Cleanup completed successfully!")
        print("\nRemaining tables should be:")
        print("  - admins")
        print("  - members")
        print("  - subscriptions (with payment fields)")
        print("  - visitors")

if __name__ == "__main__":
    print("=" * 60)
    print("DROP UNUSED TABLES SCRIPT")
    print("=" * 60)
    print("\nThis will drop the following tables:")
    print("  - payments (data now in subscriptions)")
    print("\n⚠️  WARNING: This action cannot be undone!")
    print("Make sure you have a backup before proceeding.")
    print("=" * 60)
    
    response = input("\nDo you want to continue? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        drop_unused_tables()
    else:
        print("\n❌ Operation cancelled.")
