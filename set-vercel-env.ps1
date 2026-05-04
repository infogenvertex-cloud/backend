# PowerShell script to set Vercel environment variables
# Run this from the backend directory: .\set-vercel-env.ps1

Write-Host "Setting Vercel environment variables..." -ForegroundColor Green

# Set each environment variable
"gateway01.ap-northeast-1.prod.aws.tidbcloud.com" | vercel env add DB_HOST production
"4000" | vercel env add DB_PORT production
"CrR1v2rQYoMqsCW.root" | vercel env add DB_USERNAME production
"lku1aT2R5cLrfFeS" | vercel env add DB_PASSWORD production
"gym_db" | vercel env add DB_DATABASE production
"gym-management-production-secret-key-2024" | vercel env add JWT_SECRET_KEY production
"HS256" | vercel env add JWT_ALGORITHM production
"1440" | vercel env add JWT_EXPIRY_MINUTES production
"https://backend-git-master-noreplynexora-9184s-projects.vercel.app" | vercel env add BASE_URL production
"https://frontend-three-swart-21e12w3z.vercel.app" | vercel env add FRONTEND_URL production

Write-Host "`nAll environment variables have been set!" -ForegroundColor Green
Write-Host "Now redeploying your project..." -ForegroundColor Yellow

# Redeploy
vercel --prod

Write-Host "`nDeployment complete!" -ForegroundColor Green
