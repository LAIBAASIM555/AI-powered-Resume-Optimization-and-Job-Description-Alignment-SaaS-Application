# 💻 Terminal Commands Guide

Ye guide aapko batayegi ki project ke saath kaam karte waqt kaunse terminal commands use karne hain.

## 📋 Quick Reference

### Docker Commands
```bash
# Project start karo
docker-compose up -d

# Project stop karo
docker-compose down

# Logs check karo
docker-compose logs -f

# Services restart karo
docker-compose restart

# Build karo (code changes ke baad)
docker-compose up -d --build
```

### Development Commands
```bash
# Backend server start karo
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Frontend server start karo
cd frontend && npm run dev

# Tests run karo
cd backend && python -m pytest

# Database migrations run karo
cd backend && alembic upgrade head
```

---

## 🐳 Docker Commands Detail

### Basic Docker Operations

#### Project Start Karna
```bash
# Foreground me (logs dekhne ke liye)
docker-compose up

# Background me (recommended)
docker-compose up -d

# Specific service start karna
docker-compose up backend
docker-compose up frontend
docker-compose up db
```

#### Project Stop Karna
```bash
# Saare services stop karo
docker-compose down

# Volumes bhi delete karo (data loss hoga)
docker-compose down -v

# Specific service stop karo
docker-compose stop backend
```

#### Logs Dekhna
```bash
# Saare services ke logs
docker-compose logs

# Real-time logs (follow mode)
docker-compose logs -f

# Specific service ke logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Last 100 lines
docker-compose logs --tail=100 backend
```

#### Services Status Check Karna
```bash
# Running containers dekho
docker ps

# Saare containers dekho (stopped bhi)
docker ps -a

# Specific container details
docker inspect resume_backend
```

### Advanced Docker Commands

#### Build aur Rebuild
```bash
# Force rebuild (cache ignore karke)
docker-compose build --no-cache

# Specific service rebuild karo
docker-compose build backend

# Build context size check karo
docker build --progress=plain .
```

#### Container Management
```bash
# Container me enter karo
docker exec -it resume_backend bash

# Container restart karo
docker-compose restart backend

# Container remove karo
docker rm resume_backend

# Images cleanup karo
docker image prune -f
```

#### Database Operations
```bash
# Database backup
docker exec resume_db pg_dump -U postgres resume_optimizer > backup.sql

# Database restore
docker exec -i resume_db psql -U postgres resume_optimizer < backup.sql

# Database shell access
docker exec -it resume_db psql -U postgres -d resume_optimizer
```

---

## 🐍 Python Backend Commands

### Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate
deactivate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
deactivate
```

### Dependencies Management
```bash
# Requirements install karo
pip install -r requirements.txt

# Specific package install karo
pip install fastapi uvicorn

# Package upgrade karo
pip install --upgrade fastapi

# Installed packages list dekho
pip list

# Requirements file generate karo
pip freeze > requirements.txt
```

### Server Operations
```bash
# Development server
uvicorn app.main:app --reload

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Workers ke saath
uvicorn app.main:app --workers 4

# HTTPS enable karo
uvicorn app.main:app --ssl-keyfile key.pem --ssl-certfile cert.pem
```

### Database Operations
```bash
# Tables create karo
python -c "from app.db.base import Base; from app.db.database import engine; Base.metadata.create_all(bind=engine)"

# Alembic migration create karo
alembic revision -m "Add new table"

# Migration run karo
alembic upgrade head

# Migration rollback karo
alembic downgrade -1
```

### Testing Commands
```bash
# Saare tests run karo
pytest

# Specific test file run karo
pytest tests/test_auth.py

# Verbose output ke saath
pytest -v

# Coverage report generate karo
pytest --cov=app --cov-report=html

# Specific test function run karo
pytest tests/test_auth.py::test_register_user -v
```

---

## ⚛️ Frontend Commands

### Dependencies Management
```bash
# Dependencies install karo
npm install

# Specific package install karo
npm install axios react-router-dom

# Development dependency install karo
npm install --save-dev @types/react

# Package uninstall karo
npm uninstall lodash
```

### Development Server
```bash
# Development server start karo
npm run dev

# Specific port pe start karo
npm run dev -- --port 3000

# Host expose karo
npm run dev -- --host 0.0.0.0
```

### Build Commands
```bash
# Production build create karo
npm run build

# Build preview karo
npm run preview

# Build analyze karo
npm run build -- --analyze
```

### Testing Commands
```bash
# Tests run karo
npm test

# Watch mode me tests run karo
npm run test:watch

# Coverage report generate karo
npm run test:coverage

# Specific test file run karo
npm test -- LoginPage.test.jsx
```

---

## 🗄️ Database Commands

### PostgreSQL Direct Commands
```bash
# Database connect karo
psql -U postgres -d resume_optimizer

# Tables list dekho
\dt

# Table structure dekho
\d users

# Query run karo
SELECT * FROM users LIMIT 5;

# Database size check karo
SELECT pg_size_pretty(pg_database_size('resume_optimizer'));

# Active connections dekho
SELECT * FROM pg_stat_activity;
```

### Database Backup/Restore
```bash
# Backup create karo
pg_dump -U postgres -d resume_optimizer > backup.sql

# Backup restore karo
psql -U postgres -d resume_optimizer < backup.sql

# Compressed backup
pg_dump -U postgres -d resume_optimizer | gzip > backup.sql.gz

# Compressed backup restore
gunzip -c backup.sql.gz | psql -U postgres -d resume_optimizer
```

---

## 🔧 Git Commands

### Basic Git Operations
```bash
# Repository clone karo
git clone <repository-url>

# Status check karo
git status

# Changes add karo
git add .

# Commit karo
git commit -m "Your commit message"

# Push karo
git push origin main

# Pull karo
git pull origin main
```

### Branch Management
```bash
# New branch create karo
git checkout -b feature/new-feature

# Branch switch karo
git checkout main

# Branches list dekho
git branch -a

# Branch delete karo
git branch -d feature/old-feature
```

### Advanced Git
```bash
# Changes stash karo
git stash

# Stash apply karo
git stash pop

# Remote add karo
git remote add origin <url>

# Log dekho
git log --oneline

# Diff dekho
git diff
```

---

## 📊 Monitoring Commands

### System Monitoring
```bash
# Disk usage dekho
df -h

# Memory usage dekho
free -h

# CPU usage dekho
top
htop

# Process list dekho
ps aux
```

### Docker Monitoring
```bash
# Container resource usage dekho
docker stats

# System disk usage dekho
docker system df

# Logs size dekho
docker system df -v

# Events dekho
docker events
```

### Network Monitoring
```bash
# Open ports dekho
netstat -tlnp
ss -tlnp

# Port check karo
telnet localhost 8000

# Ping test karo
ping localhost
```

---

## 🐛 Debugging Commands

### Log Analysis
```bash
# Recent logs dekho
tail -f /var/log/application.log

# Error logs search karo
grep "ERROR" /var/log/application.log

# Last 100 lines dekho
tail -100 /var/log/application.log
```

### Process Debugging
```bash
# Process find karo
ps aux | grep python

# Process kill karo
kill -9 <PID>

# Process details dekho
ps -p <PID> -o pid,ppid,cmd,%cpu,%mem
```

### Network Debugging
```bash
# DNS resolution check karo
nslookup localhost

# Connection test karo
curl -v http://localhost:8000/health

# Firewall rules dekho
iptables -L
ufw status
```

---

## 🚀 Deployment Commands

### Production Deployment
```bash
# Environment variables set karo
export SECRET_KEY="your-secret-key"
export DATABASE_URL="your-db-url"
export DEBUG=False

# Application start karo
docker-compose -f docker-compose.prod.yml up -d

# SSL certificate renew karo
certbot renew

# Nginx reload karo
nginx -s reload
```

### Backup Commands
```bash
# Full backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker exec resume_db pg_dump -U postgres resume_optimizer > backup_$DATE.sql
docker exec resume_backend tar czf /app/uploads_$DATE.tar.gz /app/uploads
echo "Backup completed: backup_$DATE.sql, uploads_$DATE.tar.gz"
```

---

## 📝 Useful Aliases

Terminal me ye aliases add karo productivity ke liye:

```bash
# .bashrc or .zshrc me add karo

# Docker aliases
alias dcu='docker-compose up -d'
alias dcd='docker-compose down'
alias dcl='docker-compose logs -f'
alias dcr='docker-compose restart'

# Git aliases
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push origin main'

# Python aliases
alias ve='source venv/bin/activate'
alias da='deactivate'

# Project specific
alias start='docker-compose up -d'
alias stop='docker-compose down'
alias logs='docker-compose logs -f'
alias backend='docker exec -it resume_backend bash'
alias db='docker exec -it resume_db psql -U postgres -d resume_optimizer'
```

---

## ⚡ Quick Commands Reference

### Daily Development
```bash
# Start working
dcu                    # docker-compose up -d
dcl                    # docker-compose logs -f

# Code changes
dcd                    # docker-compose down
dcu --build          # docker-compose up -d --build

# Testing
pytest                # Run backend tests
npm test             # Run frontend tests

# Database
db                    # Connect to database
\dt                   # List tables
SELECT * FROM users; # Query users
```

### Emergency Commands
```bash
# Full reset
docker-compose down -v
docker system prune -f
docker-compose up -d --build

# Quick restart
docker-compose restart

# Logs clear karo
truncate -s 0 /var/log/application.log

# Cache clear karo
docker system prune -f
npm cache clean --force
pip cache purge
```

---

## 🎯 Command Categories

### 🔨 Development
- `docker-compose up -d` - Project start karo
- `npm run dev` - Frontend development
- `uvicorn app.main:app --reload` - Backend development
- `pytest` - Tests run karo

### 📦 Deployment
- `docker-compose build` - Images build karo
- `docker-compose push` - Images push karo
- `docker-compose pull` - Images pull karo

### 🔍 Monitoring
- `docker stats` - Resource usage dekho
- `docker-compose logs -f` - Real-time logs
- `docker ps` - Container status

### 🛠️ Maintenance
- `docker system prune` - Cleanup karo
- `docker volume prune` - Volumes cleanup
- `docker image prune` - Images cleanup

---

**Tip**: Commands ko yaad rakhne ke liye cheatsheet create karo ya aliases use karo!