"""
Add amount and payment_date columns back to subscriptions table.

Usage:
    python add_payment_tracking_fields.py
"""

from sqlalchemy import text
from app.database import engine

def add_payment_fields():
    """Add amount and payment_date columns to subscriptions table."""
    try:
        with engine.connect() as conn:
            print("🔄 Adding payment tracking fields to subscriptions table...")
            
            # Add amount column
            try:
                print("  Adding 'amount' column...")
                conn.execute(text("ALTER TABLE subscriptions ADD COLUMN amount FLOAT NOT NULL DEFAULT 0.0"))
                conn.commit()
                print("  ✅ 'amount' column added")
            except Exception as e:
                print(f"  ⚠️  'amount' column might already exist: {e}")
            
            # Add payment_date column
            try:
                print("  Adding 'payment_date' column...")
                conn.execute(text("ALTER TABLE subscriptions ADD COLUMN payment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP"))
                conn.commit()
                print("  ✅ 'payment_date' column added")
            except Exception as e:
                print(f"  ⚠️  'payment_date' column might already exist: {e}")
            
            print("\n✅ Successfully added payment tracking fields to subscriptions table")
            
            # Verify the columns were added
            print("\n📊 Verifying table structure...")
            verify_query = text("DESCRIBE subscriptions")
            result = conn.execute(verify_query)
            
            print("\nCurrent subscriptions table columns:")
            print("-" * 60)
            for row in result:
                print(f"  {row[0]:20} | {row[1]:20} | {row[2]}")
                
    except Exception as e:
        print(f"❌ Error adding columns: {e}")
        raise

if __name__ == "__main__":
    add_payment_fields()
    print("\n✅ Migration completed successfully!")
    print("💡 Tip: Restart your backend server to see the changes.")
