"""
Script to check the current database structure.
Shows all tables and their columns.

Usage:
    python check_database_structure.py
"""

from sqlalchemy import text
from app.database import engine

def check_database_structure():
    """Check and display current database structure."""
    try:
        with engine.connect() as conn:
            print("=" * 80)
            print("DATABASE STRUCTURE CHECK")
            print("=" * 80)
            
            # Get all tables
            tables_query = text("""
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                ORDER BY TABLE_NAME
            """)
            tables_result = conn.execute(tables_query)
            tables = [row[0] for row in tables_result]
            
            print(f"\n📊 Total Tables: {len(tables)}")
            print("-" * 80)
            
            for table_name in tables:
                print(f"\n✓ Table: {table_name}")
                print("-" * 80)
                
                # Get columns for this table
                columns_query = text(f"""
                    SELECT 
                        COLUMN_NAME,
                        DATA_TYPE,
                        IS_NULLABLE,
                        COLUMN_KEY,
                        COLUMN_DEFAULT
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE()
                    AND TABLE_NAME = '{table_name}'
                    ORDER BY ORDINAL_POSITION
                """)
                columns_result = conn.execute(columns_query)
                
                print(f"{'Column':<20} {'Type':<15} {'Nullable':<10} {'Key':<10} {'Default':<15}")
                print("-" * 80)
                
                for col in columns_result:
                    col_name, data_type, nullable, key, default = col
                    default_str = str(default) if default else ""
                    print(f"{col_name:<20} {data_type:<15} {nullable:<10} {key:<10} {default_str:<15}")
            
            print("\n" + "=" * 80)
            print("DATABASE CHECK COMPLETE")
            print("=" * 80)
            
            # Check for any orphaned tables
            expected_tables = ['members', 'subscriptions', 'visitors', 'admins']
            unexpected_tables = [t for t in tables if t not in expected_tables]
            
            if unexpected_tables:
                print(f"\n⚠️  UNEXPECTED TABLES FOUND: {', '.join(unexpected_tables)}")
                print("These tables may need to be cleaned up.")
            else:
                print("\n✅ All tables are expected and clean!")
                
    except Exception as e:
        print(f"❌ Error checking database structure: {e}")
        raise

if __name__ == "__main__":
    check_database_structure()
