# Deploy India Portal with Browser Automation
Write-Host "🚀 Deploying India Portal with Browser Automation..." -ForegroundColor Green

# Stop existing containers
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Yellow
docker compose -f docker-compose.prod.yml down

# Generate SSL certificate
Write-Host "🔐 Generating SSL certificate..." -ForegroundColor Cyan

# Create SSL directory
if (!(Test-Path "ssl")) {
    New-Item -ItemType Directory -Path "ssl"
}

# Generate SSL certificate using OpenSSL (if available) or create dummy files
try {
    # Generate private key
    openssl genrsa -out ssl/key.pem 2048
    
    # Generate certificate
    openssl req -new -x509 -key ssl/key.pem -out ssl/cert.pem -days 365 -subj "/C=IN/ST=Gujarat/L=Ahmedabad/O=IndiaPortal/CN=50.19.189.29"
    
    Write-Host "✅ SSL certificate generated successfully!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ OpenSSL not found. Creating dummy SSL files..." -ForegroundColor Yellow
    
    # Create dummy SSL files for development
    @"
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKB
wQNneCjGCYw4JUKVdnompnYnWjjrQnXKxfD2jJo4tINb9ljTedWfqg4P4SgRcqhM
vWwHdAHGOjo+VOKpjweGknFP2CFIqak1hrV6xtIBe2XHY3jMxLMoMWuHs2xt4J3A
oAoRwxQG/nHgui7f3C+y7O8UBwc6yq2s5kRi8fDbxgZqd2uyVSMMMcQhcQdNycsz
oGxjjxMjnVT8AbAHXdxtPgRSAuDbvpgjXgBXrfB2FeNd1AoGBAOjIwFFYQwjjWZx
hof7GmdHxmg1reacyDVw/ky1gHQqQGSGT0f1ROhK1wL7wN4tchnocdlDvLsAcFqB
dBPlOr9w
-----END PRIVATE KEY-----
"@ | Out-File -FilePath "ssl/key.pem" -Encoding ASCII

    @"
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAJC1HiIAZAiIMA0GCSqGSIb3DQEBBQUAMEUxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQwHhcNMTIwOTEyMjE1MjAyWhcNMTUwOTEyMjE1MjAyWjBF
MQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50
ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEAwUdHPiQnlWZMhEVEM32fbdhR5j6N859j2SuAGxIzwWFwB7kcQ4FFMjBA
uLiTcbPjzrQntVudKe6NiUqH0aloqAdE7cyoRaLOuBq6TQHcmEsXMk4PS24hRh6V
mROhYmEjzyGkDr0A0Aw93xRN4XQPiHDI1BqkW+oqsHWMchO4DtVkqzqOo+dLpAqf
tnmZtsywiLZNXpmS+VjCSPiOhVx24IeYgQn7nnpbS657njm1Z5wpAz7YAMQBBx6b
87uRtPpwSqcQpFdvFuwAmBBhxtolD5OjbQoBbvVFjmUjrdOgHPfuUxancJAjvx1f
xqvQIx2jzw==
-----END CERTIFICATE-----
"@ | Out-File -FilePath "ssl/cert.pem" -Encoding ASCII
    
    Write-Host "✅ Dummy SSL files created for development!" -ForegroundColor Green
}

# Build and start containers
Write-Host "🔨 Building and starting containers..." -ForegroundColor Cyan
docker compose -f docker-compose.prod.yml up --build -d

# Wait for services to start
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check container status
Write-Host "📊 Container status:" -ForegroundColor Cyan
docker compose -f docker-compose.prod.yml ps

Write-Host ""
Write-Host "🎉 Deployment completed!" -ForegroundColor Green
Write-Host "🌐 Portal URLs:" -ForegroundColor Cyan
Write-Host "   - HTTP:  http://50.19.189.29:3000" -ForegroundColor White
Write-Host "   - HTTPS: https://50.19.189.29 (accept certificate warning)" -ForegroundColor White
Write-Host "   - API:   http://50.19.189.29:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "🤖 Browser automation is now available!" -ForegroundColor Green
Write-Host "📝 Test automation by creating a new connection in the portal" -ForegroundColor Yellow