# 🚀 Setup Guide

Ye guide aapko batayega ki is project ko apne system pe kaise setup karna hai. Windows aur Linux dono ke liye instructions hain.

## 📋 Prerequisites

### Required Software

#### For All Platforms
- **Git**: Code download karne ke liye
- **Text Editor**: VS Code recommended

#### For Docker Setup (Recommended)
- **Docker Desktop** (Windows/Linux)
- **Docker Compose**

#### For Local Development
- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 15+**

---

## 💻 Windows Setup

### Option 1: Docker Setup (Recommended)

#### Step 1: Required Software Install Karo
```bash
# 1. Git Install (agar nahi hai)
# Download: https://git-scm.com/download/win
git --version

# 2. Docker Desktop Install
# Download: https://www.docker.com/products/docker-desktop
docker --version
docker-compose --version
```

#### Step 2: Project Download Karo
```bash
# Project clone karo
git clone https://github.com/LAIBAASIM555/AI-powered-Resume-Optimization-and-Job-Description-Alignment-SaaS-Application.git
cd AI-powered-Resume-Optimization-and-Job-Description-Alignment-SaaS-Application
```

#### Step 3: Application Start Karo
```bash
# Saari services start karo
docker-compose up --build

# Ya background me run karo
docker-compose up -d --build
```

#### Step 4: Application Access Karo
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Option 2: Local Development Setup

#### Step 1: Python Install Karo
```bash
# Python 3.11+ download karo
# https://python.org/downloads/
python --version
pip --version
```

#### Step 2: Node.js Install Karo
```bash
# Node.js 18+ download karo
# https://nodejs.org/
node --version
npm --version
```

#### Step 3: PostgreSQL Install Karo
```bash
# PostgreSQL 15+ download karo
# https://postgresql.org/download/windows/
# Ya Docker use karo
docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=password123 postgres:15-alpine
```

#### Step 4: Project Setup Karo
```bash
# Project clone karo
git clone https://github.com/LAIBAASIM555/AI-powered-Resume-Optimization-and-Job-Description-Alignment-SaaS-Application.git
cd AI-powered-Resume-Optimization-and-Job-Description-Alignment-SaaS-Application
```

#### Step 5: Backend Setup Karo
```bash
cd backend

# Virtual environment create karo
python -m venv venv
venv\Scripts\activate

# Dependencies install karo
pip install -r requirements.txt

# spaCy model download karo
python -m spacy download en_core_web_sm

# Database tables create karo
python -c "from app.models.user import User; from app.models.resume import Resume; from app.models.job import JobDescription; from app.models.analysis import Analysis; from app.db.database import engine; from app.db.base import Base; Base.metadata.create_all(bind=engine); print('Tables created')"
```

#### Step 6: Frontend Setup Karo
```bash
cd ../frontend

# Dependencies install karo
npm install

# Development server start karo
npm run dev
```

#### Step 7: Backend Server Start Karo
```bash
# New terminal me
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Step 8: Application Access Karo
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🐧 Linux Setup

### Option 1: Docker Setup (Recommended)

#### Step 1: Required Software Install Karo
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install git curl

# Docker install karo
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl start docker
sudo systemctl enable docker

# Docker Compose install karo
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Current user ko docker group me add karo
sudo usermod -aG docker $USER
# Logout aur login karo
```

#### Step 2: Project Download Karo
```bash
# Project clone karo
git clone https://github.com/LAIBAASIM555/AI-powered-Resume-Optimization-and-Job-Description-Alignment-SaaS-Application.git
cd AI-powered-Resume-Optimization-and-Job-Description-Alignment-SaaS-Application
```

#### Step 3: Application Start Karo
```bash
# Saari services start karo
docker-compose up --build

# Ya background me run karo
docker-compose up -d --build
```

#### Step 4: Application Access Karo
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Option 2: Local Development Setup

#### Step 1: Python Install Karo
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# CentOS/RHEL
sudo yum install python311 python311-pip
```

#### Step 2: Node.js Install Karo
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# CentOS/RHEL
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs
```

#### Step 3: PostgreSQL Install Karo
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# PostgreSQL start karo
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Database create karo
sudo -u postgres psql
CREATE DATABASE resume_optimizer;
\q

# Ya Docker use karo
sudo docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=password123 postgres:15-alpine
```

#### Step 4: Project Setup Karo
```bash
# Project clone karo
git clone https://github.com/LAIBAASIM555/AI-powered-Resume-Optimization-and-Job-Description-Alignment-SaaS-Application.git
cd AI-powered-Resume-Optimization-and-Job-Description-Alignment-SaaS-Application
```

#### Step 5: Backend Setup Karo
```bash
cd backend

# Virtual environment create karo
python3 -m venv venv
source venv/bin/activate

# Dependencies install karo
pip install -r requirements.txt

# spaCy model download karo
python -m spacy download en_core_web_sm

# Database tables create karo
python -c "from app.models.user import User; from app.models.resume import Resume; from app.models.job import JobDescription; from app.models.analysis import Analysis; from app.db.database import engine; from app.db.base import Base; Base.metadata.create_all(bind=engine); print('Tables created')"
```

#### Step 6: Frontend Setup Karo
```bash
cd ../frontend

# Dependencies install karo
npm install

# Development server start karo
npm run dev
```

#### Step 7: Backend Server Start Karo
```bash
# New terminal me
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Step 8: Application Access Karo
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🔧 Environment Configuration

### .env File Setup
Backend directory me `.env` file create karo:

```bash
# Database
DATABASE_URL=postgresql://postgres:password123@localhost:5432/resume_optimizer

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Application
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost

# File Upload
UPLOAD_DIR=uploads
MAX_FILE_SIZE=5242880
ALLOWED_EXTENSIONS=pdf,docx
```

---

## 🐛 Troubleshooting

### Common Issues

#### Docker Issues
```bash
# Docker permission error
sudo usermod -aG docker $USER
# Logout aur login karo

# Port already in use
docker-compose down
docker-compose up -d

# Build cache clear karo
docker system prune -a
```

#### Python Issues
```bash
# Virtual environment activate karo
# Windows
venv\Scripts\activate
# Linux
source venv/bin/activate

# Dependencies reinstall karo
pip install -r requirements.txt --force-reinstall
```

#### Database Issues
```bash
# PostgreSQL status check karo
sudo systemctl status postgresql

# Database connect karo
psql -U postgres -d resume_optimizer

# Tables check karo
\dt
```

#### Port Issues
```bash
# Check which ports are in use
# Windows
netstat -ano | findstr :8000
# Linux
lsof -i :8000

# Port kill karo
# Windows
taskkill /PID <PID> /F
# Linux
kill -9 <PID>
```

---

## 📱 Mobile Testing

Application responsive hai aur mobile devices pe bhi kaam karta hai:

- **Chrome DevTools**: Mobile view test karne ke liye
- **BrowserStack**: Different devices pe test karne ke liye
- **Responsiveness**: 320px se 1920px+ tak support

---

## 🔐 Security Setup

### Production Environment
```bash
# Strong secret key generate karo
openssl rand -hex 32

# SSL certificate setup karo
# Let's Encrypt use karo free certificates ke liye

# Environment variables set karo
export SECRET_KEY="your-secure-key"
export DEBUG=False
export DATABASE_URL="your-production-db-url"
```

---

## 📊 Monitoring Setup

### Health Checks
```bash
# API health check
curl http://localhost:8000/health

# Database health check
docker exec resume_db pg_isready -U postgres -d resume_optimizer
```

### Logs Check Karo
```bash
# Backend logs
docker-compose logs backend

# Frontend logs
docker-compose logs frontend

# Database logs
docker-compose logs db
```

---

## 🎯 Quick Verification

Setup complete hone ke baad ye commands run karo:

```bash
# 1. Services status check karo
docker ps

# 2. API health check karo
curl http://localhost:8000/health

# 3. Frontend access karo
curl http://localhost

# 4. Database connection check karo
docker exec resume_db psql -U postgres -d resume_optimizer -c "SELECT COUNT(*) FROM users;"
```

---

## 📞 Support

Agar koi problem aye to:

1. **Logs check karo**: `docker-compose logs`
2. **Services restart karo**: `docker-compose restart`
3. **Cache clear karo**: `docker system prune`
4. **Documentation check karo**: README.md, TESTING_GUIDE.md
5. **GitHub issues check karo**: Repository me issues dekhiye

---

**Note**: Docker setup recommended hai kyunki ye sab kuch automatically handle karta hai aur dependencies conflicts se bachata hai.