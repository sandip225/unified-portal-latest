# Windows EC2 Deployment Guide - RPA Government Portal

## 🖥️ New Windows EC2 Instance: 34.228.199.241

### ✅ Why Windows EC2 for RPA?
- **Visible Browser**: Chrome browser actually dikhega (not headless)
- **Full GUI Support**: Windows desktop environment available  
- **Same as Localhost**: Jaise localhost par chal raha hai, waise hi chalega
- **No Linux Restrictions**: Linux ki headless limitations nahi hongi

## 🚀 Deployment Steps

### 1. Connect to Windows EC2
```
Server: 34.228.199.241
Method: RDP (Remote Desktop)
Username: Administrator
Password: [Your EC2 key pair password]
```

### 2. Install Prerequisites on Windows Server

#### Install Chrome Browser:
```cmd
# Download and install Chrome from:
https://www.google.com/chrome/
```

#### Install Python 3.11+:
```cmd
# Download from: https://www.python.org/downloads/
# Make sure to check "Add Python to PATH"
```

#### Install Node.js 18+:
```cmd
# Download from: https://nodejs.org/
```

#### Install Git:
```cmd
# Download from: https://git-scm.com/download/win
```

### 3. Clone and Setup Repository

```cmd
# Clone the repository
git clone https://github.com/Vaidehip0407/rpa-gov-portal.git
cd rpa-gov-portal

# Setup Backend
cd backend
pip install -r requirements.txt

# Setup Frontend  
cd ..\frontend
npm install
npm run build
```

### 4. Configure Environment

#### Backend Environment (.env):
```env
DATABASE_URL=sqlite:///./unified_portal.db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=RPA Government Portal
ALGORITHM=HS256
```

#### Frontend Environment:
```env
VITE_API_URL=http://34.228.199.241:8000/api
```

### 5. Start Services

#### Start Backend (in Command Prompt 1):
```cmd
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Start Frontend (in Command Prompt 2):
```cmd
cd frontend
npm run preview -- --host 0.0.0.0 --port 3003
```

### 6. Configure Windows Firewall

```cmd
# Allow inbound connections on ports 3003 and 8000
netsh advfirewall firewall add rule name="RPA Portal Frontend" dir=in action=allow protocol=TCP localport=3003
netsh advfirewall firewall add rule name="RPA Portal Backend" dir=in action=allow protocol=TCP localport=8000
```

## 🌐 Access URLs

- **Frontend**: http://34.228.199.241:3003
- **Backend**: http://34.228.199.241:8000  
- **API Docs**: http://34.228.199.241:8000/docs

## 🤖 RPA Automation Features

### ✅ What Works on Windows EC2:
- **Visible Chrome Browser**: User can see automation happening
- **Form Auto-fill**: Torrent Power forms filled automatically
- **Real-time Feedback**: Green highlighting on filled fields
- **Success Messages**: Confirmation after form submission
- **No Headless Issues**: Full GUI support

### 🎯 RPA Flow:
1. User clicks "Start AI Auto-fill"
2. Chrome browser opens visibly on Windows desktop
3. Navigates to Torrent Power website
4. Fills all form fields with green highlighting
5. Clicks Submit button automatically
6. Shows success message on website
7. Keeps browser open for user review

## 🔧 Troubleshooting

### RPA Not Working:
```cmd
# Test Chrome installation
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version

# Test Python Selenium
python -c "from selenium import webdriver; print('Selenium working')"

# Test webdriver-manager
python -c "from webdriver_manager.chrome import ChromeDriverManager; print('WebDriver Manager working')"
```

### Port Issues:
```cmd
# Check if ports are open
netstat -an | findstr :3003
netstat -an | findstr :8000
```

### Service Management:
```cmd
# Create Windows Services (optional)
# Use NSSM (Non-Sucking Service Manager) to run as Windows services
```

## 📝 Production Tips

1. **Auto-start Services**: Configure services to start automatically on boot
2. **Monitoring**: Use Windows Task Manager to monitor resource usage
3. **Backup**: Regular backup of SQLite database
4. **Updates**: Keep Chrome and Python updated for RPA compatibility
5. **Security**: Configure Windows Defender and firewall properly

## 🎉 Expected Results

- **Fast Login/Registration**: 2-3 seconds (bcrypt optimized)
- **Working RPA**: 5/5 fields filled successfully
- **Visible Automation**: User can watch Chrome filling forms
- **Professional UI**: Government portal design with Ashoka emblem
- **Stable Performance**: Windows GUI environment ensures reliability

The Windows EC2 setup will give you the same RPA experience as localhost! 🚀