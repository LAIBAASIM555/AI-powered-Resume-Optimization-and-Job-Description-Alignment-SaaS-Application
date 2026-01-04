# 🔌 API Documentation

Complete API reference for the AI Resume Optimizer application.

## API Overview

**Base URL:** `http://localhost:8000/api/v1`

**Authentication:** Bearer Token (JWT)

**Content-Type:** `application/json` (unless uploading files)

---

## Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Database
    
    User->>Frontend: Enter credentials
    Frontend->>Backend: POST /auth/login/json
    Backend->>Database: Verify user
    Database-->>Backend: User data
    Backend->>Backend: Generate JWT
    Backend-->>Frontend: {access_token, token_type}
    Frontend->>Frontend: Store in localStorage
    Frontend-->>User: Redirect to dashboard
```

---

## 🔐 Authentication Endpoints

### Register User
```
POST /api/v1/auth/register
```

**Request Body:**
```json
{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "SecurePassword123"
}
```

**Response (201):**
```json
{
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_verified": false,
    "created_at": "2026-01-01T00:00:00"
}
```

**Errors:**
- `400` - Email already registered
- `422` - Validation error

---

### Login (JSON)
```
POST /api/v1/auth/login/json
```

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "SecurePassword123"
}
```

**Response (200):**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

**Errors:**
- `401` - Invalid credentials

---

### Login (Form Data)
```
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded
```

**Request Body:**
```
username=user@example.com&password=SecurePassword123
```

---

## 👤 User Endpoints

### Get Current User
```
GET /api/v1/users/me
Authorization: Bearer <token>
```

**Response (200):**
```json
{
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_verified": false,
    "last_login": "2026-01-01T12:00:00",
    "created_at": "2026-01-01T00:00:00"
}
```

---

### Update User
```
PUT /api/v1/users/me
Authorization: Bearer <token>
```

**Request Body:**
```json
{
    "full_name": "John Updated"
}
```

---

### Get User Statistics
```
GET /api/v1/users/me/stats
Authorization: Bearer <token>
```

**Response (200):**
```json
{
    "total_resumes": 5,
    "total_analyses": 12,
    "average_score": 78.5
}
```

---

## 📄 Resume Endpoints

### Upload Resume
```
POST /api/v1/resume/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request:**
- `file`: PDF or DOCX file (max 5MB)

**Response (200):**
```json
{
    "id": 1,
    "filename": "my_resume.pdf",
    "file_type": "pdf",
    "file_size": 245678,
    "skills": ["Python", "React", "PostgreSQL"],
    "upload_date": "2026-01-01T12:00:00",
    "is_valid": true,
    "validation_message": "Valid resume"
}
```

**Errors:**
- `400` - Invalid file type (only PDF/DOCX)
- `400` - File too large (>5MB)
- `400` - Not a valid resume (rejected by validator)
- `422` - File processing error

---

### Get All Resumes
```
GET /api/v1/resume/
Authorization: Bearer <token>
```

**Response (200):**
```json
[
    {
        "id": 1,
        "filename": "resume_v1.pdf",
        "file_type": "pdf",
        "upload_date": "2026-01-01T12:00:00"
    }
]
```

---

### Get Resume by ID
```
GET /api/v1/resume/{id}
Authorization: Bearer <token>
```

---

### Delete Resume
```
DELETE /api/v1/resume/{id}
Authorization: Bearer <token>
```

---

## 💼 Job Description Endpoints

### Create Job Description
```
POST /api/v1/job/
Authorization: Bearer <token>
```

**Request Body:**
```json
{
    "title": "Senior Software Engineer",
    "company": "Tech Corp",
    "location": "Remote",
    "raw_text": "We are looking for an experienced software engineer with Python, React, and PostgreSQL skills..."
}
```

**Response (200):**
```json
{
    "id": 1,
    "title": "Senior Software Engineer",
    "company": "Tech Corp",
    "location": "Remote",
    "required_skills": ["Python", "React", "PostgreSQL"],
    "keywords": ["agile", "CI/CD", "microservices"],
    "created_date": "2026-01-01T12:00:00"
}
```

---

### Get All Job Descriptions
```
GET /api/v1/job/
Authorization: Bearer <token>
```

---

### Get Job by ID
```
GET /api/v1/job/{id}
Authorization: Bearer <token>
```

---

### Delete Job Description
```
DELETE /api/v1/job/{id}
Authorization: Bearer <token>
```

---

## 📊 Analysis Endpoints

### Run Analysis
```
POST /api/v1/analysis/analyze
Authorization: Bearer <token>
```

**Request Body:**
```json
{
    "resume_id": 1,
    "job_id": 1
}
```

**Response (200):**
```json
{
    "id": 1,
    "ats_score": 82.5,
    "score_breakdown": {
        "skills_score": 85,
        "keywords_score": 78,
        "experience_score": 82,
        "format_score": 90,
        "achievements_score": 75
    },
    "matched_skills": ["Python", "React", "PostgreSQL"],
    "missing_skills": ["Docker", "Kubernetes"],
    "extra_skills": ["MongoDB", "Vue.js"],
    "matched_keywords": ["agile", "CI/CD"],
    "missing_keywords": ["microservices"],
    "recommendations": [
        {
            "priority": "high",
            "category": "skills",
            "message": "Add Docker experience",
            "details": "Docker is listed as required skill"
        }
    ],
    "created_date": "2026-01-01T12:00:00"
}
```

---

### Get Analysis History
```
GET /api/v1/analysis/
Authorization: Bearer <token>
```

---

### Get Analysis by ID
```
GET /api/v1/analysis/{id}
Authorization: Bearer <token>
```

---

### Delete Analysis
```
DELETE /api/v1/analysis/{id}
Authorization: Bearer <token>
```

---

## 📈 Dashboard Endpoints

### Get Dashboard Statistics
```
GET /api/v1/dashboard/stats
Authorization: Bearer <token>
```

**Response (200):**
```json
{
    "total_analyses": 12,
    "average_score": 78.5,
    "best_score": 92.0,
    "improvement": 15.5,
    "recent_analyses": [
        {
            "id": 12,
            "ats_score": 85.0,
            "job_title": "Senior Developer",
            "created_date": "2026-01-01T12:00:00"
        }
    ]
}
```

---

## 🔧 System Endpoints

### Health Check
```
GET /health
```

**Response (200):**
```json
{
    "status": "healthy",
    "database": "PostgreSQL connected"
}
```

---

### Root Endpoint
```
GET /
```

**Response (200):**
```json
{
    "app": "Resume Optimizer API",
    "version": "1.0.0",
    "status": "running",
    "database": "PostgreSQL",
    "docs": "/docs"
}
```

---

## 🔐 Authentication Headers

All protected endpoints require the Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Token Details:**
- Algorithm: HS256
- Expiry: 24 hours (1440 minutes)
- Stored in: localStorage (frontend)

---

## 📋 Error Responses

### Common Error Format
```json
{
    "detail": "Error message here"
}
```

### HTTP Status Codes
| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Server Error |

---

## 🧪 Testing with cURL

### Register
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"Test123456"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456"}'
```

### Upload Resume
```bash
curl -X POST http://localhost:8000/api/v1/resume/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@resume.pdf"
```

### Run Analysis
```bash
curl -X POST http://localhost:8000/api/v1/analysis/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"resume_id":1,"job_id":1}'
```

---

## 📚 Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔄 API Flow Diagram

```mermaid
flowchart TD
    A[User] --> B[Register/Login]
    B --> C{Authenticated?}
    C -->|No| B
    C -->|Yes| D[Upload Resume]
    D --> E{Valid Resume?}
    E -->|No| F[Error: Not a valid resume]
    E -->|Yes| G[Create Job Description]
    G --> H[Run Analysis]
    H --> I[View Results]
    I --> J[Dashboard]
    J --> D
```

---

**Note:** All API endpoints are versioned under `/api/v1/`. Future updates will use `/api/v2/` for breaking changes.
