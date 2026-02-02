#!/bin/bash

echo "🚨 EMERGENCY FIX - SQLAlchemy Missing"
echo "===================================="

# Pull latest requirements.txt
git pull origin main

# Stop backend
docker compose -f docker-compose.prod.yml stop backend

# Remove backend image to force rebuild
docker rmi india-portal-backend 2>/dev/null || true

# Rebuild backend with correct dependencies
echo "🔨 Rebuilding backend with SQLAlchemy..."
docker compose -f docker-compose.prod.yml build --no-cache backend

# Start backend
echo "🚀 Starting backend..."
docker compose -f docker-compose.prod.yml up -d backend

# Wait for backend
echo "⏳ Waiting for backend to start..."
sleep 30

# Test backend
echo "🧪 Testing backend..."
curl -s http://localhost:8000/health && echo "✅ Backend working!" || echo "❌ Backend still failing"

# Show logs if still failing
echo ""
echo "📋 Backend logs:"
docker compose -f docker-compose.prod.yml logs --tail=10 backend

echo ""
echo "🌐 Portal should now work:"
echo "   - Portal: http://50.19.189.29:3000"
echo "   - API: http://50.19.189.29:8000/health"