"""
Migration script to drop invoice_url column from subscriptions table.
Run this script to remove the invoice_url column from the database.

Usage:
    python drop_invoice_url_column.py
"""

from sqlalchemy import text
from app.database import engine

def drop_invoice_url_column():
    """Drop invoice_url column from subscriptions table."""
    try:
        with engine.connect() as conn:
            # Check if column exists first
            check_query = text("""
                SELECT COUNT(*) as count
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'subscriptions'
                AND COLUMN_NAME = 'invoice_url'
            """)
            result = conn.execute(check_query)
            row = result.fetchone()
            
            if row and row[0] > 0:
                print("✓ Found invoice_url column in subscriptions table")
                
                # Drop the column
                drop_query = text("""
                    ALTER TABLE subscriptions
                    DROP COLUMN invoice_url
                """)
                conn.execute(drop_query)
                conn.commit()
                
                print("✅ Successfully dropped invoice_url column from subscriptions table")
            else:
                print("ℹ️  invoice_url column does not exist in subscriptions table (already removed)")
                
    except Exception as e:
        print(f"❌ Error dropping invoice_url column: {e}")
        raise

if __name__ == "__main__":
    print("🔄 Starting migration to drop invoice_url column...")
    drop_invoice_url_column()
    print("✅ Migration completed successfully!")
