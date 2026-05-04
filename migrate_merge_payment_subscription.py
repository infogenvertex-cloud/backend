"""
Migration script to merge Payment table into Subscription table.
This adds payment fields (amount, payment_date, invoice_url) to subscriptions table.

Run this script ONCE to migrate your database schema.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

def migrate():
    # Get database URL from environment or use SQLite default
    database_url = os.getenv("DATABASE_URL", "sqlite:///./gym.db")
    print(f"Using database: {database_url}")
    
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        print("Starting migration: Merging Payment into Subscription...")
        
        # Add new columns to subscriptions table
        try:
            print("Adding 'amount' column...")
            conn.execute(text("ALTER TABLE subscriptions ADD COLUMN amount FLOAT"))
            conn.commit()
        except Exception as e:
            print(f"Column 'amount' might already exist: {e}")
        
        try:
            print("Adding 'payment_date' column...")
            conn.execute(text("ALTER TABLE subscriptions ADD COLUMN payment_date DATETIME"))
            conn.commit()
        except Exception as e:
            print(f"Column 'payment_date' might already exist: {e}")
        
        try:
            print("Adding 'invoice_url' column...")
            conn.execute(text("ALTER TABLE subscriptions ADD COLUMN invoice_url VARCHAR(255)"))
            conn.commit()
        except Exception as e:
            print(f"Column 'invoice_url' might already exist: {e}")
        
        print("\n✅ Migration completed successfully!")
        print("\nNOTE: Old 'payments' table still exists for reference.")
        print("You can manually drop it later if needed: DROP TABLE payments;")
        print("\nIMPORTANT: Restart your backend server for changes to take effect.")

if __name__ == "__main__":
    migrate()
