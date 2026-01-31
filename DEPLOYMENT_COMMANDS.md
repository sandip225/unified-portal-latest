# India Portal Deployment Commands

## Quick Deployment with Browser Automation

### For Linux/Mac:
```bash
# Deploy with browser automation and SSL
bash deploy-browser-automation.sh
```

### For Windows:
```powershell
# Deploy with browser automation and SSL
.\deploy-browser-automation.ps1
```

## Manual Deployment Steps

### 1. Stop existing containers
```bash
docker compose -f docker-compose.prod.yml down
```

### 2. Generate SSL certificate
```bash
bash generate-ssl-cert.sh
```

### 3. Build and start containers
```bash
docker compose -f docker-compose.prod.yml up --build -d
```

### 4. Check status
```bash
docker compose -f docker-compose.prod.yml ps
```

## Portal URLs
- **HTTP**: http://50.19.189.29:3000
- **HTTPS**: https://50.19.189.29 (accept certificate warning)
- **API Docs**: http://50.19.189.29:8000/docs

## Browser Automation Features
- ✅ AI-powered form filling
- ✅ Visible browser automation
- ✅ Torrent Power integration
- ✅ Government portal support
- ✅ OpenAI GPT-4 powered

## Troubleshooting

### Browser automation not working:
```bash
# Check browser-use installation
docker compose -f docker-compose.prod.yml exec backend python -c "from browser_use import Agent; print('✅ browser-use working')"

# Check OpenAI API key
docker compose -f docker-compose.prod.yml exec backend python -c "import os; print('API Key:', os.getenv('OPENAI_API_KEY')[:20] + '...')"
```

### SSL certificate issues:
```bash
# Regenerate SSL certificate
bash generate-ssl-cert.sh
docker compose -f docker-compose.prod.yml restart nginx
```

### Container logs:
```bash
# Backend logs
docker compose -f docker-compose.prod.yml logs backend

# Frontend logs  
docker compose -f docker-compose.prod.yml logs frontend

# Nginx logs
docker compose -f docker-compose.prod.yml logs nginx
```