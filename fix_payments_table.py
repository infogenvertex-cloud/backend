"""
Fix payments table structure - remove invoice_url, add plan and notes columns
"""

from sqlalchemy import text
from app.database import SessionLocal

def main():
    print("=" * 60)
    print("🔧 FIXING PAYMENTS TABLE STRUCTURE")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Check current structure
        print("\n📊 Current payments table structure:")
        result = db.execute(text("DESCRIBE payments"))
        columns = {col[0]: col[1] for col in result.fetchall()}
        for col_name, col_type in columns.items():
            print(f"  - {col_name}: {col_type}")
        
        # Remove invoice_url if exists
        if 'invoice_url' in columns:
            print("\n🗑️  Removing invoice_url column...")
            db.execute(text("ALTER TABLE payments DROP COLUMN invoice_url"))
            db.commit()
            print("✅ invoice_url column removed")
        
        # Add plan column if not exists
        if 'plan' not in columns:
            print("\n➕ Adding plan column...")
            db.execute(text("ALTER TABLE payments ADD COLUMN plan VARCHAR(50) NOT NULL DEFAULT '1_month'"))
            db.commit()
            print("✅ plan column added")
        
        # Add notes column if not exists
        if 'notes' not in columns:
            print("\n➕ Adding notes column...")
            db.execute(text("ALTER TABLE payments ADD COLUMN notes VARCHAR(200) NULL"))
            db.commit()
            print("✅ notes column added")
        
        # Verify final structure
        print("\n📊 Updated payments table structure:")
        result = db.execute(text("DESCRIBE payments"))
        for col in result.fetchall():
            print(f"  ✅ {col[0]}: {col[1]}")
        
        print("\n" + "=" * 60)
        print("✅ PAYMENTS TABLE FIXED!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
