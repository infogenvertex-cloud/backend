#!/usr/bin/env python3
"""
Test script to verify member join_date update functionality
"""

import sys
import os
from datetime import datetime, date

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.member import Member
from app.schemas.member import MemberUpdate
from app.services.member_service import update_member

def test_member_update():
    """Test member join_date update functionality"""
    
    db = SessionLocal()
    
    try:
        print("🧪 Testing Member Update Functionality")
        
        # Find an existing member
        member = db.query(Member).first()
        if not member:
            print("❌ No members found in database")
            return
        
        print(f"👤 Testing with member: {member.member_id} ({member.name})")
        print(f"📅 Current join_date: {member.join_date}")
        
        # Test updating join_date
        new_join_date = date(2024, 1, 15)  # Set a specific test date
        update_data = MemberUpdate(join_date=new_join_date)
        
        print(f"🔄 Updating join_date to: {new_join_date}")
        print(f"📋 Update data: {update_data}")
        print(f"🔍 Update data dict: {update_data.model_dump()}")
        
        # Perform the update
        updated_member = update_member(db, member.id, update_data)
        
        print(f"✅ Update completed!")
        print(f"📅 New join_date: {updated_member.join_date}")
        print(f"🔍 Member object: {updated_member.__dict__}")
        
        # Verify the update in database
        db.refresh(updated_member)
        fresh_member = db.query(Member).filter(Member.id == member.id).first()
        print(f"🔍 Fresh from DB: {fresh_member.join_date}")
        
        if fresh_member.join_date == new_join_date:
            print("✅ SUCCESS: Join date updated correctly in database!")
        else:
            print(f"❌ FAILED: Expected {new_join_date}, got {fresh_member.join_date}")
        
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_member_update()