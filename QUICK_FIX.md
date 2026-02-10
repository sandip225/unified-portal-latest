# ⚡ Quick Fix - 405 Error

## The Problem
You were accessing: `http://18.207.167.97:3003` ❌
This bypasses Nginx and causes 405 errors.

## The Solution
Access: `http://18.207.167.97` ✅
(Port 80 - goes through Nginx)

---

## Deploy on EC2

```bash
# SSH to EC2
ssh -i your-key.pem ubuntu@18.207.167.97

# Navigate to project
cd gujarat-unified-services-portal

# Pull changes
git pull origin main

# Deploy
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check status
docker-compose ps
```

---

## Test

```bash
# Should return JSON
curl http://localhost/health

# Should return HTML
curl http://localhost/
```

---

## Access

**Correct:** http://18.207.167.97
**Wrong:** http://18.207.167.97:3003

---

## What Changed

1. ✅ Added Nginx to docker-compose
2. ✅ Nginx runs on port 80
3. ✅ Backend/Frontend are internal only
4. ✅ All requests go through Nginx proxy

---

## Security Group

Only need port 80 open now:
- Port 80 (HTTP) ✅
- Port 443 (HTTPS) ✅
- Port 22 (SSH) ✅
- Port 3003 ❌ (close it)
- Port 8000 ❌ (close it)

---

That's it! Access on port 80 and everything works.
