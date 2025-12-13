# 🖥️ Terminal Guide - Running AI Resume Optimizer

Complete step-by-step guide to run the application on Windows PowerShell.

---

## 📋 Prerequisites Check

First, verify you have everything installed:

```powershell
# Check Python version (should be 3.11+)
python --version

# Check Node.js version (should be 18+)
node --version

# Check npm version
npm --version

# Check if PostgreSQL is running (optional - check Services)
```

---

## 🚀 Step-by-Step Setup

### **STEP 1: Open Two Terminal Windows**

You need **TWO** terminal windows:
1. **Terminal 1** - For Backend (FastAPI)
2. **Terminal 2** - For Frontend (React)

---

### **STEP 2: Setup Backend (Terminal 1)**

#### 2.1 Navigate to Backend Directory

```powershell
cd D:\FYP\backend
```

#### 2.2 Activate Virtual Environment

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

**If you get an execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try again:
.\venv\Scripts\Activate.ps1
```

**You should see `(venv)` at the start of your prompt:**
```
(venv) PS D:\FYP\backend>
```

#### 2.3 Verify Dependencies

```powershell
# Check if pydantic-settings is installed
pip list | findstr pydantic-settings
```

**If not installed:**
```powershell
pip install pydantic-settings
```

#### 2.4 Check Database Connection

Make sure PostgreSQL is running and database exists:

```powershell
# Check if database exists (if you have psql installed)
psql -U postgres -c "\l" | findstr resume_optimizer
```

**If database doesn't exist, create it:**
```powershell
# Connect to PostgreSQL
psql -U postgres

# Then in psql prompt:
CREATE DATABASE resume_optimizer;
\q
```

#### 2.5 Create .env File (if not exists)

```powershell
# Check if .env exists
dir .env

# If not, create it:
echo "DATABASE_URL=postgresql://postgres:password123@localhost:5432/resume_optimizer" > .env
echo "SECRET_KEY=your-super-secret-key-change-this-in-production-12345" >> .env
```

#### 2.6 Start Backend Server

```powershell
uvicorn app.main:app --reload
```

**✅ Success looks like:**
```
INFO:     Will watch for changes in these directories: ['D:\\FYP\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**✅ Backend is now running on:** http://localhost:8000

**Keep this terminal window open!**

---

### **STEP 3: Setup Frontend (Terminal 2)**

#### 3.1 Open New Terminal Window

Open a **NEW** PowerShell window (keep Terminal 1 running!)

#### 3.2 Navigate to Frontend Directory

```powershell
cd D:\FYP\frontend
```

#### 3.3 Install Dependencies (First Time Only)

```powershell
# Install all npm packages
npm install
```

**This may take a few minutes. Wait for it to complete.**

#### 3.4 Start Frontend Server

```powershell
npm run dev
```

**✅ Success looks like:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**✅ Frontend is now running on:** http://localhost:5173

**Keep this terminal window open!**

---

## 🎉 Application is Running!

### Access Points:

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## 🧪 Quick Test

1. Open browser: http://localhost:5173
2. Click "Get Started Free"
3. Register a new account
4. Login
5. Upload a resume
6. Add job description
7. Analyze!

---

## 🛑 How to Stop Servers

### Stop Backend (Terminal 1):
```powershell
# Press Ctrl+C in Terminal 1
```

### Stop Frontend (Terminal 2):
```powershell
# Press Ctrl+C in Terminal 2
```

---

## 🔧 Common Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'pydantic_settings'"

**Solution:**
```powershell
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

# Install missing package
pip install pydantic-settings

# Or reinstall all requirements
pip install -r requirements.txt
```

### Issue 2: "Port 8000 already in use"

**Solution:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

### Issue 3: "Port 5173 already in use"

**Solution:**
```powershell
# Find process using port 5173
netstat -ano | findstr :5173

# Kill the process
taskkill /PID <PID> /F
```

### Issue 4: "Database connection error"

**Solution:**
```powershell
# Check PostgreSQL is running
# Windows: Check Services (services.msc) - look for "postgresql"

# Verify database exists
psql -U postgres -c "\l" | findstr resume_optimizer

# If not, create it:
psql -U postgres
CREATE DATABASE resume_optimizer;
\q
```

### Issue 5: "Execution Policy Error"

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 6: "npm install fails"

**Solution:**
```powershell
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

---

## 📝 Complete Command Reference

### Backend Commands (Terminal 1)

```powershell
# Navigate to backend
cd D:\FYP\backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload

# Stop server
Ctrl+C
```

### Frontend Commands (Terminal 2)

```powershell
# Navigate to frontend
cd D:\FYP\frontend

# Install dependencies (first time)
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Stop server
Ctrl+C
```

---

## 🎯 Quick Start Script

You can create a batch file to start both servers:

**Create `start-backend.bat` in `D:\FYP\backend\`:**
```batch
@echo off
cd /d D:\FYP\backend
call venv\Scripts\activate.bat
uvicorn app.main:app --reload
pause
```

**Create `start-frontend.bat` in `D:\FYP\frontend\`:**
```batch
@echo off
cd /d D:\FYP\frontend
npm run dev
pause
```

Then just double-click these files to start each server!

---

## ✅ Verification Checklist

Before starting, verify:

- [ ] PostgreSQL is running
- [ ] Database `resume_optimizer` exists
- [ ] Virtual environment is activated (see `(venv)` in prompt)
- [ ] All backend dependencies installed
- [ ] `.env` file exists in backend directory
- [ ] All frontend dependencies installed (`node_modules` exists)
- [ ] Port 8000 is free (for backend)
- [ ] Port 5173 is free (for frontend)

---

## 🆘 Still Having Issues?

1. **Check Backend Logs** - Look at Terminal 1 for error messages
2. **Check Frontend Logs** - Look at Terminal 2 for error messages
3. **Check Browser Console** - Press F12 in browser, check Console tab
4. **Verify Services Running:**
   - Backend: http://localhost:8000/health
   - Frontend: http://localhost:5173

---

## 📞 Need Help?

Refer to:
- [README.md](./README.md) - Full documentation
- [TESTING_GUIDE.md](./TESTING_GUIDE.md) - Testing procedures
- [QUICK_START.md](./QUICK_START.md) - Quick setup guide

---

**Happy Coding! 🚀**

