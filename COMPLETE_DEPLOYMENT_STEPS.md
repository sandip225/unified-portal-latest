# 🚀 Complete Windows EC2 Deployment Steps

## 📋 Server Details:
- **IP**: 34.228.199.241
- **OS**: Windows Server 2019/2022
- **Access**: RDP (Remote Desktop Protocol)

## 🔧 Step-by-Step Deployment Commands

### STEP 1: Connect to Windows EC2
```
1. Open Remote Desktop Connection
2. Computer: 34.228.199.241
3. Username: Administrator
4. Password: [Your EC2 key pair password]
```

### STEP 2: Install Prerequisites (Run on EC2)

#### Install Chrome Browser:
```cmd
# Download and install from: https://www.google.com/chrome/
# Or use PowerShell:
Invoke-WebRequest -Uri "https://dl.google.com/chrome/install/latest/chrome_installer.exe" -OutFile "chrome_installer.exe"
.\chrome_installer.exe
```

#### Install Python 3.11+:
```cmd
# Download from: https://www.python.org/downloads/windows/
# Or use Chocolatey:
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco install python -y
```

#### Install Node.js 18+:
```cmd
# Download from: https://nodejs.org/
# Or use Chocolatey:
choco install nodejs -y
```

#### Install Git:
```cmd
# Download from: https://git-scm.com/download/win
# Or use Chocolatey:
choco install git -y
```

### STEP 3: Clone Repository (Run on EC2)
```cmd
# Open Command Prompt as Administrator
cd C:\
git clone https://github.com/Vaidehip0407/rpa-gov-portal.git
cd rpa-gov-portal
```

### STEP 4: Setup Backend (Run on EC2)
```cmd
cd backend
pip install -r requirements.txt

# Create .env file
echo DATABASE_URL=sqlite:///./unified_portal.db > .env
echo SECRET_KEY=rpa-gov-portal-secret-key-2024 >> .env
echo ACCESS_TOKEN_EXPIRE_MINUTES=30 >> .env
echo APP_NAME=RPA Government Portal >> .env
echo ALGORITHM=HS256 >> .env
```

### STEP 5: Setup Frontend (Run on EC2)
```cmd
cd ..\frontend
npm install
npm run build
```

### STEP 6: Configure Windows Firewall (Run on EC2)
```cmd
# Allow inbound connections
netsh advfirewall firewall add rule name="RPA Portal Frontend" dir=in action=allow protocol=TCP localport=3003
netsh advfirewall firewall add rule name="RPA Portal Backend" dir=in action=allow protocol=TCP localport=8000

# Check firewall rules
netsh advfirewall firewall show rule name="RPA Portal Frontend"
netsh advfirewall firewall show rule name="RPA Portal Backend"
```

### STEP 7: Start Backend Service (Run on EC2)
```cmd
# Open Command Prompt 1 as Administrator
cd C:\rpa-gov-portal\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### STEP 8: Start Frontend Service (Run on EC2)
```cmd
# Open Command Prompt 2 as Administrator
cd C:\rpa-gov-portal\frontend
npm run preview -- --host 0.0.0.0 --port 3003

# You should see:
# Local:   http://localhost:3003/
# Network: http://0.0.0.0:3003/
```

### STEP 9: Test Services (Run on EC2)
```cmd
# Test Backend Health
curl http://localhost:8000/health

# Test Frontend
curl http://localhost:3003
```

### STEP 10: Configure AWS Security Group
```
1. Go to AWS EC2 Console
2. Select your instance (34.228.199.241)
3. Go to Security Groups
4. Add Inbound Rules:
   - Type: Custom TCP, Port: 3003, Source: 0.0.0.0/0
   - Type: Custom TCP, Port: 8000, Source: 0.0.0.0/0
```

## 🌐 Access URLs (After Deployment):
- **Frontend**: http://34.228.199.241:3003
- **Backend**: http://34.228.199.241:8000
- **API Docs**: http://34.228.199.241:8000/docs

## 🤖 Test RPA Automation:
1. Go to: http://34.228.199.241:3003
2. Register/Login to portal
3. Navigate: Services → Electricity → Name Change → Torrent Power
4. Fill form and click "Start AI Auto-fill"
5. Watch Chrome browser open and fill form automatically!

## 🔍 Troubleshooting Commands:

### Check Services:
```cmd
# Check if Python is running
tasklist | findstr python

# Check if Node is running  
tasklist | findstr node

# Check port usage
netstat -an | findstr :3003
netstat -an | findstr :8000
```

### Restart Services:
```cmd
# Kill existing processes
taskkill /f /im python.exe
taskkill /f /im node.exe

# Restart backend
cd C:\rpa-gov-portal\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Restart frontend
cd C:\rpa-gov-portal\frontend  
npm run preview -- --host 0.0.0.0 --port 3003
```

### Check Chrome for RPA:
```cmd
# Verify Chrome installation
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version

# Test Selenium
python -c "from selenium import webdriver; print('✅ Selenium working')"
```

## 🎯 Expected Results:
- ✅ Backend running on port 8000
- ✅ Frontend running on port 3003  
- ✅ RPA automation working with visible Chrome
- ✅ Forms auto-filled successfully
- ✅ Fast login/registration (2-3 seconds)

## 📞 Support:
If any step fails, check the error messages and refer to troubleshooting section above.

🚀 **Your RPA Government Portal will be live on Windows EC2!** 🚀