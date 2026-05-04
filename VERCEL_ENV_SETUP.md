# Vercel Environment Variables Setup Guide

## Your Environment Variables to Add:

Copy and paste these values into Vercel Dashboard:

### Database Configuration
```
DB_HOST = gateway01.ap-northeast-1.prod.aws.tidbcloud.com
DB_PORT = 4000
DB_USERNAME = CrR1v2rQYoMqsCW.root
DB_PASSWORD = lku1aT2R5cLrfFeS
DB_DATABASE = gym_db
```

### JWT Configuration
```
JWT_SECRET_KEY = gym-management-production-secret-key-2024
JWT_ALGORITHM = HS256
JWT_EXPIRY_MINUTES = 1440
```

### URL Configuration
```
BASE_URL = https://backend-git-master-noreplynexora-9184s-projects.vercel.app
FRONTEND_URL = https://frontend-three-swart-21e12w3z.vercel.app
```

---

## Step-by-Step Instructions:

### 1. Open Vercel Dashboard
- Go to: https://vercel.com/dashboard
- Login if needed

### 2. Select Your Backend Project
- Find and click on your backend project
- (It should be named something like "backend" or show the GitHub repo name)

### 3. Go to Settings
- Click the **"Settings"** tab at the top of the page

### 4. Navigate to Environment Variables
- In the left sidebar, click **"Environment Variables"**

### 5. Add Each Variable
For each variable listed above:

1. Click the **"Add New"** button
2. Enter the **Name** (e.g., `DB_HOST`)
3. Enter the **Value** (e.g., `gateway01.ap-northeast-1.prod.aws.tidbcloud.com`)
4. Select environments: Check **Production**, **Preview**, and **Development**
5. Click **"Save"**

Repeat for all 10 variables.

### 6. Redeploy Your Application
After adding all variables:

1. Go to the **"Deployments"** tab
2. Find the latest deployment
3. Click the three dots (**...**) menu
4. Click **"Redeploy"**
5. **IMPORTANT:** Uncheck "Use existing Build Cache"
6. Click **"Redeploy"** button

### 7. Verify Deployment
After redeployment completes (2-3 minutes):

- Visit: https://backend-git-master-noreplynexora-9184s-projects.vercel.app/
- You should see: `{"status":"ok","message":"Gym Management API is running","version":"1.0.0"}`

- Visit: https://backend-git-master-noreplynexora-9184s-projects.vercel.app/docs
- You should see the FastAPI documentation page

---

## Quick Copy-Paste Format

If you prefer, here's a format you can copy one line at a time:

```
DB_HOST
gateway01.ap-northeast-1.prod.aws.tidbcloud.com

DB_PORT
4000

DB_USERNAME
CrR1v2rQYoMqsCW.root

DB_PASSWORD
lku1aT2R5cLrfFeS

DB_DATABASE
gym_db

JWT_SECRET_KEY
gym-management-production-secret-key-2024

JWT_ALGORITHM
HS256

JWT_EXPIRY_MINUTES
1440

BASE_URL
https://backend-git-master-noreplynexora-9184s-projects.vercel.app

FRONTEND_URL
https://frontend-three-swart-21e12w3z.vercel.app
```

---

## Troubleshooting

### If you still get errors after adding variables:
1. Make sure all 10 variables are added
2. Check for typos in variable names (they are case-sensitive)
3. Make sure you selected all three environments (Production, Preview, Development)
4. Make sure you redeployed WITHOUT using the build cache

### If deployment fails:
1. Check the deployment logs in Vercel
2. Look for any error messages
3. Verify the database password is correct

---

## Need Help?
If you encounter any issues, share the deployment logs from Vercel dashboard.
