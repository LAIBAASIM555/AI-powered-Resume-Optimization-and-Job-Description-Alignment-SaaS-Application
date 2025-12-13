# ⚡ Quick Start Guide

Get the AI Resume Optimizer up and running in 5 minutes!

## Prerequisites Check

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] PostgreSQL 15+ installed and running
- [ ] Git installed

---

## 🚀 5-Minute Setup

### Step 1: Database Setup (1 minute)

```bash
# Create database
psql -U postgres
CREATE DATABASE resume_optimizer;
\q
```

### Step 2: Backend Setup (2 minutes)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Create .env file
echo "DATABASE_URL=postgresql://postgres:password123@localhost:5432/resume_optimizer" > .env
echo "SECRET_KEY=your-super-secret-key-change-this-in-production" >> .env

# Start server
uvicorn app.main:app --reload
```

✅ Backend running on http://localhost:8000

### Step 3: Frontend Setup (2 minutes)

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

✅ Frontend running on http://localhost:5173

---

## 🧪 Quick Test

1. Open http://localhost:5173
2. Click "Get Started Free"
3. Register with:
   - Email: `test@example.com`
   - Password: `Test123456`
   - Full Name: `Test User`
4. Login with same credentials
5. Upload a PDF resume
6. Add a job description
7. Click "Analyze Resume"
8. View results!

---

## ✅ Verification Checklist

- [ ] Backend API responds: http://localhost:8000/health
- [ ] API docs available: http://localhost:8000/docs
- [ ] Frontend loads: http://localhost:5173
- [ ] Can register new user
- [ ] Can login
- [ ] Can upload resume
- [ ] Can create job description
- [ ] Can run analysis
- [ ] Results page displays correctly

---

## 🐛 Common Quick Fixes

**Backend won't start?**
```bash
# Check PostgreSQL is running
# Check .env file exists
# Check port 8000 is free
```

**Frontend won't start?**
```bash
# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

**Database connection error?**
```bash
# Verify PostgreSQL is running
# Check DATABASE_URL in .env
# Verify database exists
```

**Network error in frontend?**
```bash
# Verify backend is running on port 8000
# Check CORS settings in backend
# Clear browser cache
```

---

## 📚 Next Steps

- Read [README.md](./README.md) for full documentation
- Check [TESTING_GUIDE.md](./TESTING_GUIDE.md) for testing procedures
- Explore API docs at http://localhost:8000/docs

---

## 🎯 Development Commands

```bash
# Backend
cd backend
uvicorn app.main:app --reload          # Start dev server
pytest -v                              # Run tests
pytest --cov=app --cov-report=html     # Coverage report

# Frontend
cd frontend
npm run dev                            # Start dev server
npm run build                          # Build for production
npm run preview                        # Preview production build
```

---

## 📞 Need Help?

1. Check [README.md](./README.md) troubleshooting section
2. Review [TESTING_GUIDE.md](./TESTING_GUIDE.md)
3. Check backend logs for errors
4. Check browser console (F12) for frontend errors

---

**Happy Coding! 🚀**

