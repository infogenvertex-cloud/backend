#!/bin/bash
# Script to set Vercel environment variables
# Run this from the backend directory: bash set-vercel-env.sh

vercel env add DB_HOST production
# Enter: gateway01.ap-northeast-1.prod.aws.tidbcloud.com

vercel env add DB_PORT production
# Enter: 4000

vercel env add DB_USERNAME production
# Enter: CrR1v2rQYoMqsCW.root

vercel env add DB_PASSWORD production
# Enter: lku1aT2R5cLrfFeS

vercel env add DB_DATABASE production
# Enter: gym_db

vercel env add JWT_SECRET_KEY production
# Enter: gym-management-production-secret-key-2024

vercel env add JWT_ALGORITHM production
# Enter: HS256

vercel env add JWT_EXPIRY_MINUTES production
# Enter: 1440

vercel env add BASE_URL production
# Enter: https://backend-git-master-noreplynexora-9184s-projects.vercel.app

vercel env add FRONTEND_URL production
# Enter: https://frontend-three-swart-21e12w3z.vercel.app

echo "All environment variables added! Now redeploy your project."
