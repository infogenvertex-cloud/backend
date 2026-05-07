#!/usr/bin/env python3
"""
Create test data for ExpiringSoon page testing
This script adds sample members with payments that expire at different times
"""

import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.member import Member
from app.models.payment import Payment

def create_expiring_test_data():
    """Create test members with payments expiring at different intervals"""
    
    db = SessionLocal()
    
    try:
        print("🔄 Creating test data for ExpiringSoon page...")
        
        # Test data for different expiry scenarios
        test_members = [
            {
                "member_id": "EXP001",
                "name": "John Urgent",
                "phone": "+1234567890",
                "payment_date": datetime.utcnow() - timedelta(days=29),  # Expires tomorrow (30-day plan)
                "plan": "1_month",
                "amount": 50.0
            },
            {
                "member_id": "EXP002", 
                "name": "Sarah Soon",
                "phone": "+1234567891",
                "payment_date": datetime.utcnow() - timedelta(days=26),  # Expires in 4 days
                "plan": "1_month",
                "amount": 50.0
            },
            {
                "member_id": "EXP003",
                "name": "Mike Upcoming",
                "phone": "+1234567892", 
                "payment_date": datetime.utcnow() - timedelta(days=23),  # Expires in 7 days
                "plan": "1_month",
                "amount": 50.0
            },
            {
                "member_id": "EXP004",
                "name": "Lisa Critical",
                "phone": "+1234567893",
                "payment_date": datetime.utcnow() - timedelta(days=30),  # Expires today!
                "plan": "1_month", 
                "amount": 50.0
            },
            {
                "member_id": "EXP005",
                "name": "Tom ThreeMonth",
                "phone": "+1234567894",
                "payment_date": datetime.utcnow() - timedelta(days=85),  # 3-month plan expiring in 5 days
                "plan": "3_month",
                "amount": 140.0
            }
        ]
        
        created_count = 0
        
        for member_data in test_members:
            # Check if member already exists
            existing_member = db.query(Member).filter(Member.member_id == member_data["member_id"]).first()
            
            if existing_member:
                print(f"⚠️  Member {member_data['member_id']} already exists, skipping...")
                continue
            
            # Create member
            member = Member(
                member_id=member_data["member_id"],
                name=member_data["name"],
                phone=member_data["phone"],
                join_date=datetime.utcnow().date()
            )
            
            db.add(member)
            db.flush()  # Get the member ID
            
            # Create payment
            payment = Payment(
                member_id=member.id,
                amount=member_data["amount"],
                payment_date=member_data["payment_date"],
                plan=member_data["plan"],
                notes=f"Test payment for {member_data['name']} - expires soon"
            )
            
            db.add(payment)
            created_count += 1
            
            # Calculate expiry date for display
            plan_days = {"1_month": 30, "3_month": 90, "6_month": 180, "12_month": 365}
            days = plan_days.get(member_data["plan"], 30)
            expiry_date = member_data["payment_date"] + timedelta(days=days)
            days_until_expiry = (expiry_date - datetime.utcnow()).days
            
            print(f"✅ Created: {member_data['name']} ({member_data['member_id']}) - Expires in {days_until_expiry} days")
        
        db.commit()
        
        print(f"\n🎉 Successfully created {created_count} test members with expiring subscriptions!")
        print("\n📋 Test Data Summary:")
        print("- EXP001 (John Urgent): Expires in 1 day - URGENT")
        print("- EXP002 (Sarah Soon): Expires in 4 days - SOON") 
        print("- EXP003 (Mike Upcoming): Expires in 7 days - UPCOMING")
        print("- EXP004 (Lisa Critical): Expires today - URGENT")
        print("- EXP005 (Tom ThreeMonth): 3-month plan expires in 5 days - SOON")
        print("\n🔗 Now visit: http://localhost:3000/expiring to test the ExpiringSoon page!")
        
    except Exception as e:
        print(f"❌ Error creating test data: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def cleanup_test_data():
    """Remove test data (optional cleanup function)"""
    
    db = SessionLocal()
    
    try:
        print("🧹 Cleaning up test data...")
        
        test_member_ids = ["EXP001", "EXP002", "EXP003", "EXP004", "EXP005"]
        
        for member_id in test_member_ids:
            member = db.query(Member).filter(Member.member_id == member_id).first()
            if member:
                # Delete payments first (due to foreign key)
                db.query(Payment).filter(Payment.member_id == member.id).delete()
                # Delete member
                db.delete(member)
                print(f"🗑️  Removed: {member_id}")
        
        db.commit()
        print("✅ Test data cleanup completed!")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage ExpiringSoon test data")
    parser.add_argument("--cleanup", action="store_true", help="Remove test data instead of creating it")
    
    args = parser.parse_args()
    
    if args.cleanup:
        cleanup_test_data()
    else:
        create_expiring_test_data()