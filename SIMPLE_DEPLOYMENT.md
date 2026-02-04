# 🚀 Simple Windows EC2 Deployment - Step by Step

## 📋 Server: 34.228.199.241 (Windows EC2)

### Step 1: Connect to Windows EC2
```
1. Open Remote Desktop Connection
2. Computer: 34.228.199.241
3. Username: Administrator
4. Connect using your key pair
```

### Step 2: Install Prerequisites (Run these commands one by one)

#### Open PowerShell as Administrator and run:

```powershell
# Install Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Python
choco install python -y

# Install Node.js
choco install nodejs -y

# Install Git
choco install git -y

# Install Chrome
choco install googlechrome -y
```

### Step 3: Clone Repository
```cmd
# Open Command Prompt as Administrator
cd C:\
git clone https://github.com/Vaidehip0407/rpa-gov-portal.git
cd rpa-gov-portal
```

### Step 4: Setup Backend
```cmd
cd backend
pip install -r requirements.txt

# Create .env file manually or copy this content:
echo DATABASE_URL=sqlite:///./unified_portal.db > .env
echo SECRET_KEY=rpa-gov-portal-secret-key-2024 >> .env
echo ACCESS_TOKEN_EXPIRE_MINUTES=30 >> .env
echo APP_NAME=RPA Government Portal >> .env
echo ALGORITHM=HS256 >> .env
```

### Step 5: Setup Frontend
```cmd
cd ..\frontend
npm install
npm run build
```

### Step 6: Configure Firewall
```cmd
# Allow ports 3003 and 8000
netsh advfirewall firewall add rule name="RPA Portal Frontend" dir=in action=allow protocol=TCP localport=3003
netsh advfirewall firewall add rule name="RPA Portal Backend" dir=in action=allow protocol=TCP localport=8000
```

### Step 7: Start Services

#### Start Backend (Command Prompt 1):
```cmd
cd C:\rpa-gov-portal\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Start Frontend (Command Prompt 2):
```cmd
cd C:\rpa-gov-portal\frontend
npm run preview -- --host 0.0.0.0 --port 3003
```

### Step 8: Configure AWS Security Group
```
1. Go to AWS EC2 Console
2. Select your instance
3. Security Groups → Edit inbound rules
4. Add rules:
   - Type: Custom TCP, Port: 3003, Source: 0.0.0.0/0
   - Type: Custom TCP, Port: 8000, Source: 0.0.0.0/0
```

## 🌐 Access Your Portal:
- **Frontend**: http://34.228.199.241:3003
- **Backend**: http://34.228.199.241:8000
- **API Docs**: http://34.228.199.241:8000/docs

## 🤖 Test RPA:
1. Go to frontend URL
2. Register/Login
3. Navigate: Services → Electricity → Name Change → Torrent Power
4. Fill form and click "Start AI Auto-fill"
5. Watch Chrome browser fill the form automatically!

## ✅ Expected Results:
- Fast login/registration (2-3 seconds)
- Visible Chrome browser automation
- 5/5 form fields filled automatically
- Success message after form submission

That's it! Your RPA Government Portal is now live on Windows EC2! 🎉