"""
Migration script to update old subscriptions with default amount.
Sets amount to 500.0 for all subscriptions that have NULL amount.

Usage:
    python update_old_subscriptions_with_amount.py
"""

from sqlalchemy import text
from app.database import engine

def update_old_subscriptions():
    """Update old subscriptions with default amount."""
    try:
        with engine.connect() as conn:
            # Check how many subscriptions have NULL amount
            check_query = text("""
                SELECT COUNT(*) as count
                FROM subscriptions
                WHERE amount IS NULL
            """)
            result = conn.execute(check_query)
            row = result.fetchone()
            null_count = row[0] if row else 0
            
            if null_count > 0:
                print(f"✓ Found {null_count} subscriptions with NULL amount")
                
                # Update subscriptions with NULL amount to default 500.0
                update_query = text("""
                    UPDATE subscriptions
                    SET amount = 500.0
                    WHERE amount IS NULL
                """)
                conn.execute(update_query)
                conn.commit()
                
                print(f"✅ Successfully updated {null_count} subscriptions with default amount (Rs. 500.00)")
            else:
                print("ℹ️  All subscriptions already have amount values")
                
    except Exception as e:
        print(f"❌ Error updating subscriptions: {e}")
        raise

if __name__ == "__main__":
    print("🔄 Starting migration to update old subscriptions with amount...")
    update_old_subscriptions()
    print("✅ Migration completed successfully!")
