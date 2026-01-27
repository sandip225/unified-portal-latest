# Selenium Setup Script for Windows
# Gujarat Unified Portal - Selenium Configuration

Write-Host "🚀 Starting Selenium setup for Gujarat Unified Portal..." -ForegroundColor Green

# Check Python installation
Write-Host "🐍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    exit 1
}

# Check pip
Write-Host "📦 Checking pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ Found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip not found. Please install pip" -ForegroundColor Red
    exit 1
}

# Install requirements
Write-Host "📥 Installing Selenium requirements..." -ForegroundColor Yellow
$requirements = @(
    "selenium==4.26.1",
    "webdriver-manager==4.0.2",
    "undetected-chromedriver==3.5.5", 
    "selenium-stealth==1.0.6",
    "fake-useragent==1.4.0"
)

foreach ($requirement in $requirements) {
    Write-Host "Installing $requirement..." -ForegroundColor Cyan
    pip install $requirement
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install $requirement" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ All requirements installed successfully" -ForegroundColor Green

# Check Chrome installation
Write-Host "🌐 Checking Chrome installation..." -ForegroundColor Yellow
$chromePaths = @(
    "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
)

$chromeFound = $false
foreach ($path in $chromePaths) {
    if (Test-Path $path) {
        Write-Host "✅ Chrome found at: $path" -ForegroundColor Green
        $chromeFound = $true
        break
    }
}

if (-not $chromeFound) {
    Write-Host "⚠️ Chrome not found. Please install Chrome from https://www.google.com/chrome/" -ForegroundColor Yellow
}

# Create directories
Write-Host "📁 Creating directories..." -ForegroundColor Yellow
$directories = @(
    "chrome_automation_data",
    "downloads",
    "screenshots", 
    "user_data",
    "automation_logs"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Created directory: $dir" -ForegroundColor Green
    } else {
        Write-Host "✅ Directory exists: $dir" -ForegroundColor Green
    }
}

# Test Selenium setup
Write-Host "🧪 Testing Selenium setup..." -ForegroundColor Yellow
$testScript = @"
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    import undetected_chromedriver as uc
    from selenium_stealth import stealth
    from fake_useragent import UserAgent
    
    print("✅ All Selenium imports successful")
    
    # Test ChromeDriver download
    driver_path = ChromeDriverManager().install()
    print(f"✅ ChromeDriver installed at: {driver_path}")
    
    # Test UserAgent
    ua = UserAgent()
    user_agent = ua.random
    print(f"✅ Random user agent generated")
    
    print("🎉 Selenium setup test completed successfully!")
    
except Exception as e:
    print(f"❌ Setup test failed: {e}")
    exit(1)
"@

$testScript | python
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Selenium test failed" -ForegroundColor Red
    exit 1
}

# Create configuration file
Write-Host "📝 Creating configuration file..." -ForegroundColor Yellow
$configContent = @"
# Selenium Configuration for Gujarat Unified Portal

## Setup Completed: $(Get-Date)

## Installed Components:
- Selenium WebDriver 4.26.1
- WebDriver Manager 4.0.2  
- Undetected ChromeDriver 3.5.5
- Selenium Stealth 1.0.6
- Fake UserAgent 1.4.0

## Features:
- ✅ Anti-detection stealth mode
- ✅ Undetected ChromeDriver support
- ✅ User data persistence
- ✅ Government site optimization
- ✅ Smart element finding
- ✅ Human-like typing simulation
- ✅ Multiple click strategies
- ✅ Automatic screenshot capture

## API Endpoints:
- GET /api/selenium/health - Check Selenium health
- POST /api/selenium/test-driver - Test WebDriver
- GET /api/selenium/config - Get configuration
- POST /api/selenium/install-chrome - Chrome installation guide
- DELETE /api/selenium/cleanup - Cleanup data

## Usage:
1. Start FastAPI server: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
2. Visit http://localhost:8000/docs for API documentation
3. Test Selenium health: GET /api/selenium/health
4. Run automation: POST /api/unified-automation/start-automation

## Troubleshooting:
- If Chrome not found, install from https://www.google.com/chrome/
- If ChromeDriver issues, delete chrome_automation_data folder
- Check logs in automation_logs directory
- Use headless=False to see browser in action

## Windows Specific:
- Chrome paths checked: Program Files and Program Files (x86)
- User data stored in: chrome_automation_data
- Screenshots saved in: screenshots
- Downloads saved in: downloads
"@

$configContent | Out-File -FilePath "SELENIUM_SETUP.md" -Encoding UTF8
Write-Host "✅ Created SELENIUM_SETUP.md configuration file" -ForegroundColor Green

# Final summary
Write-Host "`n🎉 Selenium setup completed successfully!" -ForegroundColor Green
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Start your FastAPI server: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor White
Write-Host "   2. Test health check: GET http://localhost:8000/api/selenium/health" -ForegroundColor White
Write-Host "   3. Run automation: POST http://localhost:8000/api/unified-automation/start-automation" -ForegroundColor White

if (-not $chromeFound) {
    Write-Host "   4. Install Chrome from: https://www.google.com/chrome/" -ForegroundColor Yellow
}

Write-Host "`n✨ Ready for Gujarat supplier automation!" -ForegroundColor Green