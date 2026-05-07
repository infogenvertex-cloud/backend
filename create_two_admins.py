#!/usr/bin/env python3
"""
Script to create 2 admin users for production use.
This will create admin accounts in the live database.
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.auth_service import register_admin
from app.models.admin import Admin

def create_production_admins():
    db: Session = SessionLocal()
    try:
        # Two admin credentials for production
        admin_users = [
            {
                "email": "admin@gym.com",
                "password": "Admin@2026!Secure",
                "name": "Primary Admin"
            },
            {
                "email": "manager@gym.com", 
                "password": "Manager@2026!Secure",
                "name": "Gym Manager"
            }
        ]
        
        created_count = 0
        
        print("=" * 60)
        print("🔧 Creating Production Admin Users")
        print("=" * 60)
        print()
        
        for user_data in admin_users:
            # Check if admin already exists
            existing_admin = db.query(Admin).filter(Admin.email == user_data["email"]).first()
            
            if existing_admin:
                print(f"⚠️  Admin already exists: {user_data['email']}")
                print(f"   Name: {existing_admin.name}")
                print(f"   Created: {existing_admin.created_at}")
                print()
                continue
            
            # Create new admin
            try:
                admin = register_admin(db, user_data["email"], user_data["password"], user_data["name"])
                print(f"✅ Successfully Created: {user_data['name']}")
                print(f"   📧 Email: {user_data['email']}")
                print(f"   🔑 Password: {user_data['password']}")
                print(f"   🆔 ID: {admin.id}")
                print()
                created_count += 1
            except Exception as e:
                print(f"❌ Failed to create {user_data['email']}: {e}")
                print()
        
        print("=" * 60)
        if created_count > 0:
            print(f"🚀 Successfully created {created_count} admin user(s)!")
        else:
            print("ℹ️  No new admin users were created (already exist)")
        print("=" * 60)
        
        # Display all credentials
        print("\n📋 Production Admin Credentials:")
        print("=" * 60)
        for user_data in admin_users:
            print(f"👤 {user_data['name']}")
            print(f"   📧 Email: {user_data['email']}")
            print(f"   🔑 Password: {user_data['password']}")
            print()
        
        print("=" * 60)
        print("⚠️  IMPORTANT SECURITY NOTES:")
        print("=" * 60)
        print("1. Save these credentials in a secure location")
        print("2. Change passwords after first login")
        print("3. Do not share credentials via insecure channels")
        print("4. Consider using a password manager")
        print("=" * 60)
        
        # Verify admins in database
        print("\n🔍 Verifying admins in database...")
        all_admins = db.query(Admin).all()
        print(f"Total admins in database: {len(all_admins)}")
        for admin in all_admins:
            print(f"  - {admin.name} ({admin.email})")
        
    except Exception as e:
        print(f"❌ Error creating admins: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("\n🚀 Starting admin creation process...")
    print("📡 Connecting to production database...\n")
    create_production_admins()
    print("\n✅ Process complete!\n")
