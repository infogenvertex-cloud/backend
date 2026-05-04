"""
Script to drop the payments table from TiDB production database.
Run this ONCE after confirming the merge is working.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

# Load environment variables
load_dotenv()

def drop_payments_table():
    # Try to get DATABASE_URL or construct it from components
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        # Construct from individual components
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_username = os.getenv("DB_USERNAME")
        db_password = os.getenv("DB_PASSWORD")
        db_database = os.getenv("DB_DATABASE")
        
        if all([db_host, db_port, db_username, db_password, db_database]):
            database_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}?ssl_ca=&ssl_verify_cert=true&ssl_verify_identity=true"
        else:
            print("❌ Database configuration not found in environment variables")
            return
    
    print(f"Connecting to database...")
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        print("\n=== Checking existing tables ===")
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        print(f"Existing tables: {existing_tables}")
        
        if "payments" in existing_tables:
            print("\n=== Dropping payments table ===")
            try:
                conn.execute(text("DROP TABLE payments"))
                conn.commit()
                print("✅ Table 'payments' dropped successfully from TiDB")
            except Exception as e:
                print(f"❌ Error dropping table: {e}")
        else:
            print("\n⚠️  Table 'payments' does not exist in TiDB")
        
        print("\n=== Verifying remaining tables ===")
        inspector = inspect(engine)
        remaining_tables = inspector.get_table_names()
        print(f"Remaining tables: {remaining_tables}")

if __name__ == "__main__":
    print("=" * 60)
    print("DROP PAYMENTS TABLE FROM TIDB")
    print("=" * 60)
    print("\n⚠️  WARNING: This will drop the 'payments' table from TiDB!")
    print("Make sure you have a backup before proceeding.")
    print("=" * 60)
    
    response = input("\nDo you want to continue? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        drop_payments_table()
    else:
        print("\n❌ Operation cancelled.")
