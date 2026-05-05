"""
Drop the amount column from subscriptions table.
This removes the payment-related field that is no longer needed.

Usage:
    python drop_amount_column.py
"""

from sqlalchemy import text
from app.database import engine

def drop_amount_column():
    """Drop amount column from subscriptions table."""
    try:
        with engine.connect() as conn:
            print("🔄 Dropping amount column from subscriptions table...")
            
            # Drop the amount column
            drop_query = text("ALTER TABLE subscriptions DROP COLUMN amount")
            conn.execute(drop_query)
            conn.commit()
            
            print("✅ Successfully dropped amount column from subscriptions table")
            
            # Verify the column is gone
            print("\n📊 Verifying table structure...")
            verify_query = text("DESCRIBE subscriptions")
            result = conn.execute(verify_query)
            
            print("\nCurrent subscriptions table columns:")
            print("-" * 60)
            for row in result:
                print(f"  {row[0]:20} | {row[1]:20} | {row[2]}")
                
    except Exception as e:
        print(f"❌ Error dropping column: {e}")
        raise

if __name__ == "__main__":
    print("⚠️  WARNING: This will permanently remove the amount column!")
    print("Make sure you have a backup if needed.\n")
    
    response = input("Do you want to continue? (yes/no): ")
    if response.lower() == "yes":
        drop_amount_column()
        print("\n✅ Migration completed successfully!")
        print("💡 Tip: Restart your backend server to see the changes.")
    else:
        print("❌ Migration cancelled.")

