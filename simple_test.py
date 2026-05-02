#!/usr/bin/env python3
"""
Simple TiDB connection test with SSL
"""

import pymysql
import os

print("🔍 Testing TiDB Connection with SSL...")
print()

# Connection parameters
config = {
    'host': 'gateway01.ap-northeast-1.prod.aws.tidbcloud.com',
    'port': 4000,
    'user': 'CrR1v2rQYoMqsCW.root',
    'password': 'lku1aT2R5cLrfFeS',
    'database': 'test',  # Use default 'test' database
    'ssl': {
        'ca': 'isrgrootx1.pem'
    }
}

print(f"📍 Host: {config['host']}")
print(f"🔌 Port: {config['port']}")
print(f"👤 User: {config['user']}")
print(f"📊 Database: {config['database']}")
print(f"🔒 SSL CA: {config['ssl']['ca']}")
print()

# Check if certificate exists
if not os.path.exists(config['ssl']['ca']):
    print(f"❌ Certificate file not found: {config['ssl']['ca']}")
    print("💡 Make sure 'isrgrootx1.pem' is in the backend directory")
    exit(1)

try:
    print("⏳ Attempting SSL connection...")
    
    connection = pymysql.connect(**config)
    
    print("✅ Connection successful!")
    print()
    
    with connection.cursor() as cursor:
        # Test query
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"📌 TiDB Version: {version[0]}")
        
        # Show databases
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print(f"📌 Available databases:")
        for db in databases:
            print(f"   - {db[0]}")
            
        # Check if gym_db exists
        cursor.execute("SHOW DATABASES LIKE 'gym_db'")
        gym_db = cursor.fetchone()
        
        print()
        if gym_db:
            print("✅ Database 'gym_db' exists!")
        else:
            print("⚠️  Database 'gym_db' does not exist")
            print("💡 Creating 'gym_db' database...")
            cursor.execute("CREATE DATABASE gym_db")
            print("✅ Database 'gym_db' created successfully!")
    
    connection.close()
    print()
    print("🎉 Test completed successfully!")
    print()
    print("✅ Your TiDB cluster is active and accessible!")
    print("✅ SSL connection working!")
    print("✅ Ready to use with your application!")
    
except pymysql.err.OperationalError as e:
    print(f"❌ Connection failed: {e}")
    print()
    print("🔧 Possible reasons:")
    print("1. TiDB cluster is paused - Go to TiDB Cloud and resume it")
    print("2. Network/Firewall blocking the connection")
    print("3. Incorrect credentials")
    print("4. SSL certificate issue")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
