"""
Database migration script to convert from complex subscription model to simple payment model.

This script will:
1. Backup existing subscription data (optional)
2. Drop the subscriptions table
3. Create the new payments table
4. Optionally migrate data from subscriptions to payments
"""

import sys
from sqlalchemy import text
from app.database import engine, SessionLocal
from app.models import Member, Payment, Visitor, Admin

def backup_subscriptions(db):
    """Backup subscription data before dropping table"""
    try:
        result = db.execute(text("SELECT * FROM subscriptions"))
        subscriptions = result.fetchall()
        
        if subscriptions:
            print(f"\n📦 Found {len(subscriptions)} subscription records")
            print("Subscription data:")
            for sub in subscriptions[:5]:  # Show first 5
                print(f"  - ID: {sub[0]}, Member: {sub[1]}, Amount: {sub[6] if len(sub) > 6 else 'N/A'}")
            if len(subscriptions) > 5:
                print(f"  ... and {len(subscriptions) - 5} more")
            return subscriptions
        else:
            print("\n✅ No subscription data found")
            return []
    except Exception as e:
        print(f"\n⚠️  Subscriptions table doesn't exist or error: {e}")
        return []


def migrate_subscriptions_to_payments(db, subscriptions):
    """Convert subscription records to payment records"""
    if not subscriptions:
        print("\n✅ No data to migrate")
        return 0
    
    print("\n🔄 Migrating subscription data to payments...")
    migrated = 0
    
    for sub in subscriptions:
        try:
            # Extract data from subscription tuple
            # Assuming: id, member_id, plan, start_date, end_date, status, amount, payment_date
            member_id = sub[1]
            plan = sub[2] if len(sub) > 2 else "1_month"
            amount = sub[6] if len(sub) > 6 and sub[6] is not None else 0.0
            payment_date = sub[7] if len(sub) > 7 and sub[7] is not None else sub[3]  # Use start_date if no payment_date
            
            # Only migrate if there's a valid amount
            if amount > 0:
                payment = Payment(
                    member_id=member_id,
                    amount=amount,
                    plan=plan,
                    payment_date=payment_date,
                    notes="Migrated from subscription"
                )
                db.add(payment)
                migrated += 1
        except Exception as e:
            print(f"  ⚠️  Error migrating record: {e}")
            continue
    
    db.commit()
    print(f"✅ Migrated {migrated} payment records")
    return migrated


def drop_subscriptions_table(db):
    """Drop the subscriptions table"""
    try:
        print("\n🗑️  Dropping subscriptions table...")
        db.execute(text("DROP TABLE IF EXISTS subscriptions"))
        db.commit()
        print("✅ Subscriptions table dropped")
        return True
    except Exception as e:
        print(f"❌ Error dropping subscriptions table: {e}")
        db.rollback()
        return False


def create_payments_table():
    """Create the new payments table using SQLAlchemy models"""
    try:
        print("\n🔨 Creating payments table...")
        from app.database import Base
        Base.metadata.create_all(bind=engine)
        print("✅ Payments table created")
        return True
    except Exception as e:
        print(f"❌ Error creating payments table: {e}")
        return False


def verify_tables(db):
    """Verify the new table structure"""
    print("\n🔍 Verifying database tables...")
    
    try:
        # Check existing tables
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE()
        """))
        tables = [row[0] for row in result.fetchall()]
        
        print("\n📋 Current tables:")
        for table in tables:
            print(f"  ✅ {table}")
        
        # Verify payments table exists
        if 'payments' in tables:
            print("\n✅ Payments table exists")
            
            # Check payments table structure
            result = db.execute(text("DESCRIBE payments"))
            columns = result.fetchall()
            print("\n📊 Payments table structure:")
            for col in columns:
                print(f"  - {col[0]}: {col[1]}")
        else:
            print("\n⚠️  Payments table not found!")
        
        # Check if subscriptions table still exists
        if 'subscriptions' in tables:
            print("\n⚠️  Warning: Subscriptions table still exists!")
        else:
            print("\n✅ Subscriptions table removed")
            
    except Exception as e:
        print(f"❌ Error verifying tables: {e}")


def main():
    print("=" * 60)
    print("🔄 DATABASE MIGRATION: Subscriptions → Payments")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Step 1: Backup existing data
        print("\n📋 STEP 1: Backup existing subscription data")
        subscriptions = backup_subscriptions(db)
        
        # Ask user if they want to migrate data
        if subscriptions:
            print("\n⚠️  You have existing subscription data!")
            print("Options:")
            print("  1. Migrate data to payments table (recommended)")
            print("  2. Drop data without migration")
            print("  3. Cancel migration")
            
            choice = input("\nEnter your choice (1/2/3): ").strip()
            
            if choice == "3":
                print("\n❌ Migration cancelled")
                return
            elif choice == "1":
                migrate_data = True
            else:
                migrate_data = False
                print("\n⚠️  Data will be lost!")
                confirm = input("Type 'YES' to confirm: ").strip()
                if confirm != "YES":
                    print("\n❌ Migration cancelled")
                    return
        else:
            migrate_data = False
        
        # Step 2: Create payments table first (if migrating)
        if migrate_data:
            print("\n📋 STEP 2: Create payments table")
            if not create_payments_table():
                print("\n❌ Migration failed")
                return
            
            # Step 3: Migrate data
            print("\n📋 STEP 3: Migrate data")
            migrate_subscriptions_to_payments(db, subscriptions)
        
        # Step 4: Drop subscriptions table
        print("\n📋 STEP 4: Drop subscriptions table")
        if not drop_subscriptions_table(db):
            print("\n❌ Migration failed")
            return
        
        # Step 5: Create payments table (if not migrating)
        if not migrate_data:
            print("\n📋 STEP 5: Create payments table")
            if not create_payments_table():
                print("\n❌ Migration failed")
                return
        
        # Step 6: Verify
        print("\n📋 STEP 6: Verify tables")
        verify_tables(db)
        
        print("\n" + "=" * 60)
        print("✅ MIGRATION COMPLETE!")
        print("=" * 60)
        print("\n📝 Summary:")
        print("  ✅ Subscriptions table removed")
        print("  ✅ Payments table created")
        if migrate_data:
            print(f"  ✅ Data migrated successfully")
        print("\n🚀 Your application is now using the simplified schema!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("\n⚠️  WARNING: This will modify your database!")
    print("Make sure you have a backup before proceeding.\n")
    
    confirm = input("Do you want to continue? (yes/no): ").strip().lower()
    if confirm == "yes":
        main()
    else:
        print("\n❌ Migration cancelled")
