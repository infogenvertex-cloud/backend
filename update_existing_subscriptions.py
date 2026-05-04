"""
Script to update existing subscription records with default payment fields.
This adds default values for amount, payment_date, and invoice_url to existing subscriptions.

Run this ONCE after the schema migration to populate existing records.
"""
import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

def update_existing_subscriptions():
    # Get database URL from environment or construct it
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
            database_url = "sqlite:///./gym.db"
    
    print(f"Connecting to database...")
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        print("\n=== Checking subscriptions without payment data ===")
        
        # Check how many subscriptions need updating
        result = conn.execute(text("""
            SELECT COUNT(*) as count 
            FROM subscriptions 
            WHERE amount IS NULL OR payment_date IS NULL
        """))
        count = result.fetchone()[0]
        
        print(f"Found {count} subscriptions without payment data")
        
        if count == 0:
            print("\n✅ All subscriptions already have payment data!")
            return
        
        print("\n=== Updating subscriptions with default payment data ===")
        
        # Update subscriptions with NULL amount/payment_date
        # Set default amount to 0 and payment_date to start_date
        try:
            conn.execute(text("""
                UPDATE subscriptions 
                SET 
                    amount = CASE WHEN amount IS NULL THEN 0 ELSE amount END,
                    payment_date = CASE WHEN payment_date IS NULL THEN start_date ELSE payment_date END
                WHERE amount IS NULL OR payment_date IS NULL
            """))
            conn.commit()
            
            print(f"✅ Updated {count} subscriptions with default payment data")
            print("   - amount: 0 (default)")
            print("   - payment_date: start_date")
            print("   - invoice_url: NULL (will be generated on next payment)")
            
        except Exception as e:
            print(f"❌ Error updating subscriptions: {e}")
            return
        
        print("\n=== Verification ===")
        
        # Verify the update
        result = conn.execute(text("""
            SELECT COUNT(*) as count 
            FROM subscriptions 
            WHERE amount IS NULL OR payment_date IS NULL
        """))
        remaining = result.fetchone()[0]
        
        if remaining == 0:
            print("✅ All subscriptions now have payment data!")
        else:
            print(f"⚠️  {remaining} subscriptions still need updating")
        
        # Show sample of updated records
        print("\n=== Sample Updated Records ===")
        result = conn.execute(text("""
            SELECT id, plan, start_date, amount, payment_date 
            FROM subscriptions 
            LIMIT 5
        """))
        
        print("\nID | Plan      | Start Date | Amount | Payment Date")
        print("-" * 60)
        for row in result:
            print(f"{row[0]:2d} | {row[1]:9s} | {row[2]} | Rs. {row[3]:6.2f} | {row[4]}")
        
        print("\n✅ Update completed successfully!")
        print("\nNOTE: Existing subscriptions now have:")
        print("  - amount = 0 (you may want to update these manually)")
        print("  - payment_date = start_date")
        print("  - invoice_url = NULL (no invoice for old records)")

if __name__ == "__main__":
    print("=" * 60)
    print("UPDATE EXISTING SUBSCRIPTIONS WITH PAYMENT DATA")
    print("=" * 60)
    print("\nThis will update existing subscriptions with default values:")
    print("  - amount: 0")
    print("  - payment_date: start_date")
    print("  - invoice_url: NULL")
    print("\n⚠️  You may want to manually update the amount values later.")
    print("=" * 60)
    
    response = input("\nDo you want to continue? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        update_existing_subscriptions()
    else:
        print("\n❌ Operation cancelled.")
