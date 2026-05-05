"""
Check subscriptions data in the database.
"""

from sqlalchemy import text
from app.database import engine

def check_subscriptions():
    """Check subscriptions data."""
    try:
        with engine.connect() as conn:
            print("📊 Checking subscriptions data...\n")
            
            # Get all subscriptions
            query = text("""
                SELECT 
                    s.id, 
                    s.member_id, 
                    m.member_id as member_code,
                    m.name as member_name,
                    s.plan, 
                    s.amount, 
                    s.payment_date, 
                    s.status
                FROM subscriptions s
                LEFT JOIN members m ON s.member_id = m.id
                ORDER BY s.id DESC
                LIMIT 20
            """)
            result = conn.execute(query)
            
            print("ID   | Member ID | Member Code | Member Name      | Plan      | Amount    | Payment Date        | Status")
            print("-" * 120)
            
            for row in result:
                sub_id = row[0]
                member_id = row[1]
                member_code = row[2] or "NULL"
                member_name = row[3] or "NULL"
                plan = row[4]
                amount = f"Rs. {row[5]:.2f}" if row[5] is not None else "NULL"
                payment_date = str(row[6]) if row[6] else "NULL"
                status = row[7]
                
                print(f"{sub_id:4} | {member_id:9} | {member_code:11} | {member_name:16} | {plan:9} | {amount:9} | {payment_date:19} | {status}")
            
            # Count by member
            print("\n\n📊 Subscriptions count by member:")
            count_query = text("""
                SELECT 
                    m.member_id,
                    m.name,
                    COUNT(s.id) as sub_count
                FROM members m
                LEFT JOIN subscriptions s ON m.id = s.member_id
                GROUP BY m.id, m.member_id, m.name
                ORDER BY sub_count DESC
            """)
            result = conn.execute(count_query)
            
            print("\nMember Code | Member Name      | Subscription Count")
            print("-" * 60)
            for row in result:
                print(f"{row[0]:11} | {row[1]:16} | {row[2]}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    check_subscriptions()
