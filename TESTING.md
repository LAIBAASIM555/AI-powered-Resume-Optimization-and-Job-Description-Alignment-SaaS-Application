# 🧪 Testing Guide

Ye guide aapko batayegi ki project ko kaise test karna hai - manual testing, automated testing, aur performance testing.

## 📋 Testing Overview

### Testing Types
- **Unit Tests**: Individual functions/components test
- **Integration Tests**: API endpoints aur database interactions test
- **End-to-End Tests**: Complete user workflows test
- **Performance Tests**: Load aur speed test
- **Manual Tests**: Human testing scenarios

---

## 🔧 Automated Testing Setup

### Backend Testing

#### Dependencies Install Karo
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Tests Run Karo
```bash
# Saare tests run karo
pytest

# Verbose output ke saath
pytest -v

# Specific test file run karo
pytest tests/test_auth.py

# Specific test function run karo
pytest tests/test_auth.py::test_register_user -v

# Coverage report generate karo
pytest --cov=app --cov-report=html
pytest --cov=app --cov-report=term-missing
```

#### Test Structure
```
backend/tests/
├── __init__.py
├── conftest.py          # Test configuration
├── test_auth.py         # Authentication tests
├── test_users.py        # User management tests
├── test_database.py     # Database tests
└── test_ml.py          # ML functionality tests
```

### Frontend Testing

#### Dependencies Install Karo
```bash
cd frontend
npm install
```

#### Tests Run Karo
```bash
# Unit tests run karo
npm test

# Watch mode me run karo
npm run test:watch

# Coverage report generate karo
npm run test:coverage

# Specific test file run karo
npm test -- LoginPage.test.jsx

# CI mode me run karo
npm run test:ci
```

#### Test Structure
```
frontend/src/
├── components/
│   └── __tests__/      # Component tests
├── pages/
│   └── __tests__/      # Page tests
├── services/
│   └── __tests__/      # API service tests
└── utils/
    └── __tests__/      # Utility function tests
```

---

## 🧪 Manual Testing Scenarios

### 1. User Registration & Login

#### Test Case: User Registration
```
Steps:
1. http://localhost pe jao
2. "Sign Up" button click karo
3. Form fill karo:
   - Email: test@example.com
   - Full Name: Test User
   - Password: Test123456
4. "Sign Up" button click karo

Expected Result:
- Success message show ho
- Login page pe redirect ho
- Database me user create ho jaye
```

#### Test Case: User Login
```
Steps:
1. http://localhost pe jao
2. "Login" button click karo
3. Credentials enter karo:
   - Email: test@example.com
   - Password: Test123456
4. "Login" button click karo

Expected Result:
- Dashboard pe redirect ho
- JWT token localStorage me save ho
- Navigation me user name show ho
```

### 2. Resume Upload

#### Test Case: PDF Resume Upload
```
Steps:
1. Login karo
2. "Upload Resume" page pe jao
3. PDF file select karo (max 5MB)
4. "Upload" button click karo

Expected Result:
- File upload ho jaye
- Progress bar show ho
- Success message aaye
- Database me resume save ho
```

#### Test Case: Invalid File Upload
```
Steps:
1. Login karo
2. TXT file select karo
3. Upload try karo

Expected Result:
- Error message show ho: "Only PDF and DOCX files allowed"
- Upload fail ho jaye
```

### 3. Job Description Creation

#### Test Case: Job Description Add Karo
```
Steps:
1. Login karo
2. "Create Job" page pe jao
3. Form fill karo:
   - Title: Software Engineer
   - Company: Tech Corp
   - Description: Job requirements...
4. "Create" button click karo

Expected Result:
- Job create ho jaye
- Job list me show ho
- Database me save ho jaye
```

### 4. Resume Analysis

#### Test Case: Complete Analysis
```
Steps:
1. Login karo
2. Resume aur Job Description select karo
3. "Analyze" button click karo

Expected Result:
- Loading spinner show ho
- ATS score calculate ho (0-100)
- Matching/missing skills show ho
- Recommendations generate ho
- Results page pe redirect ho
```

### 5. Dashboard Functionality

#### Test Case: Dashboard View
```
Steps:
1. Login karo
2. Dashboard page pe jao

Expected Result:
- Statistics cards show ho
- Recent analyses list show ho
- Charts render ho
- User info display ho
```

---

## 🔌 API Testing

### Using Swagger UI

#### API Documentation Access Karo
```
URL: http://localhost:8000/docs
```

#### Authentication Setup
```
1. "Authorize" button click karo
2. Token enter karo: Bearer <your-jwt-token>
3. "Authorize" click karo
```

#### API Endpoints Test Karo
```bash
# Health Check
GET /health

# User Registration
POST /api/v1/auth/register
{
  "email": "test@example.com",
  "full_name": "Test User",
  "password": "Test123456"
}

# User Login
POST /api/v1/auth/login/json
{
  "email": "test@example.com",
  "password": "Test123456"
}

# Resume Upload
POST /api/v1/resume/upload
Content-Type: multipart/form-data
Authorization: Bearer <token>
file: <resume.pdf>

# Job Creation
POST /api/v1/job/
Authorization: Bearer <token>
{
  "title": "Software Engineer",
  "company": "Tech Corp",
  "description": "Job description here..."
}

# Analysis
POST /api/v1/analysis/analyze
Authorization: Bearer <token>
{
  "resume_id": 1,
  "job_id": 1
}
```

### Using cURL Commands

#### Registration Test
```bash
curl -X POST http://localhost/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"Test123456"}'
```

#### Login Test
```bash
curl -X POST http://localhost/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456"}'
```

#### Protected Endpoint Test
```bash
curl -X GET http://localhost/api/v1/users/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 📊 Performance Testing

### Load Testing

#### Using Apache Bench
```bash
# Basic load test
ab -n 100 -c 10 http://localhost:8000/health

# API endpoint test
ab -n 50 -c 5 -H "Authorization: Bearer <token>" \
  http://localhost/api/v1/users/me
```

#### Using Siege
```bash
# Install siege
# Ubuntu: sudo apt install siege
# macOS: brew install siege

# Load test
siege -c 10 -t 30s http://localhost:8000/health

# Multiple URLs test
siege -c 5 -i -f urls.txt
```

### Memory & CPU Testing

#### Docker Resource Monitoring
```bash
# Container resource usage dekho
docker stats

# Specific container stats
docker stats resume_backend

# Memory usage history
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" resume_backend
```

#### Application Profiling
```bash
# Python memory profiling
pip install memory-profiler
python -m memory_profiler app/main.py

# CPU profiling
pip install py-spy
py-spy top --pid <backend-process-id>
```

---

## 🔍 Database Testing

### Database Connection Test
```bash
# Docker container se test karo
docker exec resume_db psql -U postgres -d resume_optimizer -c "SELECT 1;"

# Direct connection test
psql -U postgres -h localhost -d resume_optimizer -c "SELECT COUNT(*) FROM users;"
```

### Data Integrity Tests
```bash
# Foreign key constraints check karo
docker exec resume_db psql -U postgres -d resume_optimizer -c "
SELECT conname, conrelid::regclass, confrelid::regclass
FROM pg_constraint
WHERE contype = 'f';
"

# Data consistency check karo
docker exec resume_db psql -U postgres -d resume_optimizer -c "
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'resumes', COUNT(*) FROM resumes
UNION ALL
SELECT 'job_descriptions', COUNT(*) FROM job_descriptions
UNION ALL
SELECT 'analyses', COUNT(*) FROM analyses;
"
```

### Query Performance Tests
```bash
# Slow queries identify karo
docker exec resume_db psql -U postgres -d resume_optimizer -c "
SELECT query, calls, total_time/calls as avg_time, rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 5;
"

# Index usage check karo
docker exec resume_db psql -U postgres -d resume_optimizer -c "
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
"
```

---

## 🌐 Browser Testing

### Cross-Browser Testing

#### Manual Browser Testing
- **Chrome/Edge**: Primary support
- **Firefox**: Secondary support
- **Safari**: Basic support
- **Mobile Browsers**: Chrome Mobile, Safari Mobile

#### Browser Developer Tools
```
1. F12 press karo (DevTools open)
2. Network tab check karo (API calls)
3. Console tab check karo (JavaScript errors)
4. Application tab check karo (localStorage, sessionStorage)
5. Responsive design test karo (device toolbar)
```

### Mobile Testing

#### Device Emulation
```javascript
// Chrome DevTools me
1. F12 press karo
2. Toggle device toolbar (Ctrl+Shift+M)
3. Different devices select karo
4. Network throttling test karo
```

#### Real Device Testing
```bash
# Local network pe access karo
# Windows: ipconfig
# Linux: ip addr show
# Access: http://<your-ip>:80
```

---

## 🔐 Security Testing

### Authentication Testing
```bash
# Invalid token test
curl -X GET http://localhost/api/v1/users/me \
  -H "Authorization: Bearer invalid_token"

# Expired token test
curl -X GET http://localhost/api/v1/users/me \
  -H "Authorization: Bearer expired_token"

# No token test
curl -X GET http://localhost/api/v1/users/me
```

### Input Validation Testing
```bash
# SQL injection test
curl -X POST http://localhost/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com; DROP TABLE users;", "password":"test"}'

# XSS test
curl -X POST http://localhost/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"<script>alert(1)</script>", "password":"test"}'

# Large file upload test
# 10MB se bada file upload karo
```

### Rate Limiting Test
```bash
# Multiple requests bhejo
for i in {1..100}; do
  curl -X POST http://localhost/api/v1/auth/login/json \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"wrong"}' &
done
```

---

## 📱 End-to-End Testing

### Complete User Journey Test

#### Scenario 1: New User Complete Flow
```
1. Landing page visit karo
2. Sign up karo
3. Email verification (agar required)
4. Login karo
5. Profile complete karo
6. Resume upload karo
7. Job description create karo
8. Analysis run karo
9. Results dekho
10. Dashboard check karo
11. Logout karo
```

#### Scenario 2: Existing User Flow
```
1. Login karo
2. Previous analyses dekho
3. New resume upload karo
4. New analysis run karo
5. Results compare karo
6. Profile update karo
```

### Error Handling Tests

#### Network Error Simulation
```bash
# Backend stop karo
docker-compose stop backend

# Frontend se request bhejo
# Network error check karo

# Backend start karo
docker-compose start backend
```

#### Database Error Simulation
```bash
# Database stop karo
docker-compose stop db

# API call karo
# Database error check karo

# Database start karo
docker-compose start db
```

---

## 📈 Test Reporting

### Coverage Reports

#### Backend Coverage
```bash
# HTML report generate karo
pytest --cov=app --cov-report=html

# Report open karo
# Windows: start htmlcov/index.html
# Linux: xdg-open htmlcov/index.html
```

#### Frontend Coverage
```bash
# Coverage report generate karo
npm run test:coverage

# Report open karo
# coverage/lcov-report/index.html
```

### Test Results Analysis

#### Failed Tests Identify Karo
```bash
# Failed tests list dekho
pytest --tb=short

# Specific failure details dekho
pytest -v --tb=long
```

#### Performance Metrics
```bash
# Response time measure karo
curl -o /dev/null -s -w "%{time_total}\n" http://localhost:8000/health

# Memory usage monitor karo
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemPerc}}"
```

---

## 🐛 Bug Reporting

### Bug Report Template
```markdown
**Bug Title:** [Clear, descriptive title]

**Environment:**
- OS: Windows/Linux
- Browser: Chrome/Firefox
- Docker Version: [version]
- Application Version: [version]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Screenshots/Logs:**
[Attach screenshots or logs]

**Additional Context:**
[Any other relevant information]
```

### Common Issues & Solutions

#### Issue: Tests Fail Randomly
```
Solution:
- Database state reset karo
- Cache clear karo
- Dependencies reinstall karo
- Environment variables check karo
```

#### Issue: Slow Test Execution
```
Solution:
- Parallel execution use karo: pytest -n auto
- Database indexes optimize karo
- Unnecessary tests skip karo
- Test data reduce karo
```

#### Issue: Frontend Tests Fail
```
Solution:
- Node modules reinstall karo: rm -rf node_modules && npm install
- Cache clear karo: npm cache clean --force
- Browser update karo
- CI environment check karo
```

---

## 🚀 CI/CD Testing

### GitHub Actions Setup
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Docker Testing
```bash
# Multi-stage build test karo
docker build --target test -t test-image .

# Container test run karo
docker run --rm test-image pytest

# Integration tests run karo
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

---

## 📊 Test Metrics

### Key Performance Indicators

#### Backend Metrics
- **Response Time**: < 500ms for API calls
- **Error Rate**: < 1% for production
- **Test Coverage**: > 80% for critical code
- **Memory Usage**: < 512MB per container

#### Frontend Metrics
- **Load Time**: < 3 seconds initial load
- **Bundle Size**: < 2MB gzipped
- **Lighthouse Score**: > 90 for performance
- **Cross-browser Compatibility**: 95%+

#### Database Metrics
- **Query Time**: < 100ms average
- **Connection Pool**: 10-20 connections
- **Data Integrity**: 100% foreign key compliance
- **Backup Success**: 100% success rate

---

## 🎯 Testing Checklist

### Pre-Deployment Checklist
- [ ] Unit tests pass (pytest)
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Performance benchmarks met
- [ ] Security tests pass
- [ ] Cross-browser testing complete
- [ ] Mobile responsiveness verified
- [ ] Accessibility standards met

### Production Monitoring
- [ ] Error tracking setup (Sentry)
- [ ] Performance monitoring (New Relic)
- [ ] Log aggregation (ELK stack)
- [ ] Alert system configured
- [ ] Backup verification
- [ ] Disaster recovery tested

---

**Note**: Testing ek continuous process hai. Code changes ke baad hamesha tests run karo aur performance monitor karo!