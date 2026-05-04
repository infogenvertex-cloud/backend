"""
Fix NULL payment fields in existing subscriptions.
This script makes the amount and payment_date columns nullable
and optionally sets default values for existing NULL records.
"""
from datetime import datetime
from sqlalchemy import text
from app.database import engine, SessionLocal
from app.models.subscription import Subscription


def fix_null_payment_fields():
    """Make payment fields nullable and optionally set defaults for NULL values."""
    
    print("🔧 Fixing NULL payment fields in subscriptions table...")
    
    with engine.connect() as conn:
        # For TiDB/MySQL: Alter columns to allow NULL
        try:
            print("Making 'amount' column nullable...")
            conn.execute(text("ALTER TABLE subscriptions MODIFY COLUMN amount FLOAT NULL"))
            conn.commit()
            print("✅ 'amount' column is now nullable")
        except Exception as e:
            print(f"⚠️  Could not modify 'amount' column: {e}")
        
        try:
            print("Making 'payment_date' column nullable...")
            conn.execute(text("ALTER TABLE subscriptions MODIFY COLUMN payment_date DATETIME NULL"))
            conn.commit()
            print("✅ 'payment_date' column is now nullable")
        except Exception as e:
            print(f"⚠️  Could not modify 'payment_date' column: {e}")
    
    # Optional: Set default values for existing NULL records
    db = SessionLocal()
    try:
        # Find subscriptions with NULL payment fields
        null_subs = db.query(Subscription).filter(
            (Subscription.amount == None) | (Subscription.payment_date == None)
        ).all()
        
        if null_subs:
            print(f"\n📊 Found {len(null_subs)} subscriptions with NULL payment fields")
            
            for sub in null_subs:
                updated = False
                if sub.amount is None:
                    # Set a default amount of 0.0 or calculate based on plan
                    sub.amount = 0.0
                    updated = True
                    print(f"  - Set amount=0.0 for subscription ID {sub.id}")
                
                if sub.payment_date is None:
                    # Use start_date as payment_date
                    sub.payment_date = datetime.combine(sub.start_date, datetime.min.time())
                    updated = True
                    print(f"  - Set payment_date={sub.payment_date} for subscription ID {sub.id}")
                
                if updated:
                    db.add(sub)
            
            db.commit()
            print(f"✅ Updated {len(null_subs)} subscriptions with default values")
        else:
            print("✅ No subscriptions with NULL payment fields found")
    
    except Exception as e:
        print(f"❌ Error updating subscriptions: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("\n✅ Migration complete!")


if __name__ == "__main__":
    fix_null_payment_fields()
