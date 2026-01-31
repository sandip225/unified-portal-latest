#!/bin/bash

echo "🔧 Fixing Browser Automation and SSL Issues..."

# Step 1: Update requirements.txt with browser-use
echo "📦 Adding browser-use to requirements..."
if ! grep -q "browser-use" backend/requirements.txt; then
    echo "browser-use==0.1.44" >> backend/requirements.txt
    echo "✅ browser-use added to requirements.txt"
else
    echo "✅ browser-use already in requirements.txt"
fi

# Step 2: Generate SSL certificate
echo "🔐 Generating SSL certificate..."
mkdir -p ssl
openssl genrsa -out ssl/key.pem 2048
openssl req -new -key ssl/key.pem -out ssl/cert.csr -subj "/C=IN/ST=Gujarat/L=Ahmedabad/O=IndiaPortal/CN=50.19.189.29"
openssl x509 -req -days 365 -in ssl/cert.csr -signkey ssl/key.pem -out ssl/cert.pem
chmod 600 ssl/key.pem
chmod 644 ssl/cert.pem
echo "✅ SSL certificate generated"

# Step 3: Stop existing containers
echo "🛑 Stopping existing containers..."
docker compose -f docker-compose.prod.yml down

# Step 4: Rebuild with browser-use
echo "🔨 Rebuilding containers with browser-use..."
docker compose -f docker-compose.prod.yml build --no-cache backend

# Step 5: Start all services
echo "🚀 Starting all services..."
docker compose -f docker-compose.prod.yml up -d

# Step 6: Wait for services
echo "⏳ Waiting for services to start..."
sleep 45

# Step 7: Test browser-use installation
echo "🧪 Testing browser-use installation..."
docker compose -f docker-compose.prod.yml exec -T backend python -c "
try:
    from browser_use import Agent, Browser
    print('✅ browser-use imported successfully')
except ImportError as e:
    print(f'❌ browser-use import failed: {e}')
"

# Step 8: Check container status
echo "📊 Container status:"
docker compose -f docker-compose.prod.yml ps

echo ""
echo "🎉 Fix completed!"
echo "🌐 Portal URLs:"
echo "   - HTTP:  http://50.19.189.29:3000"
echo "   - HTTPS: https://50.19.189.29 (accept certificate warning)"
echo "   - API:   http://50.19.189.29:8000/docs"
echo ""
echo "🤖 Browser automation should now work!"
echo "📝 Test by creating a new connection in the portal"