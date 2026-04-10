# 🧪 Testing Guide

This guide covers how to test the AI Resume Optimizer project — from automated API tests to full manual user flows.

## 📋 Testing Overview

| Type | Tool | What it Tests |
|------|------|---------------|
| Unit Tests | Pytest | Individual ML functions, scorers, parsers |
| Integration Tests | Pytest + HTTPX | API endpoints + database interactions |
| Manual Tests | Browser + cURL | Complete user workflows |
| Performance Tests | Apache Bench | Load & response time |

---

## 🔧 Automated Backend Testing

### Setup
```powershell
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### Run Tests
```powershell
# Run all tests
pytest

# Verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py
pytest tests/test_resume.py

# With HTML coverage report
pytest --cov=app --cov-report=html

# Quick smoke test — no DB needed
pytest tests/ -k "not db"
```

### Test Files Location
```
backend/tests/
├── test_auth.py       # Registration, login, token validation
├── test_resume.py     # Upload, parsing, validation
├── test_analysis.py   # ATS scoring, recommendations
└── test_career.py     # Career analysis matching
```

---

## 🧪 Manual Testing Scenarios

### 1. User Registration
```
Steps:
1. Go to http://localhost (or http://localhost:5173 in dev)
2. Click "Sign Up"
3. Fill form:
   - Email: test@example.com
   - Full Name: Test User
   - Password: Test123456
4. Submit

Expected:
✅ Success message displayed
✅ Redirect to /login
✅ User record created in database (check: SELECT * FROM users;)
```

### 2. User Login
```
Steps:
1. Go to /login
2. Enter email: test@example.com
3. Enter password: Test123456
4. Click "Login"

Expected:
✅ Redirect to /upload
✅ JWT token stored in localStorage
✅ Navbar shows user name
```

### 3. Resume Upload
```
Steps:
1. Go to /upload after login
2. Click the upload area or drag-and-drop a PDF/DOCX file
3. Wait for upload

Expected:
✅ Upload progress shown
✅ Resume appears in dropdown
✅ Skills extracted and displayed

Rejection Cases (expected errors):
❌ Non-PDF/DOCX file → "Invalid file type"
❌ File > 5MB → "File too large"
❌ Non-resume document (e.g. invoice) → "Not a valid resume"
```

### 4. Job Description Input
```
Steps:
1. Paste a complete job description into the text area
2. Fill in optional Title, Company, Location fields
3. Click "Add Job Description"

Expected:
✅ Job description saved
✅ Job appears in dropdown for analysis
```

### 5. ATS Analysis
```
Steps:
1. Select a resume from dropdown
2. Select a job description from dropdown
3. Click "Analyze"

Expected:
✅ Loading spinner shown during analysis
✅ Redirect to /results/{id}
✅ ATS score displayed (0–100)
✅ Matched skills shown in green
✅ Missing skills shown in red
✅ Prioritized recommendations displayed
```

### 6. Career Analysis
```
Steps:
1. Navigate to Career Analysis page (if linked in navbar)
2. Select a resume from the dropdown
3. Click "Analyze Career Fit"

Expected:
✅ Best-fit career displayed with match percentage
✅ List of eligible careers shown
✅ Career fields (Software Engineering, Data Science, etc.) shown
✅ Salary range, market demand, growth rate shown per career
```

### 7. Dashboard
```
Steps:
1. Go to /dashboard after performing at least one analysis

Expected:
✅ Total analyses count shown
✅ Average ATS score shown
✅ Best score shown
✅ Analysis history list shown
✅ Can click on any history item to view full results
```

---

## 🔌 API Testing via Swagger UI

Access: `http://localhost:8000/docs`

**Testing flow:**
1. `POST /auth/register` → create user
2. `POST /auth/login/json` → get token
3. Click **Authorize** button → enter `Bearer <token>`
4. `POST /resume/upload` → upload a resume file
5. `POST /job/` → add a job description
6. `POST /analysis/analyze` → run analysis with `resume_id` and `job_id`
7. `GET /analysis/{id}` → view full results
8. `POST /career/analyze` → run career analysis with `resume_id`

---

## 🔌 API Testing via cURL

### Register & Login
```powershell
# Register
curl -X POST http://localhost:8000/api/v1/auth/register `
  -H "Content-Type: application/json" `
  -d '{"email":"test@example.com","full_name":"Test User","password":"Test123456"}'

# Login (save the token from response)
curl -X POST http://localhost:8000/api/v1/auth/login/json `
  -H "Content-Type: application/json" `
  -d '{"email":"test@example.com","password":"Test123456"}'
```

### Resume & Analysis
```powershell
# Upload resume (replace YOUR_TOKEN and path)
curl -X POST http://localhost:8000/api/v1/resume/upload `
  -H "Authorization: Bearer YOUR_TOKEN" `
  -F "file=@C:\path\to\resume.pdf"

# Get current user info
curl -X GET http://localhost:8000/api/v1/users/me `
  -H "Authorization: Bearer YOUR_TOKEN"

# Run analysis
curl -X POST http://localhost:8000/api/v1/analysis/analyze `
  -H "Authorization: Bearer YOUR_TOKEN" `
  -H "Content-Type: application/json" `
  -d '{"resume_id":1,"job_id":1}'

# Run career analysis
curl -X POST http://localhost:8000/api/v1/career/analyze `
  -H "Authorization: Bearer YOUR_TOKEN" `
  -H "Content-Type: application/json" `
  -d '{"resume_id":1}'
```

---

## 📊 Performance Testing

### Response Time Test
```powershell
# Check health endpoint response time
curl -o /dev/null -s -w "%{time_total}s\n" http://localhost:8000/health
```

### Load Testing (Apache Bench)
```powershell
# 100 requests, 10 concurrent
ab -n 100 -c 10 http://localhost:8000/health
```

### Docker Resource Monitoring
```powershell
docker stats --no-stream
```

---

## 🔐 Security Testing

### Invalid Authentication
```powershell
# No token (expect 401)
curl -X GET http://localhost:8000/api/v1/users/me

# Invalid token (expect 401)
curl -X GET http://localhost:8000/api/v1/users/me `
  -H "Authorization: Bearer invalid_token_here"
```

### Input Validation
- Upload file > 5MB → expect `400 Bad Request`
- Upload `.exe` file → expect `400 Bad Request`
- Register with invalid email format → expect `422 Unprocessable Entity`
- Login with wrong password → expect `401 Unauthorized`
- Access another user's analysis → expect `404 Not Found` (user-scoped queries)

---

## 🗄️ Database Verification

```powershell
# Run inside database container
docker exec resume_db psql -U postgres -d resume_optimizer -c "
SELECT 'users' AS table_name, COUNT(*) FROM users
UNION ALL
SELECT 'resumes', COUNT(*) FROM resumes
UNION ALL
SELECT 'job_descriptions', COUNT(*) FROM job_descriptions
UNION ALL
SELECT 'analyses', COUNT(*) FROM analyses;"
```

---

## 📈 Test Metrics Targets

### Backend
| Metric | Target |
|--------|--------|
| Health endpoint response | < 100ms |
| Resume upload + parse | < 5s |
| ATS analysis | < 10s |
| Career analysis | < 15s |
| Test coverage | > 70% |

### Frontend
| Metric | Target |
|--------|--------|
| Initial page load | < 3s |
| Production bundle size | < 2MB |
| Cross-browser support | Chrome, Firefox, Edge |
| Responsive breakpoints | Desktop, Tablet, Mobile |
| Dark/Light mode | Both modes render correctly |

---

## 🐛 Bug Reporting Template

```markdown
**Bug Title:** [Short description]

**Environment:**
- OS: Windows 11
- Browser: Chrome 120
- Node.js: v24.x
- Python: 3.11.x

**Steps to Reproduce:**
1. Log in at http://localhost
2. Upload resume...
3. Click Analyze

**Expected:** ATS score is displayed
**Actual:** Error message appears / blank screen

**Console Errors:** [Paste any browser console errors]
**API Response:** [Paste any API error response]
**Screenshots:** [Attach if available]
```

---

## 🎯 Pre-Deployment Checklist

- [ ] All pytest tests pass (`pytest -v`)
- [ ] Health check returns 200 (`curl http://localhost:8000/health`)
- [ ] User registration & login works
- [ ] Resume upload accepts PDF and DOCX
- [ ] Resume upload rejects invalid files
- [ ] ATS analysis returns results
- [ ] Career analysis returns results
- [ ] Dashboard displays history
- [ ] Dark/Light mode toggle works
- [ ] Mobile responsive layout verified
- [ ] Docker build succeeds (`docker-compose up --build`)

---

**Note**: For each new feature added, write corresponding tests in the `backend/tests/` directory before deployment.