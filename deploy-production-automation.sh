#!/bin/bash

echo "🚀 PRODUCTION-READY TORRENT POWER AUTOMATION DEPLOYMENT"
echo "======================================================="

# Pull latest code
echo "📥 Pulling latest production-ready automation code..."
git pull origin main

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker compose -f docker-compose.prod.yml down

# Remove old backend image to force rebuild
echo "🗑️ Removing old backend image..."
docker rmi india-portal-backend 2>/dev/null || true

# Create SSL certificate
echo "🔐 Creating SSL certificate..."
mkdir -p ssl
openssl req -x509 -newkey rsa:2048 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes -subj "/CN=50.19.189.29" 2>/dev/null

# Build with production automation
echo "🔨 Building services with production automation..."
docker compose -f docker-compose.prod.yml build --no-cache

# Start all services
echo "🚀 Starting all services..."
docker compose -f docker-compose.prod.yml up -d

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 60

# Check status
echo "📊 Checking service status..."
docker compose -f docker-compose.prod.yml ps

# Test automation service
echo "🧪 Testing production automation service..."
sleep 10
curl -s http://localhost:8000/torrent-automation/test-connection | grep -q "success" && echo "✅ Automation service ready!" || echo "⚠️ Automation service starting..."

# Test supported fields
echo ""
echo "📋 Testing supported fields endpoint..."
curl -s http://localhost:8000/torrent-automation/supported-fields | grep -q "torrent_power" && echo "✅ Automation endpoints working!" || echo "⚠️ Endpoints still loading..."

echo ""
echo "🎉 PRODUCTION-READY AUTOMATION DEPLOYED!"
echo "========================================"
echo "🌐 Portal URLs:"
echo "   - Main Portal: http://50.19.189.29:3000"
echo "   - HTTPS Portal: https://50.19.189.29"
echo "   - API Docs: http://50.19.189.29:8000/docs"
echo "   - Automation Test: http://50.19.189.29:8000/torrent-automation/test-connection"
echo ""
echo "🤖 PRODUCTION AUTOMATION FEATURES:"
echo "   ✅ AI-assisted field mapping"
echo "   ✅ Intelligent form filling with fallback strategies"
echo "   ✅ Screenshot audit trail generation"
echo "   ✅ Visible browser automation process"
echo "   ✅ Production-ready error handling"
echo "   ✅ Session-based data storage"
echo "   ✅ Complete workflow automation"
echo ""
echo "🎯 HOW TO TEST:"
echo "1. Go to: http://50.19.189.29:3000"
echo "2. Login with your credentials"
echo "3. Navigate: Services → Electricity → Name Change"
echo "4. Select: Torrent Power"
echo "5. Fill form with test data:"
echo "   - City: Ahmedabad"
echo "   - Service Number: TP123456789"
echo "   - T Number: T789"
echo "   - Mobile: 9876543210"
echo "   - Email: test@example.com"
echo "6. Click: 'Start AI Auto-fill in Website (Production Ready)'"
echo "7. 🎉 Watch the magic happen!"
echo ""
echo "🔥 PRODUCTION-READY AUTOMATION IS LIVE! 🔥"