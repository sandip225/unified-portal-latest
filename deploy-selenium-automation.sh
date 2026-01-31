#!/bin/bash

echo "🚀 Deploying India Portal with Selenium Browser Automation..."

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker compose -f docker-compose.prod.yml down

# Generate SSL certificate
echo "🔐 Generating SSL certificate..."
bash generate-ssl-cert.sh

# Build and start containers with Selenium
echo "🔨 Building and starting containers with Selenium..."
docker compose -f docker-compose.prod.yml up --build -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 30

# Check container status
echo "📊 Container status:"
docker compose -f docker-compose.prod.yml ps

# Test Selenium installation
echo "🧪 Testing Selenium installation..."
docker compose -f docker-compose.prod.yml exec backend python -c "
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    print('✅ Selenium imported successfully')
    
    from webdriver_manager.chrome import ChromeDriverManager
    print('✅ ChromeDriverManager available')
    
    print('✅ Selenium automation ready!')
except ImportError as e:
    print(f'❌ Selenium import failed: {e}')
"

echo ""
echo "🎉 Selenium Deployment completed!"
echo "🌐 Portal URLs:"
echo "   - HTTP:  http://50.19.189.29:3000"
echo "   - HTTPS: https://50.19.189.29 (accept certificate warning)"
echo "   - API:   http://50.19.189.29:8000/docs"
echo ""
echo "🤖 Selenium browser automation is now available!"
echo "✅ Benefits:"
echo "   - No OpenAI API key required"
echo "   - Faster and more reliable"
echo "   - Visible browser automation"
echo "   - Free to use"
echo ""
echo "📝 Test automation by creating a new connection in the portal"