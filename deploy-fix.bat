@echo off
echo 🔧 Deploying Fixed Configuration...

REM Stop existing containers
echo Stopping existing containers...
docker-compose down

REM Rebuild with new configuration
echo Building containers...
docker-compose build --no-cache

REM Start services
echo Starting services...
docker-compose up -d

REM Wait for services to be ready
echo Waiting for services to start...
timeout /t 10 /nobreak > nul

REM Check status
echo.
echo 📊 Service Status:
docker-compose ps

echo.
echo ✅ Deployment complete!
echo.
echo Access your application at:
echo   http://18.207.167.97
echo.
echo View logs with:
echo   docker-compose logs -f
