# Gym Management System - Backend API

FastAPI backend for the Marvel Fitness Gym Management System with TiDB database.

## Features

- 🔐 JWT Authentication
- 👥 Member Management
- 📅 Subscription Tracking
- 💰 Payment Processing
- 📊 Dashboard Analytics
- 👤 Visitor Tracking
- 🔍 Advanced Search
- 📱 WhatsApp Integration (Optional)
- ⏰ Automated Expiry Reminders

## Tech Stack

- **Framework**: FastAPI
- **Database**: TiDB (MySQL-compatible)
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **Deployment**: Vercel Serverless

## Local Development

### Prerequisites

- Python 3.9+
- TiDB Cloud account (or local TiDB)

### Setup

1. Clone the repository:
```bash
git clone <your-backend-repo-url>
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Update `.env` with your TiDB connection string:
```env
DATABASE_URL=mysql+pymysql://username:password@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/gym_db?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true
JWT_SECRET_KEY=your-super-secret-key
FRONTEND_URL=http://localhost:5006
```

6. Run the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

7. Create admin user:
```bash
python create_admin.py
```

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deployment to Vercel

### Prerequisites

- Vercel account
- TiDB Cloud database
- GitHub repository

### Steps

1. Push code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

2. Import project to Vercel:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Select the backend folder as root directory

3. Configure Environment Variables in Vercel:
   - `DATABASE_URL`: Your TiDB connection string
   - `JWT_SECRET_KEY`: Strong secret key
   - `JWT_EXPIRY_MINUTES`: 1440
   - `FRONTEND_URL`: Your frontend Vercel URL
   - `SCHEDULER_HOUR`: 8
   - `SCHEDULER_MINUTE`: 0
   - `EXPIRY_REMINDER_DAYS`: 5
   - `WHATSAPP_TOKEN`: (Optional)
   - `WHATSAPP_PHONE_ID`: (Optional)

4. Deploy!

### TiDB Connection String Format

```
mysql+pymysql://[username]:[password]@[host]:[port]/[database]?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true
```

Example:
```
mysql+pymysql://2aXxXxXx.root:YourPassword@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/gym_db?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | TiDB connection string | Yes |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | Yes |
| `JWT_EXPIRY_MINUTES` | Token expiry time (default: 1440) | No |
| `FRONTEND_URL` | Frontend URL for CORS | Yes |
| `SCHEDULER_HOUR` | Hour to run daily checks (0-23) | No |
| `SCHEDULER_MINUTE` | Minute to run daily checks (0-59) | No |
| `EXPIRY_REMINDER_DAYS` | Days before expiry to send reminder | No |
| `WHATSAPP_TOKEN` | WhatsApp API token | No |
| `WHATSAPP_PHONE_ID` | WhatsApp phone number ID | No |

## API Endpoints

### Authentication
- `POST /api/auth/login` - Admin login

### Members
- `GET /api/members/` - List all members
- `GET /api/members/?search=query` - Search members
- `POST /api/members/` - Create member
- `GET /api/members/{id}` - Get member details
- `PUT /api/members/{id}` - Update member
- `DELETE /api/members/{id}` - Delete member

### Subscriptions
- `GET /api/subscriptions/` - List subscriptions
- `POST /api/subscriptions/` - Create subscription
- `GET /api/subscriptions/{id}` - Get subscription
- `PUT /api/subscriptions/{id}` - Update subscription
- `DELETE /api/subscriptions/{id}` - Delete subscription

### Payments
- `GET /api/payments/` - List payments
- `POST /api/payments/` - Create payment
- `GET /api/payments/{id}` - Get payment
- `DELETE /api/payments/{id}` - Delete payment

### Visitors
- `GET /api/visitors/` - List visitors
- `POST /api/visitors/` - Add visitor
- `PUT /api/visitors/{id}` - Update visitor
- `DELETE /api/visitors/{id}` - Delete visitor

### Dashboard
- `GET /api/dashboard/` - Get dashboard statistics

## Database Schema

The application automatically creates tables on startup:
- `admins` - Admin users
- `members` - Gym members
- `subscriptions` - Membership subscriptions
- `payments` - Payment records
- `visitors` - Visitor logs

## Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- SQL injection prevention via SQLAlchemy ORM
- Input validation with Pydantic

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.
