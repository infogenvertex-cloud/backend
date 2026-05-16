"""
Migration script to add last_payment_date column to members table
and populate it with the most recent payment date for each member.
"""
import sys
import os

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.config import settings

def add_last_payment_date_column():
    """Add last_payment_date column and populate it"""
    database_url = settings.database_url
    
    print(f"🔗 Connecting to database...")
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        # Check if column already exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='members' AND column_name='last_payment_date'
        """))
        
        if result.fetchone():
            print("✅ Column 'last_payment_date' already exists")
        else:
            # Add the column
            print("📝 Adding 'last_payment_date' column to members table...")
            conn.execute(text("""
                ALTER TABLE members 
                ADD COLUMN last_payment_date TIMESTAMP NULL
            """))
            conn.commit()
            print("✅ Column added successfully")
        
        # Create index for better query performance
        print("📝 Creating index on last_payment_date...")
        try:
            conn.execute(text("""
                CREATE INDEX idx_members_last_payment_date 
                ON members(last_payment_date DESC)
            """))
            conn.commit()
            print("✅ Index created successfully")
        except Exception as e:
            print(f"⚠️ Index creation skipped (may already exist): {e}")
        
        # Populate last_payment_date with the most recent payment for each member
        print("📝 Populating last_payment_date from existing payments...")
        conn.execute(text("""
            UPDATE members m
            SET last_payment_date = (
                SELECT MAX(p.payment_date)
                FROM payments p
                WHERE p.member_id = m.id
            )
            WHERE EXISTS (
                SELECT 1 FROM payments p WHERE p.member_id = m.id
            )
        """))
        conn.commit()
        
        # Show results
        result = conn.execute(text("""
            SELECT 
                COUNT(*) as total_members,
                COUNT(last_payment_date) as members_with_payments,
                COUNT(*) - COUNT(last_payment_date) as members_without_payments
            FROM members
        """))
        stats = result.fetchone()
        
        print("\n✅ Migration completed successfully!")
        print(f"📊 Total members: {stats[0]}")
        print(f"💰 Members with payments: {stats[1]}")
        print(f"📝 Members without payments: {stats[2]}")
        
        # Show sample of updated data
        print("\n📋 Sample of members with last_payment_date:")
        result = conn.execute(text("""
            SELECT member_id, name, last_payment_date
            FROM members
            WHERE last_payment_date IS NOT NULL
            ORDER BY last_payment_date DESC
            LIMIT 5
        """))
        
        for row in result:
            print(f"  {row[0]} - {row[1]}: {row[2]}")

if __name__ == "__main__":
    print("🚀 Starting migration to add last_payment_date column...")
    try:
        add_last_payment_date_column()
        print("\n✨ All done!")
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
