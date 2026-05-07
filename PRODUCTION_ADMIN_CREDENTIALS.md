# 🔐 Production Admin Credentials

## ✅ Admin Users Created Successfully

Two admin users have been created in the **live production database** (TiDB Cloud).

---

## 👥 Admin Accounts

### 1. Primary Admin
- **Name**: Primary Admin
- **Email**: `admin@gym.com`
- **Password**: `Admin@2026!Secure`
- **ID**: 30001
- **Role**: Full administrative access

### 2. Gym Manager
- **Name**: Gym Manager
- **Email**: `manager@gym.com`
- **Password**: `Manager@2026!Secure`
- **ID**: 30002
- **Role**: Management access

---

## 🔗 Login URL

**Frontend Application**: Use your deployed frontend URL or local development URL
- Production: `https://your-frontend-url.vercel.app/login`
- Local: `http://localhost:5173/login`

---

## 🚀 How to Login

1. Navigate to the login page
2. Enter one of the email addresses above
3. Enter the corresponding password
4. Click "Login"

---

## ⚠️ IMPORTANT SECURITY NOTES

### Immediate Actions Required:
1. ✅ **Save these credentials** in a secure password manager
2. ✅ **Change passwords** after first login (recommended)
3. ✅ **Delete this file** after saving credentials securely
4. ✅ **Do not commit** this file to version control

### Security Best Practices:
- 🔒 Never share credentials via email or chat
- 🔒 Use strong, unique passwords
- 🔒 Enable two-factor authentication (if available)
- 🔒 Regularly update passwords
- 🔒 Monitor login activity
- 🔒 Limit admin access to trusted personnel only

---

## 📊 Database Status

- **Database**: TiDB Cloud (Production)
- **Total Admins**: 2
- **Status**: ✅ Active and verified
- **Connection**: ✅ Successful

---

## 🔄 Password Change Instructions

To change passwords after first login:
1. Log in with the credentials above
2. Navigate to account settings (if available)
3. Update password to a new secure password
4. Save changes

---

## 🛠️ Troubleshooting

### Cannot Login?
1. Verify you're using the correct email and password
2. Check that the backend API is running
3. Verify database connection
4. Check browser console for errors

### Forgot Password?
Currently, there's no "forgot password" feature. You can:
1. Create a new admin using `python create_two_admins.py`
2. Or manually reset password in the database

### Need More Admins?
Run the script again or modify it to add more users:
```bash
cd backend
python create_two_admins.py
```

---

## 📝 Notes

- These credentials are for **production use**
- Passwords follow security best practices (uppercase, lowercase, numbers, special characters)
- Admin IDs start at 30001 (TiDB auto-increment)
- All admins have full access to the system

---

## 🗑️ After Saving Credentials

**IMPORTANT**: Once you've saved these credentials securely:

1. Delete this file:
   ```bash
   rm backend/PRODUCTION_ADMIN_CREDENTIALS.md
   ```

2. Or add it to `.gitignore` to prevent accidental commits

3. Never commit credentials to version control

---

## ✅ Verification Checklist

- [x] 2 admin users created
- [x] Credentials documented
- [x] Database connection verified
- [x] Admins verified in database
- [ ] Credentials saved in password manager
- [ ] This file deleted or secured
- [ ] First login successful
- [ ] Passwords changed (recommended)

---

**Created**: May 6, 2026  
**Database**: TiDB Cloud Production  
**Status**: ✅ Ready for use
