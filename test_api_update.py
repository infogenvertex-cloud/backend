#!/usr/bin/env python3
"""
Test the member update API endpoint directly
"""

import requests
import json
from datetime import date

def test_member_update_api():
    """Test the member update API endpoint"""
    
    base_url = "http://localhost:8000"
    
    # First, login to get a token
    login_data = {
        "email": "admin@gym.com",
        "password": "admin123"
    }
    
    print("🔐 Logging in...")
    login_response = requests.post(f"{base_url}/auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("✅ Login successful!")
    
    # Get the first member
    print("👤 Getting member list...")
    members_response = requests.get(f"{base_url}/members/?page=1&page_size=1", headers=headers)
    
    if members_response.status_code != 200:
        print(f"❌ Failed to get members: {members_response.status_code}")
        return
    
    members_data = members_response.json()
    if not members_data["items"]:
        print("❌ No members found")
        return
    
    member = members_data["items"][0]
    member_id = member["id"]
    
    print(f"👤 Testing with member: {member['member_id']} ({member['name']})")
    print(f"📅 Current join_date: {member['join_date']}")
    
    # Update the member's join_date
    update_data = {
        "name": member["name"],
        "phone": member["phone"],
        "join_date": "2024-02-20"  # New test date
    }
    
    print(f"🔄 Updating member with data: {update_data}")
    
    update_response = requests.put(
        f"{base_url}/members/{member_id}", 
        json=update_data, 
        headers=headers
    )
    
    print(f"📤 API Response Status: {update_response.status_code}")
    print(f"📥 API Response: {update_response.text}")
    
    if update_response.status_code == 200:
        updated_member = update_response.json()
        print(f"✅ Update successful!")
        print(f"📅 New join_date: {updated_member['join_date']}")
        
        if updated_member['join_date'] == "2024-02-20":
            print("🎉 SUCCESS: Join date updated correctly via API!")
        else:
            print(f"❌ FAILED: Expected 2024-02-20, got {updated_member['join_date']}")
    else:
        print(f"❌ Update failed: {update_response.status_code}")
        print(f"Error: {update_response.text}")

if __name__ == "__main__":
    test_member_update_api()