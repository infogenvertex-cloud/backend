"""
Fix ALL subscriptions with NULL or 0.0 amount values.
Sets proper default amounts based on subscription plan.

Usage:
    python fix_all_null_amounts.py
"""

from sqlalchemy import text
from app.database import engine

# Default amounts per plan (you can adjust these)
PLAN_AMOUNTS = {
    "1_month": 500.0,
    "3_month": 1400.0,
    "6_month": 2700.0,
    "12_month": 5000.0,
}

def fix_all_null_amounts():
    """Update all subscriptions with NULL or 0.0 amount to proper values."""
    try:
        with engine.connect() as conn:
            # Check how many subscriptions need fixing
            check_query = text("""
                SELECT COUNT(*) as count
                FROM subscriptions
                WHERE amount IS NULL OR amount = 0.0
            """)
            result = conn.execute(check_query)
            row = result.fetchone()
            null_count = row[0] if row else 0
            
            if null_count > 0:
                print(f"✓ Found {null_count} subscriptions with NULL or 0.0 amount")
                
                # Update each plan type with appropriate amount
                total_updated = 0
                for plan, amount in PLAN_AMOUNTS.items():
                    update_query = text(f"""
                        UPDATE subscriptions
                        SET amount = :amount
                        WHERE (amount IS NULL OR amount = 0.0) AND plan = :plan
                    """)
                    result = conn.execute(update_query, {"amount": amount, "plan": plan})
                    updated = result.rowcount
                    if updated > 0:
                        print(f"  ✓ Updated {updated} subscriptions with plan '{plan}' to Rs. {amount}")
                        total_updated += updated
                
                conn.commit()
                print(f"\n✅ Successfully updated {total_updated} subscriptions with proper amounts")
            else:
                print("ℹ️  All subscriptions already have valid amount values")
            
            # Show summary
            print("\n📊 Current subscription amounts:")
            summary_query = text("""
                SELECT plan, COUNT(*) as count, MIN(amount) as min_amt, MAX(amount) as max_amt
                FROM subscriptions
                GROUP BY plan
                ORDER BY plan
            """)
            result = conn.execute(summary_query)
            print("\nPlan       | Count | Min Amount | Max Amount")
            print("-" * 50)
            for row in result:
                print(f"{row[0]:10} | {row[1]:5} | Rs. {row[2] or 0:7.2f} | Rs. {row[3] or 0:7.2f}")
                
    except Exception as e:
        print(f"❌ Error updating subscriptions: {e}")
        raise

if __name__ == "__main__":
    print("🔄 Starting migration to fix all NULL/0.0 amounts...")
    fix_all_null_amounts()
    print("\n✅ Migration completed successfully!")
    print("\n💡 Tip: Restart your backend server to see the changes.")

