# Database Cleanup Guide

## Overview
This guide explains how to clear all data from the database while preserving the table structure, making it ready for production use.

## What This Does
- ✅ Deletes all records from all tables (Members, Payments, Visitors, Admins)
- ✅ Preserves table structure and schema
- ✅ Respects foreign key constraints (deletes in correct order)
- ✅ Resets auto-increment counters (for SQLite)
- ✅ Verifies all tables are empty after cleanup

## What This Does NOT Do
- ❌ Does not drop tables
- ❌ Does not modify table structure
- ❌ Does not delete the database file itself

## Usage

### Step 1: Run the Cleanup Script

```bash
cd backend
python clear_all_data.py
```

### Step 2: Confirm the Action
The script will ask for confirmation:
```
⚠️  WARNING: This will DELETE ALL DATA from the database!
Table structure will be preserved, but all records will be removed.

This action cannot be undone.

Are you sure you want to continue? (yes/no):
```

Type `yes` to proceed or `no` to cancel.

### Step 3: Review the Output
The script will show:
- Number of records deleted from each table
- Verification that all tables are empty
- Status of auto-increment counter reset

Example output:
```
Starting database cleanup...
============================================================
✓ Deleted 15 payment records
✓ Deleted 10 member records
✓ Deleted 5 visitor records
✓ Deleted 1 admin records
============================================================
✓ Database cleanup completed successfully!

Total records deleted:
  - Members: 10
  - Payments: 15
  - Visitors: 5
  - Admins: 1
  - TOTAL: 31

============================================================
Verifying tables are empty...
✓ All tables are empty!

Database is now ready for production use.
Table structure has been preserved.
```

### Step 4: Create a New Admin User
After clearing the database, you'll need to create a new admin user:

```bash
python create_admin.py
```

Follow the prompts to create your admin account.

## Important Notes

### ⚠️ Before Running in Production
1. **Backup your data** if you need to keep any records
2. Make sure you're connected to the correct database
3. Verify the database URL in your `.env` file
4. Consider exporting important data before cleanup

### Database Types
This script works with:
- ✅ SQLite (local development)
- ✅ TiDB (production)
- ✅ MySQL/PostgreSQL (if configured)

### Foreign Key Constraints
The script deletes records in the correct order:
1. Payments (has foreign key to Members)
2. Members (parent table)
3. Visitors (independent)
4. Admins (independent)

### Auto-Increment Reset
- For SQLite: Auto-increment counters are reset automatically
- For TiDB/MySQL: Auto-increment continues from last value (this is normal)
- For PostgreSQL: Sequences continue from last value (this is normal)

## Troubleshooting

### Error: "Database connection failed"
- Check your `.env` file for correct database credentials
- Verify the database server is running
- Test connection with `python test_tidb_connection.py`

### Error: "Foreign key constraint failed"
- The script handles this automatically by deleting in correct order
- If you still see this error, there may be additional relationships

### Some Records Remain
- Check for any custom tables not included in the script
- Verify foreign key constraints are properly defined
- Run the script again

## Alternative: Manual Cleanup

If you prefer to clear data manually:

```sql
-- Delete in this order to respect foreign keys
DELETE FROM payments;
DELETE FROM members;
DELETE FROM visitors;
DELETE FROM admins;

-- For SQLite, reset auto-increment
DELETE FROM sqlite_sequence WHERE name IN ('members', 'payments', 'visitors', 'admins');
```

## After Cleanup

Your database is now in a clean state with:
- ✅ All tables present and properly structured
- ✅ No data records
- ✅ Ready for production use
- ✅ Auto-increment counters reset (SQLite)

Remember to:
1. Create a new admin user
2. Test the application
3. Verify all features work correctly
4. Begin adding production data

## Safety Features

The script includes several safety features:
- Confirmation prompt before deletion
- Transaction rollback on error
- Verification of empty tables
- Detailed logging of all operations
- Error handling and reporting

## Need Help?

If you encounter issues:
1. Check the error message carefully
2. Verify database connection
3. Review the `.env` configuration
4. Check database logs
5. Ensure you have proper permissions
