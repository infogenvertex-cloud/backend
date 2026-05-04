# 🔐 Admin Login Credentials

## Default Admin Accounts

These are the default admin accounts that should be created in your database:

### 1. Main Admin (Primary)
```
📧 Email: admin@gym.com
🔑 Password: admin123
👤 Name: Main Admin
```

### 2. Gym Manager
```
📧 Email: manager@gym.com
🔑 Password: manager123
👤 Name: Gym Manager
```

### 3. Staff Member
```
📧 Email: staff@gym.com
🔑 Password: staff123
👤 Name: Staff Member
```

### 4. Gym Owner
```
📧 Email: owner@gym.com
🔑 Password: owner123
👤 Name: Gym Owner
```

### 5. Supervisor
```
📧 Email: supervisor@gym.com
🔑 Password: super123
👤 Name: Supervisor
```

---

## 🚀 How to Create Admin Users

If these users don't exist in your database yet, you need to run the `create_admin.py` script:

### Option 1: Run Locally (Recommended)
```bash
cd backend
python create_admin.py
```

### Option 2: Create via API (if you have access)
You can also create an admin user by making a POST request to the registration endpoint (if it's exposed).

---

## 🧪 Testing Login

### Using the Frontend
1. Go to: https://frontend-three-swart-2tke12jw3z.vercel.app/login
2. Enter email: `admin@gym.com`
3. Enter password: `admin123`
4. Click Login

### Using cURL (API Test)
```bash
curl -X POST https://backend-gamma-seven-22.vercel.app/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@gym.com",
    "password": "admin123"
  }'
```

---

## ⚠️ Important Notes

1. **First Time Setup**: If this is your first deployment, you need to run `create_admin.py` to create these users in the database.

2. **Security**: These are default credentials. For production use, you should:
   - Change these passwords immediately after first login
   - Use strong, unique passwords
   - Consider implementing password reset functionality

3. **Database Connection**: Make sure your TiDB database is accessible and the credentials are correct.

---

## 🔧 Troubleshooting

### If login fails:

1. **Check if admin users exist**:
   - Run `create_admin.py` locally to create the users
   - Or check your database directly

2. **Verify backend is running**:
   - Visit: https://backend-gamma-seven-22.vercel.app/
   - Should return: `{"status":"ok",...}`

3. **Check database connection**:
   - Visit: https://backend-gamma-seven-22.vercel.app/health
   - Should show database status

4. **Check frontend API URL**:
   - Make sure frontend `.env` has: `VITE_API_URL=https://backend-gamma-seven-22.vercel.app`

---

## 📝 Quick Start

**Recommended first login:**
```
Email: admin@gym.com
Password: admin123
```

This is the main admin account with full access to all features.

---

**Last Updated**: May 4, 2026
