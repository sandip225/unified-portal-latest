#!/bin/bash

echo "🚀 Deploying India Portal with Browser Automation..."

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker compose -f docker-compose.prod.yml down

# Generate SSL certificate
echo "🔐 Generating SSL certificate..."
bash generate-ssl-cert.sh

# Build and start containers with browser-use
echo "🔨 Building and starting containers..."
docker compose -f docker-compose.prod.yml up --build -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 30

# Check container status
echo "📊 Container status:"
docker compose -f docker-compose.prod.yml ps

# Test browser-use installation
echo "🧪 Testing browser-use installation..."
docker compose -f docker-compose.prod.yml exec backend python -c "
try:
    from browser_use import Agent, Browser
    print('✅ browser-use imported successfully')
except ImportError as e:
    print(f'❌ browser-use import failed: {e}')
"

echo ""
echo "🎉 Deployment completed!"
echo "🌐 Portal URLs:"
echo "   - HTTP:  http://50.19.189.29:3000"
echo "   - HTTPS: https://50.19.189.29 (accept certificate warning)"
echo "   - API:   http://50.19.189.29:8000/docs"
echo ""
echo "🤖 Browser automation is now available!"
echo "📝 Test automation by creating a new connection in the portal"