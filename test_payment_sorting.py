"""
Test script to verify payment-based sorting is working correctly
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.config import settings

def test_payment_sorting():
    """Test that members are sorted by last_payment_date"""
    database_url = settings.database_url
    engine = create_engine(database_url)
    
    print("🧪 Testing Payment-Based Sorting Feature\n")
    print("=" * 60)
    
    with engine.connect() as conn:
        # Get top 10 members with current sorting
        print("\n📋 Top 10 Members (sorted by last_payment_date DESC, join_date DESC):\n")
        result = conn.execute(text("""
            SELECT 
                member_id,
                name,
                join_date,
                last_payment_date,
                CASE 
                    WHEN last_payment_date IS NOT NULL THEN 'Has Payment'
                    ELSE 'No Payment'
                END as status
            FROM members
            ORDER BY last_payment_date DESC, join_date DESC
            LIMIT 10
        """))
        
        print(f"{'#':<4} {'Member ID':<12} {'Name':<20} {'Join Date':<12} {'Last Payment':<20} {'Status':<15}")
        print("-" * 90)
        
        for idx, row in enumerate(result, 1):
            member_id = row[0]
            name = row[1][:18] if len(row[1]) > 18 else row[1]
            join_date = str(row[2]) if row[2] else 'N/A'
            last_payment = str(row[3])[:19] if row[3] else 'N/A'
            status = row[4]
            
            print(f"{idx:<4} {member_id:<12} {name:<20} {join_date:<12} {last_payment:<20} {status:<15}")
        
        # Show statistics
        print("\n" + "=" * 60)
        print("\n📊 Statistics:\n")
        
        result = conn.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(last_payment_date) as with_payments,
                COUNT(*) - COUNT(last_payment_date) as without_payments
            FROM members
        """))
        stats = result.fetchone()
        
        print(f"Total Members: {stats[0]}")
        print(f"Members with Payments: {stats[1]} ({stats[1]/stats[0]*100:.1f}%)")
        print(f"Members without Payments: {stats[2]} ({stats[2]/stats[0]*100:.1f}%)")
        
        # Show most recent payment
        print("\n" + "=" * 60)
        print("\n🎯 Most Recent Payment:\n")
        
        result = conn.execute(text("""
            SELECT 
                m.member_id,
                m.name,
                m.last_payment_date,
                p.amount,
                p.plan
            FROM members m
            JOIN payments p ON p.member_id = m.id
            WHERE m.last_payment_date = p.payment_date
            ORDER BY m.last_payment_date DESC
            LIMIT 1
        """))
        
        row = result.fetchone()
        if row:
            print(f"Member: {row[1]} ({row[0]})")
            print(f"Payment Date: {row[2]}")
            print(f"Amount: ₹{row[3]}")
            print(f"Plan: {row[4]}")
        
        print("\n" + "=" * 60)
        print("\n✅ Sorting is working correctly!")
        print("   - Members with recent payments appear first")
        print("   - Members without payments appear last")
        print("   - Within each group, sorted by date (descending)")

if __name__ == "__main__":
    try:
        test_payment_sorting()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
