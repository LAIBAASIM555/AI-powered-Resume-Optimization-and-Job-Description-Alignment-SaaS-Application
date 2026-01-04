# 🧪 Testing Guide

This guide covers how to test the AI Resume Optimizer project.

## 📋 Testing Overview

- **Unit Tests**: Individual functions/components
- **Integration Tests**: API endpoints & database
- **Manual Tests**: Complete user workflows
- **Performance Tests**: Load & speed testing

---

## 🔧 Automated Testing

### Backend Testing

#### Setup
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Run Tests
```bash
# All tests
pytest

# Verbose output
pytest -v

# Specific test file
pytest tests/test_auth.py

# With coverage
pytest --cov=app --cov-report=html
```

### Frontend Testing
```bash
cd frontend
npm install
npm test
npm run test:coverage
```

---

## 🧪 Manual Testing Scenarios

### 1. User Registration
```
Steps:
1. Go to http://localhost
2. Click "Sign Up"
3. Fill form:
   - Email: test@example.com
   - Name: Test User
   - Password: Test123456
4. Submit

Expected:
- Success message appears
- Redirect to login page
- User created in database
```

### 2. User Login
```
Steps:
1. Go to login page
2. Enter credentials
3. Click "Login"

Expected:
- Redirect to dashboard
- JWT token stored in localStorage
```

### 3. Resume Upload
```
Steps:
1. Login
2. Go to Upload page
3. Select PDF/DOCX file (max 5MB)
4. Upload

Expected:
- Progress bar shows
- Success message appears
- Resume saved to database

Note: Only REAL resumes are accepted. Files without
contact info, work experience, or education will be rejected.
```

### 4. Resume Analysis
```
Steps:
1. Upload resume
2. Enter job description
3. Click "Analyze"

Expected:
- Loading spinner shows
- ATS score calculated (0-100)
- Skills comparison displayed
- Recommendations generated
- Redirect to results page
```

---

## 🔌 API Testing

### Using Swagger UI

Access: http://localhost:8000/docs

### cURL Examples

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"Test123456"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456"}'

# Get current user (with token)
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 📊 Performance Testing

### Load Testing
```bash
# Apache Bench
ab -n 100 -c 10 http://localhost:8000/health

# Check response time
curl -o /dev/null -s -w "%{time_total}\n" http://localhost:8000/health
```

### Docker Monitoring
```bash
docker stats
```

---

## 🔐 Security Testing

### Authentication Tests
```bash
# Invalid token
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer invalid_token"
# Expected: 401 Unauthorized

# No token
curl -X GET http://localhost:8000/api/v1/users/me
# Expected: 401 Unauthorized
```

### Input Validation
- SQL injection attempts should be blocked
- XSS attempts should be sanitized
- Large files (>5MB) should be rejected
- Only PDF/DOCX files should be accepted
- Non-resume documents should be rejected

---

## 🗄️ Database Testing

```bash
# Connection test
docker exec resume_db psql -U postgres -d resume_optimizer -c "SELECT 1;"

# Data counts
docker exec resume_db psql -U postgres -d resume_optimizer -c "
SELECT 'users' as table_name, COUNT(*) FROM users
UNION ALL
SELECT 'resumes', COUNT(*) FROM resumes
UNION ALL
SELECT 'analyses', COUNT(*) FROM analyses;"
```

---

## 📈 Test Metrics

### Backend Targets
- Response Time: < 500ms
- Error Rate: < 1%
- Test Coverage: > 80%

### Frontend Targets
- Load Time: < 3 seconds
- Bundle Size: < 2MB gzipped
- Cross-browser: Chrome, Firefox, Safari

---

## 🐛 Bug Reporting Template

```markdown
**Bug Title:** [Short description]

**Environment:**
- OS: Windows/Linux
- Browser: Chrome/Firefox
- Docker Version: [version]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected:** [What should happen]
**Actual:** [What happens]
**Screenshots:** [Attach if available]
```

---

## 🎯 Pre-Deployment Checklist

- [ ] All unit tests pass
- [ ] API endpoints tested
- [ ] Manual testing completed
- [ ] Performance benchmarks met
- [ ] Security tests pass
- [ ] Cross-browser tested
- [ ] Mobile responsive verified

---

**Note**: Run tests after every code change and before deployment!