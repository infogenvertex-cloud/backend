"""
Migration script to drop the unused payments table.
The payments functionality has been merged into the subscriptions table.

Usage:
    python drop_payments_table.py
"""

from sqlalchemy import text
from app.database import engine

def drop_payments_table():
    """Drop the unused payments table from the database."""
    try:
        with engine.connect() as conn:
            # Check if table exists first
            check_query = text("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'payments'
            """)
            result = conn.execute(check_query)
            row = result.fetchone()
            
            if row and row[0] > 0:
                print("✓ Found payments table in database")
                
                # Drop the table
                drop_query = text("DROP TABLE payments")
                conn.execute(drop_query)
                conn.commit()
                
                print("✅ Successfully dropped payments table from database")
                print("ℹ️  Payment functionality is now merged into subscriptions table")
            else:
                print("ℹ️  payments table does not exist in database (already removed)")
                
    except Exception as e:
        print(f"❌ Error dropping payments table: {e}")
        raise

if __name__ == "__main__":
    print("🔄 Starting migration to drop unused payments table...")
    print("⚠️  Note: Payment data has been merged into subscriptions table")
    drop_payments_table()
    print("✅ Migration completed successfully!")
