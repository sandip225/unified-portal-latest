#!/bin/bash

# Generate SSL certificate for India Portal
echo "🔐 Generating SSL certificate for India Portal..."

# Create SSL directory
mkdir -p ssl

# Generate private key
openssl genrsa -out ssl/key.pem 2048

# Generate certificate signing request
openssl req -new -key ssl/key.pem -out ssl/cert.csr -subj "/C=IN/ST=Gujarat/L=Ahmedabad/O=IndiaPortal/CN=50.19.189.29"

# Generate self-signed certificate
openssl x509 -req -days 365 -in ssl/cert.csr -signkey ssl/key.pem -out ssl/cert.pem

# Set proper permissions
chmod 600 ssl/key.pem
chmod 644 ssl/cert.pem

echo "✅ SSL certificate generated successfully!"
echo "📁 Certificate files:"
echo "   - Private key: ssl/key.pem"
echo "   - Certificate: ssl/cert.pem"
echo ""
echo "🚀 Now you can access the portal with HTTPS (accept the certificate warning)"