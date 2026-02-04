# Windows EC2 Deployment Script for RPA Government Portal
# Run this script on Windows EC2 instance (34.228.199.241)

Write-Host "🚀 DEPLOYING RPA GOVERNMENT PORTAL TO WINDOWS EC2" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Running as Administrator" -ForegroundColor Green

# Step 1: Install Chocolatey (Package Manager)
Write-Host "📦 Installing Chocolatey..." -ForegroundColor Cyan
try {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    Write-Host "✅ Chocolatey installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Chocolatey installation failed, continuing..." -ForegroundColor Yellow
}

# Step 2: Install Prerequisites
Write-Host "🔧 Installing Prerequisites..." -ForegroundColor Cyan

# Install Python
Write-Host "Installing Python..." -ForegroundColor Yellow
choco install python -y

# Install Node.js
Write-Host "Installing Node.js..." -ForegroundColor Yellow
choco install nodejs -y

# Install Git
Write-Host "Installing Git..." -ForegroundColor Yellow
choco install git -y

# Install Chrome
Write-Host "Installing Chrome..." -ForegroundColor Yellow
choco install googlechrome -y

# Refresh environment variables
Write-Host "Refreshing environment variables..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Step 3: Clone Repository
Write-Host "📥 Cloning Repository..." -ForegroundColor Cyan
Set-Location C:\
if (Test-Path "C:\rpa-gov-portal") {
    Write-Host "Repository already exists, pulling latest changes..." -ForegroundColor Yellow
    Set-Location C:\rpa-gov-portal
    git pull origin main
} else {
    git clone https://github.com/Vaidehip0407/rpa-gov-portal.git
    Set-Location C:\rpa-gov-portal
}

# Step 4: Setup Backend
Write-Host "🐍 Setting up Backend..." -ForegroundColor Cyan
Set-Location backend

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env file
Write-Host "Creating .env file..." -ForegroundColor Yellow
$envContent = @"
DATABASE_URL=sqlite:///./unified_portal.db
SECRET_KEY=rpa-gov-portal-secret-key-2024
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=RPA Government Portal
ALGORITHM=HS256
"@
$envContent | Out-File -FilePath ".env" -Encoding UTF8

Write-Host "✅ Backend setup complete" -ForegroundColor Green

# Step 5: Setup Frontend
Write-Host "🎨 Setting up Frontend..." -ForegroundColor Cyan
Set-Location ..\frontend

# Install Node dependencies
Write-Host "Installing Node dependencies..." -ForegroundColor Yellow
npm install

# Build frontend
Write-Host "Building frontend..." -ForegroundColor Yellow
npm run build

Write-Host "✅ Frontend setup complete" -ForegroundColor Green

# Step 6: Configure Windows Firewall
Write-Host "🔥 Configuring Windows Firewall..." -ForegroundColor Cyan
netsh advfirewall firewall add rule name="RPA Portal Frontend" dir=in action=allow protocol=TCP localport=3003
netsh advfirewall firewall add rule name="RPA Portal Backend" dir=in action=allow protocol=TCP localport=8000
Write-Host "✅ Firewall configured" -ForegroundColor Green

# Step 7: Create startup scripts
Write-Host "📝 Creating startup scripts..." -ForegroundColor Cyan

# Backend startup script
$backendScript = @"
@echo off
cd C:\rpa-gov-portal\backend
echo 🚀 Starting RPA Government Portal Backend...
echo Backend will be available at: http://34.228.199.241:8000
echo API Docs: http://34.228.199.241:8000/docs
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
pause
"@
$backendScript | Out-File -FilePath "C:\rpa-gov-portal\start-backend.bat" -Encoding UTF8

# Frontend startup script
$frontendScript = @"
@echo off
cd C:\rpa-gov-portal\frontend
echo 🎨 Starting RPA Government Portal Frontend...
echo Frontend will be available at: http://34.228.199.241:3003
echo.
npm run preview -- --host 0.0.0.0 --port 3003
pause
"@
$frontendScript | Out-File -FilePath "C:\rpa-gov-portal\start-frontend.bat" -Encoding UTF8

# Combined startup script
$portalScript = @"
@echo off
echo 🚀 STARTING RPA GOVERNMENT PORTAL
echo ================================
echo.
echo Starting Backend...
start "RPA Backend" cmd /k "C:\rpa-gov-portal\start-backend.bat"
timeout /t 5 /nobreak > nul

echo Starting Frontend...
start "RPA Frontend" cmd /k "C:\rpa-gov-portal\start-frontend.bat"

echo.
echo 🎉 RPA Government Portal is starting!
echo ====================================
echo.
echo 🌐 URLs:
echo Frontend: http://34.228.199.241:3003
echo Backend:  http://34.228.199.241:8000
echo API Docs: http://34.228.199.241:8000/docs
echo.
echo 🤖 RPA Features:
echo ✅ Visible Chrome browser automation
echo ✅ Torrent Power form auto-fill
echo ✅ Real-time visual feedback
echo ✅ Success messages after submission
echo.
echo 📝 Next Steps:
echo 1. Wait for services to start (30 seconds)
echo 2. Open browser and go to: http://34.228.199.241:3003
echo 3. Register/Login to portal
echo 4. Test RPA automation!
echo.
pause
"@
$portalScript | Out-File -FilePath "C:\rpa-gov-portal\start-portal.bat" -Encoding UTF8

Write-Host "✅ Startup scripts created" -ForegroundColor Green

# Step 8: Final Instructions
Write-Host ""
Write-Host "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "📁 Files created:" -ForegroundColor Cyan
Write-Host "  - C:\rpa-gov-portal\start-backend.bat" -ForegroundColor White
Write-Host "  - C:\rpa-gov-portal\start-frontend.bat" -ForegroundColor White
Write-Host "  - C:\rpa-gov-portal\start-portal.bat" -ForegroundColor White
Write-Host ""
Write-Host "🚀 To start the portal:" -ForegroundColor Cyan
Write-Host "  Double-click: C:\rpa-gov-portal\start-portal.bat" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Access URLs:" -ForegroundColor Cyan
Write-Host "  Frontend: http://34.228.199.241:3003" -ForegroundColor White
Write-Host "  Backend:  http://34.228.199.241:8000" -ForegroundColor White
Write-Host "  API Docs: http://34.228.199.241:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "🤖 RPA Features Ready:" -ForegroundColor Cyan
Write-Host "  ✅ Visible Chrome browser automation" -ForegroundColor Green
Write-Host "  ✅ Torrent Power form auto-fill" -ForegroundColor Green
Write-Host "  ✅ Real-time visual feedback" -ForegroundColor Green
Write-Host "  ✅ Success messages after submission" -ForegroundColor Green
Write-Host ""
Write-Host "🔧 AWS Security Group:" -ForegroundColor Yellow
Write-Host "  Make sure to allow inbound traffic on ports 3003 and 8000" -ForegroundColor White
Write-Host ""

# Ask if user wants to start the portal now
$startNow = Read-Host "Do you want to start the portal now? (y/n)"
if ($startNow -eq "y" -or $startNow -eq "Y") {
    Write-Host "🚀 Starting RPA Government Portal..." -ForegroundColor Green
    Start-Process "C:\rpa-gov-portal\start-portal.bat"
} else {
    Write-Host "👍 You can start the portal later by running:" -ForegroundColor Yellow
    Write-Host "   C:\rpa-gov-portal\start-portal.bat" -ForegroundColor White
}

Write-Host ""
Write-Host "🎯 Deployment Complete! Your RPA Government Portal is ready!" -ForegroundColor Green