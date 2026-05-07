"""
Quick database migration - Drop subscriptions, create payments table
"""

from sqlalchemy import text
from app.database import engine, SessionLocal, Base

def main():
    print("=" * 60)
    print("🔄 QUICK DATABASE MIGRATION")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Step 1: Drop subscriptions table
        print("\n🗑️  Dropping subscriptions table...")
        try:
            db.execute(text("DROP TABLE IF EXISTS subscriptions"))
            db.commit()
            print("✅ Subscriptions table dropped")
        except Exception as e:
            print(f"⚠️  Error dropping subscriptions: {e}")
            db.rollback()
        
        # Step 2: Create all tables (including payments)
        print("\n🔨 Creating/updating all tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created/updated")
        
        # Step 3: Verify tables
        print("\n🔍 Verifying tables...")
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE()
            ORDER BY table_name
        """))
        tables = [row[0] for row in result.fetchall()]
        
        print("\n📋 Current database tables:")
        for table in tables:
            icon = "✅" if table in ['members', 'payments', 'visitors', 'admins'] else "📄"
            print(f"  {icon} {table}")
        
        # Check payments table structure
        if 'payments' in tables:
            print("\n📊 Payments table structure:")
            result = db.execute(text("DESCRIBE payments"))
            for col in result.fetchall():
                print(f"  - {col[0]}: {col[1]}")
        
        print("\n" + "=" * 60)
        print("✅ MIGRATION COMPLETE!")
        print("=" * 60)
        print("\n📝 Changes:")
        print("  ❌ Removed: subscriptions table")
        print("  ✅ Added: payments table")
        print("\n🚀 Database is ready for the simplified application!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("\n⚠️  This will DROP the subscriptions table and all its data!")
    print("Make sure you have a backup if needed.\n")
    
    confirm = input("Continue? (yes/no): ").strip().lower()
    if confirm == "yes":
        main()
    else:
        print("\n❌ Migration cancelled")
