#!/usr/bin/env python3
"""
Script to create a default admin user for the gym management system.
Run this script to create your first admin account.
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.auth_service import register_admin

def create_admin_users():
    db: Session = SessionLocal()
    try:
        # Multiple admin credentials
        admin_users = [
            {
                "email": "admin@gym.com",
                "password": "admin123",
                "name": "Main Admin"
            },
            {
                "email": "manager@gym.com", 
                "password": "manager123",
                "name": "Gym Manager"
            },
            {
                "email": "staff@gym.com",
                "password": "staff123", 
                "name": "Staff Member"
            },
            {
                "email": "owner@gym.com",
                "password": "owner123",
                "name": "Gym Owner"
            },
            {
                "email": "supervisor@gym.com",
                "password": "super123",
                "name": "Supervisor"
            }
        ]
        
        from app.models.admin import Admin
        created_count = 0
        
        print("🔧 Creating admin users...\n")
        
        for user_data in admin_users:
            # Check if admin already exists
            existing_admin = db.query(Admin).filter(Admin.email == user_data["email"]).first()
            
            if existing_admin:
                print(f"⚠️  Admin already exists: {user_data['email']}")
                continue
            
            # Create new admin
            try:
                admin = register_admin(db, user_data["email"], user_data["password"], user_data["name"])
                print(f"✅ Created: {user_data['name']}")
                print(f"   📧 Email: {user_data['email']}")
                print(f"   🔑 Password: {user_data['password']}")
                print()
                created_count += 1
            except Exception as e:
                print(f"❌ Failed to create {user_data['email']}: {e}")
        
        print(f"🚀 Successfully created {created_count} admin users!")
        print("\n📋 All Admin Credentials:")
        print("=" * 50)
        for user_data in admin_users:
            print(f"👤 {user_data['name']}")
            print(f"   📧 {user_data['email']}")
            print(f"   🔑 {user_data['password']}")
            print()
        
    except Exception as e:
        print(f"❌ Error creating admins: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_users()