"""
Script to add payment columns to subscriptions table in TiDB.
This adds amount, payment_date, and invoice_url columns.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

# Load environment variables
load_dotenv()

def add_payment_columns():
    # Construct database URL from components
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_database = os.getenv("DB_DATABASE")
    
    if not all([db_host, db_port, db_username, db_password, db_database]):
        print("❌ Database configuration not found in environment variables")
        return
    
    database_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}?ssl_ca=&ssl_verify_cert=true&ssl_verify_identity=true"
    
    print(f"Connecting to TiDB database...")
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        print("\n=== Checking existing columns ===")
        
        # Check current columns
        result = conn.execute(text("DESCRIBE subscriptions"))
        existing_columns = [row[0] for row in result]
        print(f"Existing columns: {existing_columns}")
        
        columns_to_add = []
        if 'amount' not in existing_columns:
            columns_to_add.append(('amount', 'FLOAT'))
        if 'payment_date' not in existing_columns:
            columns_to_add.append(('payment_date', 'DATETIME'))
        if 'invoice_url' not in existing_columns:
            columns_to_add.append(('invoice_url', 'VARCHAR(255)'))
        
        if not columns_to_add:
            print("\n✅ All payment columns already exist!")
            return
        
        print(f"\n=== Adding {len(columns_to_add)} columns ===")
        
        for column_name, column_type in columns_to_add:
            try:
                print(f"Adding '{column_name}' column ({column_type})...")
                conn.execute(text(f"ALTER TABLE subscriptions ADD COLUMN {column_name} {column_type}"))
                conn.commit()
                print(f"✅ Column '{column_name}' added successfully")
            except Exception as e:
                print(f"❌ Error adding column '{column_name}': {e}")
        
        print("\n=== Verifying columns ===")
        result = conn.execute(text("DESCRIBE subscriptions"))
        print("\nColumn Name       | Type          | Null | Key | Default")
        print("-" * 70)
        for row in result:
            print(f"{row[0]:17s} | {row[1]:13s} | {row[2]:4s} | {row[3]:3s} | {str(row[4])}")
        
        print("\n✅ Migration completed successfully!")

if __name__ == "__main__":
    print("=" * 60)
    print("ADD PAYMENT COLUMNS TO SUBSCRIPTIONS TABLE (TIDB)")
    print("=" * 60)
    print("\nThis will add the following columns to subscriptions table:")
    print("  - amount (FLOAT)")
    print("  - payment_date (DATETIME)")
    print("  - invoice_url (VARCHAR(255))")
    print("=" * 60)
    
    response = input("\nDo you want to continue? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        add_payment_columns()
    else:
        print("\n❌ Operation cancelled.")
