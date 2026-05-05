"""
Script to delete old subscriptions that have NULL amount.
These are subscriptions created before the payment merge.

Usage:
    python delete_old_subscriptions.py
"""

from sqlalchemy import text
from app.database import engine

def delete_old_subscriptions():
    """Delete subscriptions with NULL amount."""
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
                print(f"✓ Found {null_count} old subscriptions with NULL amount")
                print(f"⚠️  These will be DELETED")
                
                # Delete subscriptions with NULL amount
                delete_query = text("""
                    DELETE FROM subscriptions
                    WHERE amount IS NULL
                """)
                conn.execute(delete_query)
                conn.commit()
                
                print(f"✅ Successfully deleted {null_count} old subscriptions")
                print("ℹ️  You can now create new subscriptions with payment amounts")
            else:
                print("ℹ️  No old subscriptions found (all subscriptions have amount values)")
                
    except Exception as e:
        print(f"❌ Error deleting old subscriptions: {e}")
        raise

if __name__ == "__main__":
    print("🔄 Starting cleanup of old subscriptions...")
    print("=" * 80)
    delete_old_subscriptions()
    print("=" * 80)
    print("✅ Cleanup completed successfully!")
