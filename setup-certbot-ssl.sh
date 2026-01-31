#!/bin/bash

# 🔒 Certbot SSL Certificate Setup Script
# This script sets up Let's Encrypt SSL certificates using Certbot

echo "🔒 Setting up Certbot SSL certificates..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get domain and email from user
echo -e "${YELLOW}📋 SSL Certificate Setup${NC}"
echo ""
read -p "Enter your domain name (e.g., mysite.com): " DOMAIN
read -p "Enter your email address: " EMAIL

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo -e "${RED}❌ Domain and email are required!${NC}"
    echo ""
    echo -e "${YELLOW}💡 If you don't have a domain, you can get a free one from:${NC}"
    echo "   - Freenom.com (free .tk, .ml, .ga domains)"
    echo "   - No-IP.com (free subdomain)"
    echo "   - DuckDNS.org (free subdomain)"
    echo ""
    echo -e "${YELLOW}🔧 For now, using enhanced self-signed certificate...${NC}"
    
    # Create enhanced self-signed certificate
    sudo mkdir -p /etc/letsencrypt/live/50.19.189.29
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/letsencrypt/live/50.19.189.29/privkey.pem \
        -out /etc/letsencrypt/live/50.19.189.29/fullchain.pem \
        -subj "/C=IN/ST=Gujarat/L=Ahmedabad/O=India Portal/CN=50.19.189.29"
    
    sudo chmod 600 /etc/letsencrypt/live/50.19.189.29/privkey.pem
    sudo chmod 644 /etc/letsencrypt/live/50.19.189.29/fullchain.pem
    
    # Copy to nginx directory
    sudo mkdir -p /etc/nginx/ssl
    sudo cp /etc/letsencrypt/live/50.19.189.29/fullchain.pem /etc/nginx/ssl/cert.pem
    sudo cp /etc/letsencrypt/live/50.19.189.29/privkey.pem /etc/nginx/ssl/key.pem
    
    echo -e "${GREEN}✅ Enhanced self-signed certificate created${NC}"
    exit 0
fi

echo ""
echo -e "${YELLOW}📋 Configuration:${NC}"
echo "   Domain: $DOMAIN"
echo "   Email: $EMAIL"
echo ""

# Install Certbot
echo -e "${YELLOW}📦 Installing Certbot...${NC}"
sudo apt update
sudo apt install -y certbot python3-certbot-nginx

# Stop nginx temporarily
echo -e "${YELLOW}🛑 Stopping nginx temporarily...${NC}"
docker compose -f docker-compose.prod.yml stop nginx

# Get SSL certificate
echo -e "${YELLOW}🔒 Obtaining SSL certificate from Let's Encrypt...${NC}"
echo -e "${YELLOW}⚠️  Make sure your domain $DOMAIN points to this server IP: 50.19.189.29${NC}"
echo ""
read -p "Press Enter when DNS is configured and ready..."

sudo certbot certonly --standalone \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN

# Check if certificate was obtained
if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo -e "${GREEN}✅ SSL certificate obtained successfully!${NC}"
    
    # Copy certificates to nginx directory
    sudo mkdir -p /etc/nginx/ssl
    sudo cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem /etc/nginx/ssl/cert.pem
    sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem /etc/nginx/ssl/key.pem
    
    # Set proper permissions
    sudo chmod 644 /etc/nginx/ssl/cert.pem
    sudo chmod 600 /etc/nginx/ssl/key.pem
    
    echo -e "${GREEN}✅ Certificates copied to nginx directory${NC}"
    
    # Update nginx config with domain
    sed -i "s/50.19.189.29/$DOMAIN/g" nginx.prod.conf
    
    # Setup auto-renewal
    echo -e "${YELLOW}⏰ Setting up auto-renewal...${NC}"
    
    # Create renewal script
    sudo tee /etc/cron.d/certbot-renew > /dev/null <<EOF
0 12 * * * root certbot renew --quiet --post-hook "docker compose -f /opt/india-portal/docker-compose.prod.yml restart nginx"
EOF
    
    echo -e "${GREEN}✅ Auto-renewal configured${NC}"
    
else
    echo -e "${RED}❌ Failed to obtain SSL certificate${NC}"
    echo -e "${YELLOW}🔧 Creating self-signed certificate as fallback...${NC}"
    
    sudo mkdir -p /etc/nginx/ssl
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/nginx/ssl/key.pem \
        -out /etc/nginx/ssl/cert.pem \
        -subj "/C=IN/ST=Gujarat/L=Ahmedabad/O=IndiaPortal/CN=$DOMAIN"
    
    sudo chmod 600 /etc/nginx/ssl/key.pem
    sudo chmod 644 /etc/nginx/ssl/cert.pem
fi

# Start nginx
echo -e "${YELLOW}🚀 Starting nginx with SSL...${NC}"
docker compose -f docker-compose.prod.yml up -d nginx

# Wait for nginx to start
sleep 10

# Test SSL
echo -e "${YELLOW}🧪 Testing SSL configuration...${NC}"
if curl -k -s https://localhost/health > /dev/null; then
    echo -e "${GREEN}✅ HTTPS is working${NC}"
else
    echo -e "${RED}❌ HTTPS test failed${NC}"
fi

echo ""
echo -e "${GREEN}🎉 SSL setup completed!${NC}"
echo ""
echo -e "${YELLOW}🌐 Access your portal:${NC}"
if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo "   HTTPS: https://$DOMAIN (Trusted SSL Certificate)"
    echo "   HTTP:  http://$DOMAIN"
else
    echo "   HTTPS: https://$DOMAIN (Self-signed Certificate)"
    echo "   HTTP:  http://$DOMAIN"
fi
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "   1. Test HTTPS access in browser"
echo "   2. Update frontend environment if needed"
echo "   3. Test browser automation"