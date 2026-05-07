"""
Script to clear all data from the database while keeping table structure intact.
This will delete all records from all tables, making it ready for production use.
"""
import sys
from sqlalchemy import text
from app.database import SessionLocal, engine
from app.models import Member, Payment, Admin, Visitor

def clear_all_data():
    """Delete all records from all tables while preserving table structure"""
    db = SessionLocal()
    
    try:
        print("Starting database cleanup...")
        print("=" * 60)
        
        # Delete in order to respect foreign key constraints
        # Payments first (has foreign key to members)
        payment_count = db.query(Payment).count()
        db.query(Payment).delete()
        print(f"✓ Deleted {payment_count} payment records")
        
        # Members (has relationship with payments)
        member_count = db.query(Member).count()
        db.query(Member).delete()
        print(f"✓ Deleted {member_count} member records")
        
        # Visitors (independent table)
        visitor_count = db.query(Visitor).count()
        db.query(Visitor).delete()
        print(f"✓ Deleted {visitor_count} visitor records")
        
        # Admins (independent table)
        admin_count = db.query(Admin).count()
        db.query(Admin).delete()
        print(f"✓ Deleted {admin_count} admin records")
        
        # Commit all deletions
        db.commit()
        
        print("=" * 60)
        print("✓ Database cleanup completed successfully!")
        print("\nTotal records deleted:")
        print(f"  - Members: {member_count}")
        print(f"  - Payments: {payment_count}")
        print(f"  - Visitors: {visitor_count}")
        print(f"  - Admins: {admin_count}")
        print(f"  - TOTAL: {member_count + payment_count + visitor_count + admin_count}")
        
        # Verify tables are empty
        print("\n" + "=" * 60)
        print("Verifying tables are empty...")
        remaining_members = db.query(Member).count()
        remaining_payments = db.query(Payment).count()
        remaining_visitors = db.query(Visitor).count()
        remaining_admins = db.query(Admin).count()
        
        if remaining_members == 0 and remaining_payments == 0 and remaining_visitors == 0 and remaining_admins == 0:
            print("✓ All tables are empty!")
            print("\nDatabase is now ready for production use.")
            print("Table structure has been preserved.")
        else:
            print("⚠ Warning: Some records may still remain:")
            print(f"  - Members: {remaining_members}")
            print(f"  - Payments: {remaining_payments}")
            print(f"  - Visitors: {remaining_visitors}")
            print(f"  - Admins: {remaining_admins}")
            
        # Reset auto-increment counters (if using SQLite)
        try:
            with engine.connect() as conn:
                # Check if it's SQLite
                result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
                if result:
                    print("\n" + "=" * 60)
                    print("Resetting auto-increment counters (SQLite)...")
                    conn.execute(text("DELETE FROM sqlite_sequence WHERE name='members'"))
                    conn.execute(text("DELETE FROM sqlite_sequence WHERE name='payments'"))
                    conn.execute(text("DELETE FROM sqlite_sequence WHERE name='visitors'"))
                    conn.execute(text("DELETE FROM sqlite_sequence WHERE name='admins'"))
                    conn.commit()
                    print("✓ Auto-increment counters reset")
        except Exception as e:
            # Not SQLite or error resetting - that's okay
            print(f"\nNote: Could not reset auto-increment counters (may not be SQLite): {e}")
        
        print("\n" + "=" * 60)
        print("IMPORTANT: You may want to create a new admin user.")
        print("Run: python backend/create_admin.py")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Error clearing database: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    print("\n⚠️  WARNING: This will DELETE ALL DATA from the database!")
    print("Table structure will be preserved, but all records will be removed.")
    print("\nThis action cannot be undone.\n")
    
    response = input("Are you sure you want to continue? (yes/no): ").strip().lower()
    
    if response == "yes":
        clear_all_data()
    else:
        print("\nOperation cancelled. No data was deleted.")
        sys.exit(0)
