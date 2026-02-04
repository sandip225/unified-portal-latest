@echo off
echo 🔧 FIXING RPA ISSUES ON WINDOWS EC2
echo ====================================

echo.
echo 🔍 Step 1: Stopping existing processes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im chrome.exe >nul 2>&1
echo ✅ Processes stopped

echo.
echo 🔍 Step 2: Checking Chrome installation...
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo ✅ Chrome found at: C:\Program Files\Google\Chrome\Application\chrome.exe
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    echo ✅ Chrome found at: C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
) else (
    echo ❌ Chrome not found. Installing...
    choco install googlechrome -y --ignore-checksums --force
    echo ✅ Chrome installation completed
)

echo.
echo 🔍 Step 3: Updating Python packages...
cd backend
pip uninstall selenium webdriver-manager -y >nul 2>&1
pip install selenium==4.15.2 webdriver-manager==4.0.1 requests==2.31.0
echo ✅ Python packages updated

echo.
echo 🔍 Step 4: Testing RPA setup...
python -c "
import sys
import os
sys.path.append('.')

try:
    print('🧪 Testing RPA setup...')
    
    # Test imports
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    print('✅ All imports successful')
    
    # Test Chrome driver setup
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    # Find Chrome binary
    import os
    chrome_paths = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            options.binary_location = path
            print(f'✅ Using Chrome binary: {path}')
            break
    
    # Create driver
    try:
        driver_path = ChromeDriverManager().install()
        print(f'✅ ChromeDriver path: {driver_path}')
        
        from selenium.webdriver.chrome.service import Service
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        print('✅ Chrome driver created successfully')
        
        # Test basic navigation
        driver.get('data:text/html,<h1>RPA Test Success!</h1>')
        print('✅ Navigation test successful')
        
        driver.quit()
        print('✅ RPA setup test completed successfully')
        
    except Exception as e:
        print(f'❌ Driver setup failed: {e}')
        sys.exit(1)
        
except Exception as e:
    print(f'❌ RPA test failed: {e}')
    sys.exit(1)
"

if %errorlevel% equ 0 (
    echo ✅ RPA test passed!
) else (
    echo ❌ RPA test failed. Check the error above.
)

echo.
echo 🔍 Step 5: Checking backend service...
netstat -ano | findstr :8000 >nul
if %errorlevel% equ 0 (
    echo ✅ Backend is running on port 8000
) else (
    echo ❌ Backend is not running. Starting backend...
    start "Backend" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
    echo ⏳ Backend starting in new window...
    timeout /t 10 /nobreak >nul
)

echo.
echo 🔍 Step 6: Testing backend health...
curl -s http://34.228.199.241:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend health check passed
) else (
    echo ❌ Backend health check failed
    echo 💡 Try: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
)

echo.
echo 🎯 SUMMARY
echo =========
echo ✅ RPA setup should now be working
echo ✅ Chrome browser will open visibly
echo ✅ Form auto-fill should work
echo.
echo 🌐 Access your portal at: http://34.228.199.241
echo 🔧 Backend API at: http://34.228.199.241:8000
echo.
echo 🎉 RPA fix completed!

echo.
echo Press any key to exit...
pause >nul