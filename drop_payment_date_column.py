"""
Migration script to drop payment_date column from subscriptions table.
Run this script to remove the payment_date column from the database.

Usage:
    python drop_payment_date_column.py
"""

from sqlalchemy import text
from app.database import engine

def drop_payment_date_column():
    """Drop payment_date column from subscriptions table."""
    try:
        with engine.connect() as conn:
            # Check if column exists first
            check_query = text("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'subscriptions'
                AND COLUMN_NAME = 'payment_date'
            """)
            result = conn.execute(check_query)
            row = result.fetchone()
            
            if row and row[0] > 0:
                print("✓ Found payment_date column in subscriptions table")
                
                # Drop the column
                drop_query = text("""
                    ALTER TABLE subscriptions
                    DROP COLUMN payment_date
                """)
                conn.execute(drop_query)
                conn.commit()
                
                print("✅ Successfully dropped payment_date column from subscriptions table")
            else:
                print("ℹ️  payment_date column does not exist in subscriptions table (already removed)")
                
    except Exception as e:
        print(f"❌ Error dropping payment_date column: {e}")
        raise

if __name__ == "__main__":
    print("🔄 Starting migration to drop payment_date column...")
    drop_payment_date_column()
    print("✅ Migration completed successfully!")
