"""
Fix the amount column to be NOT NULL and update existing NULL values.
"""

from sqlalchemy import text
from app.database import engine

def fix_amount_column():
    """Make amount column NOT NULL and update existing NULL values."""
    try:
        with engine.connect() as conn:
            print("🔄 Fixing amount column...")
            
            # First, update all NULL amounts to 0.0
            print("\n1. Updating NULL amounts to 0.0...")
            update_query = text("UPDATE subscriptions SET amount = 0.0 WHERE amount IS NULL")
            result = conn.execute(update_query)
            conn.commit()
            print(f"   ✅ Updated {result.rowcount} rows")
            
            # Now modify the column to NOT NULL
            print("\n2. Modifying column to NOT NULL...")
            try:
                alter_query = text("ALTER TABLE subscriptions MODIFY COLUMN amount FLOAT NOT NULL")
                conn.execute(alter_query)
                conn.commit()
                print("   ✅ Column modified to NOT NULL")
            except Exception as e:
                print(f"   ⚠️  Could not modify column: {e}")
            
            # Verify the changes
            print("\n3. Verifying changes...")
            verify_query = text("SELECT id, member_id, amount FROM subscriptions WHERE amount = 0.0")
            result = conn.execute(verify_query)
            rows = result.fetchall()
            
            if rows:
                print(f"\n   ⚠️  Found {len(rows)} subscriptions with 0.0 amount:")
                print("   ID   | Member ID | Amount")
                print("   " + "-" * 40)
                for row in rows:
                    print(f"   {row[0]:4} | {row[1]:9} | {row[2]}")
                print("\n   💡 These subscriptions need proper amounts assigned!")
            else:
                print("   ✅ All subscriptions have non-zero amounts")
            
            print("\n✅ Fix completed!")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    fix_amount_column()
