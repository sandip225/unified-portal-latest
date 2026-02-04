@echo off
echo 🚀 DEPLOYING TO WINDOWS EC2: 34.228.199.241
echo ================================================

echo 📋 Prerequisites Check:
echo - Windows Server 2019/2022 AMI
echo - Chrome browser installed
echo - Python 3.11+ installed
echo - Node.js 18+ installed
echo - Git installed
echo - RDP access enabled
echo.

echo 🔧 Step 1: Connect to Windows EC2
echo Server: 34.228.199.241
echo Method: RDP (Remote Desktop)
echo Username: Administrator
echo.

echo 📥 Step 2: Clone Repository (Run on EC2)
echo git clone https://github.com/Vaidehip0407/rpa-gov-portal.git
echo cd rpa-gov-portal
echo.

echo 🐍 Step 3: Setup Backend (Run on EC2)
echo cd backend
echo pip install -r requirements.txt
echo.

echo 🎨 Step 4: Setup Frontend (Run on EC2)
echo cd ..\frontend
echo npm install
echo npm run build
echo.

echo ⚙️ Step 5: Configure Environment (Run on EC2)
echo Create backend\.env with:
echo DATABASE_URL=sqlite:///./unified_portal.db
echo SECRET_KEY=your-secret-key-here
echo ACCESS_TOKEN_EXPIRE_MINUTES=30
echo APP_NAME=RPA Government Portal
echo ALGORITHM=HS256
echo.

echo 🔥 Step 6: Configure Windows Firewall (Run on EC2)
echo netsh advfirewall firewall add rule name="RPA Portal Frontend" dir=in action=allow protocol=TCP localport=3003
echo netsh advfirewall firewall add rule name="RPA Portal Backend" dir=in action=allow protocol=TCP localport=8000
echo.

echo 🚀 Step 7: Start Services (Run on EC2)
echo Backend: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
echo Frontend: npm run preview -- --host 0.0.0.0 --port 3003
echo.

echo 🌐 Access URLs:
echo Frontend: http://34.228.199.241:3003
echo Backend: http://34.228.199.241:8000
echo API Docs: http://34.228.199.241:8000/docs
echo.

echo 🤖 RPA Features:
echo ✅ Visible Chrome browser automation
echo ✅ Torrent Power form auto-fill
echo ✅ Real-time visual feedback
echo ✅ Success message after submission
echo ✅ No headless restrictions
echo.

echo 📝 Next Steps:
echo 1. Connect to Windows EC2 via RDP
echo 2. Run the commands shown above
echo 3. Test RPA automation
echo 4. Enjoy visible browser automation!
echo.

pause