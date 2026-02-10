# 🔧 Current Deployment Fix - UPDATED

## Problem Identified
- Frontend trying to connect to port 3003 instead of going through Nginx
- **Root Cause**: Nginx was NOT included in docker-compose
- Requests going to `http://18.207.167.97:3003/api` (frontend port) instead of `http://18.207.167.97/api` (Nginx port)
- Result: 405 Not Allowed error

## Solution Applied

### 1. Added Nginx to Docker Compose
- Added Nginx service to `docker-compose.yml`
- Nginx now runs on port 80 and proxies to backend/frontend
- Backend and frontend are now internal (not exposed directly)

### 2. Fixed Port Mappings
**Before:**
- Frontend: `3003:80` (exposed directly)
- Backend: `8000:8000` (exposed directly)
- Nginx: Not in docker-compose

**After:**
- Nginx: `80:80` (main entry point)
- Frontend: Internal only (accessed via Nginx)
- Backend: Internal only (accessed via Nginx)

### 3. Updated Nginx Config
- Changed server_name to `18.207.167.97`
- Proper proxy configuration for `/api` routes

### 4. Fixed API Configuration
- Frontend uses relative paths (`/api`) in production
- Works automatically through Nginx proxy

---

## 🚀 Deploy the Fix

### On EC2 Instance

```bash
# 1. SSH to EC2
ssh -i your-key.pem ubuntu@18.207.167.97

# 2. Navigate to project
cd gujarat-unified-services-portal

# 3. Pull latest changes
git pull origin main

# 4. Run deployment script
chmod +x deploy-fix.sh
./deploy-fix.sh

# OR manually:
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# 5. Check status
docker-compose ps
docker-compose logs -f
```

### On Windows (Local Testing)

```cmd
REM Run the deployment script
deploy-fix.bat

REM OR manually:
docker-compose down
docker-compose build --no-cache
docker-compose up -d
docker-compose ps
```

---

## 🔍 Verify Deployment

### 1. Check All Services Running
```bash
docker-compose ps

# Should show:
# - gujarat-portal-nginx (port 80)
# - gujarat-portal-frontend (internal)
# - gujarat-portal-backend (internal)
```

### 2. Test Endpoints
```bash
# Health check (should return JSON)
curl http://localhost/health

# API docs (should return HTML)
curl http://localhost/docs

# Frontend (should return HTML)
curl http://localhost/
```

### 3. Test from Browser
1. Open: `http://18.207.167.97` (NOT port 3003!)
2. Open browser console (F12)
3. Try to register/login
4. Check Network tab - requests should go to `/api/auth/register` (relative path)
5. Should see 200 OK, not 405

---

## 🔒 AWS Security Group

Only port 80 needs to be open now:

| Port | Protocol | Source | Purpose |
|------|----------|--------|---------|
| 80 | TCP | 0.0.0.0/0 | HTTP (Nginx) |
| 443 | TCP | 0.0.0.0/0 | HTTPS (future) |
| 22 | TCP | Your IP | SSH |

**You can CLOSE ports 3003 and 8000** - they're now internal only!

---

## 🐛 Troubleshooting

### Still Getting 405 Error
```bash
# Make sure you're accessing port 80, not 3003
# WRONG: http://18.207.167.97:3003
# RIGHT: http://18.207.167.97

# Check Nginx is running
docker-compose ps | grep nginx

# Check Nginx logs
docker-compose logs nginx
```

### Nginx Not Starting
```bash
# Check configuration
docker-compose exec nginx nginx -t

# View logs
docker-compose logs nginx

# Restart
docker-compose restart nginx
```

### Backend Not Responding
```bash
# Check backend logs
docker-compose logs backend

# Test backend directly (from inside container)
docker-compose exec backend curl http://localhost:8000/health
```

### Clear Browser Cache
```javascript
// In browser console
localStorage.clear()
sessionStorage.clear()
location.reload(true)
```

---

## ✅ Expected Result

After deployment:
- ✅ Access site at `http://18.207.167.97` (port 80)
- ✅ API requests go to `/api/*` (relative paths)
- ✅ Nginx proxies to backend/frontend
- ✅ No 405 errors
- ✅ Login/Register works
- ✅ Service Worker registers successfully

---

## 📊 Architecture

```
Internet
    ↓
Port 80 (Nginx)
    ↓
    ├─→ /api/* → Backend (internal port 8000)
    ├─→ /docs → Backend docs
    ├─→ /health → Backend health
    └─→ /* → Frontend (internal port 80)
```

---

## 📝 Files Changed

1. **docker-compose.yml** - Added Nginx service, changed port mappings
2. **nginx.conf** - Updated server_name to 18.207.167.97
3. **frontend/src/api/axios.js** - Use relative paths in production
4. **frontend/vite.config.js** - Fixed Service Worker registration
5. **deploy-fix.sh** - Deployment script for Linux
6. **deploy-fix.bat** - Deployment script for Windows

---

## 🎯 Next Steps

1. **Deploy to EC2** using commands above
2. **Access at port 80** (not 3003!)
3. **Test registration/login**
4. **Close ports 3003 and 8000** in security group
5. **Set up HTTPS** (optional, for production)

---

**Status:** Ready to deploy
**Access URL:** http://18.207.167.97 (port 80 only!)
**Key Fix:** Nginx now in docker-compose, proper port routing
