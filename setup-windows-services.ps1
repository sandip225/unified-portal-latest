# Setup Windows Services for RPA Government Portal
# This will make frontend and backend start automatically on Windows EC2

Write-Host "🚀 Setting up Windows Services for Auto-Startup" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "❌ Please run this script as Administrator" -ForegroundColor Red
    exit 1
}

# Install NSSM (Non-Sucking Service Manager)
Write-Host "📦 Installing NSSM (Service Manager)..." -ForegroundColor Yellow
try {
    choco install nssm -y
    Write-Host "✅ NSSM installed successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️ NSSM installation failed, trying manual download..." -ForegroundColor Yellow
    
    # Download NSSM manually
    $nssmUrl = "https://nssm.cc/release/nssm-2.24.zip"
    $nssmZip = "C:\temp\nssm.zip"
    $nssmDir = "C:\nssm"
    
    New-Item -ItemType Directory -Path "C:\temp" -Force
    Invoke-WebRequest -Uri $nssmUrl -OutFile $nssmZip
    Expand-Archive -Path $nssmZip -DestinationPath "C:\temp" -Force
    Move-Item "C:\temp\nssm-2.24\win64\nssm.exe" "C:\Windows\System32\nssm.exe" -Force
    Write-Host "✅ NSSM installed manually" -ForegroundColor Green
}

# Project paths
$projectPath = "C:\rpa-gov-portal"
$backendPath = "$projectPath\backend"
$frontendPath = "$projectPath\frontend"

# Create service scripts
Write-Host "📝 Creating service scripts..." -ForegroundColor Yellow

# Backend service script
$backendScript = @"
@echo off
cd /d $backendPath
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
"@

$backendScript | Out-File -FilePath "$projectPath\backend-service.bat" -Encoding ASCII

# Frontend service script
$frontendScript = @"
@echo off
cd /d $frontendPath
npx serve dist -l 80
"@

$frontendScript | Out-File -FilePath "$projectPath\frontend-service.bat" -Encoding ASCII

Write-Host "✅ Service scripts created" -ForegroundColor Green

# Remove existing services if they exist
Write-Host "🧹 Removing existing services..." -ForegroundColor Yellow
nssm remove "RPA-Backend" confirm 2>$null
nssm remove "RPA-Frontend" confirm 2>$null

# Create Backend Service
Write-Host "🔧 Creating Backend Service..." -ForegroundColor Yellow
nssm install "RPA-Backend" "$projectPath\backend-service.bat"
nssm set "RPA-Backend" DisplayName "RPA Government Portal - Backend"
nssm set "RPA-Backend" Description "FastAPI backend service for RPA Government Portal"
nssm set "RPA-Backend" Start SERVICE_AUTO_START
nssm set "RPA-Backend" AppStdout "$projectPath\logs\backend-stdout.log"
nssm set "RPA-Backend" AppStderr "$projectPath\logs\backend-stderr.log"
nssm set "RPA-Backend" AppRotateFiles 1
nssm set "RPA-Backend" AppRotateOnline 1
nssm set "RPA-Backend" AppRotateSeconds 86400
nssm set "RPA-Backend" AppRotateBytes 1048576

Write-Host "✅ Backend service created" -ForegroundColor Green

# Create Frontend Service
Write-Host "🔧 Creating Frontend Service..." -ForegroundColor Yellow
nssm install "RPA-Frontend" "$projectPath\frontend-service.bat"
nssm set "RPA-Frontend" DisplayName "RPA Government Portal - Frontend"
nssm set "RPA-Frontend" Description "React frontend service for RPA Government Portal"
nssm set "RPA-Frontend" Start SERVICE_AUTO_START
nssm set "RPA-Frontend" AppStdout "$projectPath\logs\frontend-stdout.log"
nssm set "RPA-Frontend" AppStderr "$projectPath\logs\frontend-stderr.log"
nssm set "RPA-Frontend" AppRotateFiles 1
nssm set "RPA-Frontend" AppRotateOnline 1
nssm set "RPA-Frontend" AppRotateSeconds 86400
nssm set "RPA-Frontend" AppRotateBytes 1048576

Write-Host "✅ Frontend service created" -ForegroundColor Green

# Create logs directory
New-Item -ItemType Directory -Path "$projectPath\logs" -Force

# Start services
Write-Host "🚀 Starting services..." -ForegroundColor Yellow
Start-Service "RPA-Backend"
Start-Service "RPA-Frontend"

# Wait for services to start
Start-Sleep -Seconds 10

# Check service status
Write-Host "🔍 Checking service status..." -ForegroundColor Yellow
$backendStatus = Get-Service "RPA-Backend" | Select-Object -ExpandProperty Status
$frontendStatus = Get-Service "RPA-Frontend" | Select-Object -ExpandProperty Status

Write-Host "Backend Service Status: $backendStatus" -ForegroundColor $(if($backendStatus -eq 'Running'){'Green'}else{'Red'})
Write-Host "Frontend Service Status: $frontendStatus" -ForegroundColor $(if($frontendStatus -eq 'Running'){'Green'}else{'Red'})

# Test endpoints
Write-Host "🧪 Testing endpoints..." -ForegroundColor Yellow

try {
    $backendTest = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 10
    Write-Host "✅ Backend is responding on port 8000" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend is not responding on port 8000" -ForegroundColor Red
}

try {
    $frontendTest = Invoke-WebRequest -Uri "http://localhost" -TimeoutSec 10
    Write-Host "✅ Frontend is responding on port 80" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend is not responding on port 80" -ForegroundColor Red
}

# Configure Windows Firewall
Write-Host "🔥 Configuring Windows Firewall..." -ForegroundColor Yellow
netsh advfirewall firewall add rule name="RPA Portal Frontend" dir=in action=allow protocol=TCP localport=80
netsh advfirewall firewall add rule name="RPA Portal Backend" dir=in action=allow protocol=TCP localport=8000

Write-Host "✅ Firewall configured" -ForegroundColor Green

# Create management scripts
Write-Host "📝 Creating management scripts..." -ForegroundColor Yellow

# Start services script
$startScript = @"
@echo off
echo Starting RPA Government Portal Services...
net start RPA-Backend
net start RPA-Frontend
echo Services started!
pause
"@

$startScript | Out-File -FilePath "$projectPath\start-services.bat" -Encoding ASCII

# Stop services script
$stopScript = @"
@echo off
echo Stopping RPA Government Portal Services...
net stop RPA-Frontend
net stop RPA-Backend
echo Services stopped!
pause
"@

$stopScript | Out-File -FilePath "$projectPath\stop-services.bat" -Encoding ASCII

# Restart services script
$restartScript = @"
@echo off
echo Restarting RPA Government Portal Services...
net stop RPA-Frontend
net stop RPA-Backend
timeout /t 5 /nobreak
net start RPA-Backend
net start RPA-Frontend
echo Services restarted!
pause
"@

$restartScript | Out-File -FilePath "$projectPath\restart-services.bat" -Encoding ASCII

# Status check script
$statusScript = @"
@echo off
echo RPA Government Portal Service Status:
echo =====================================
sc query RPA-Backend
echo.
sc query RPA-Frontend
echo.
echo Testing endpoints...
curl -s http://localhost:8000/health
echo.
curl -s http://localhost
echo.
pause
"@

$statusScript | Out-File -FilePath "$projectPath\check-services.bat" -Encoding ASCII

Write-Host "✅ Management scripts created" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 WINDOWS SERVICES SETUP COMPLETE!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Services Created:" -ForegroundColor Yellow
Write-Host "   • RPA-Backend (Port 8000)" -ForegroundColor White
Write-Host "   • RPA-Frontend (Port 80)" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Access URLs:" -ForegroundColor Yellow
Write-Host "   • Frontend: http://34.228.199.241" -ForegroundColor White
Write-Host "   • Backend:  http://34.228.199.241:8000" -ForegroundColor White
Write-Host "   • API Docs: http://34.228.199.241:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Management Commands:" -ForegroundColor Yellow
Write-Host "   • Start:    $projectPath\start-services.bat" -ForegroundColor White
Write-Host "   • Stop:     $projectPath\stop-services.bat" -ForegroundColor White
Write-Host "   • Restart:  $projectPath\restart-services.bat" -ForegroundColor White
Write-Host "   • Status:   $projectPath\check-services.bat" -ForegroundColor White
Write-Host ""
Write-Host "📁 Log Files:" -ForegroundColor Yellow
Write-Host "   • Backend:  $projectPath\logs\backend-stdout.log" -ForegroundColor White
Write-Host "   • Frontend: $projectPath\logs\frontend-stdout.log" -ForegroundColor White
Write-Host ""
Write-Host "✅ Services will start automatically on Windows boot!" -ForegroundColor Green
Write-Host "✅ No more manual terminal startup required!" -ForegroundColor Green

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")