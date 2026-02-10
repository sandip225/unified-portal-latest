#!/bin/bash

echo "🔧 Deploying Fixed Configuration..."

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down

# Remove old containers and images (optional - uncomment if needed)
# docker-compose rm -f
# docker system prune -f

# Rebuild with new configuration
echo "Building containers..."
docker-compose build --no-cache

# Start services
echo "Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Check status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🔍 Testing endpoints..."
echo "Backend health:"
curl -s http://localhost/health || echo "❌ Backend not responding"

echo ""
echo "Frontend:"
curl -s -o /dev/null -w "%{http_code}" http://localhost/ || echo "❌ Frontend not responding"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Access your application at:"
echo "  http://18.207.167.97"
echo ""
echo "View logs with:"
echo "  docker-compose logs -f"
