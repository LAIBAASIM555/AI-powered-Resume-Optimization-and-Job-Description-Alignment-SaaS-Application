# 🏗️ Architecture Documentation

## Project Overview

Ye ek AI-powered Resume Optimization aur Job Description Alignment SaaS application hai jo machine learning ka use karke resumes ko optimize karta hai aur job descriptions ke saath align karta hai.

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │     Backend     │    │   Database      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│  (PostgreSQL)   │
│                 │    │                 │    │                 │
│ - User Interface│    │ - API Endpoints │    │ - User Data     │
│ - File Upload   │    │ - ML Processing │    │ - Resumes       │
│ - Results Display│   │ - Authentication │    │ - Job Descriptions│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Components Detail

### Backend (FastAPI)
- **Framework**: FastAPI with async support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with argon2 password hashing
- **File Processing**: PDF aur DOCX parsing with PyMuPDF aur python-docx
- **AI/ML**: spaCy for NLP, scikit-learn for similarity matching
- **API Documentation**: Automatic OpenAPI/Swagger docs

### Frontend (React)
- **Framework**: React 18 with Vite build tool
- **Styling**: Tailwind CSS for responsive design
- **HTTP Client**: Axios for API communication
- **Charts**: Recharts for data visualization
- **Routing**: React Router for navigation

### Database Schema

#### Users Table
User accounts aur authentication manage karta hai.

#### Resumes Table
Uploaded resume files aur parsed content store karta hai.

#### Job Descriptions Table
Job posting information aur requirements store karta hai.

#### Analyses Table
Analysis results aur recommendations store karta hai.

### Relationships
- Users → Resumes (One-to-Many)
- Users → Analyses (One-to-Many)
- Resumes → Analyses (One-to-Many)
- Job Descriptions → Analyses (One-to-Many)

## Technology Stack

### Backend Technologies
- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- spaCy (NLP)
- scikit-learn
- argon2 (password hashing)
- JWT (authentication)

### Frontend Technologies
- React.js 18+
- Vite (build tool)
- Tailwind CSS 3+
- Axios (HTTP client)
- React Router v6
- Lucide React (icons)
- Recharts (charts)

### DevOps & Tools
- Docker & Docker Compose
- Nginx (reverse proxy)
- Alembic (database migrations)
- Pytest (testing)

## Data Flow

1. **User Registration/Login**
   - Frontend → Backend API → Database
   - JWT token generation aur validation

2. **Resume Upload**
   - File upload → Backend processing → spaCy parsing → Database storage

3. **Job Description Creation**
   - Text input → Backend processing → Skills extraction → Database storage

4. **Analysis Process**
   - Resume + Job Description → ML processing → Similarity scoring → Recommendations

## Security Features

- **Password Hashing**: Argon2 algorithm
- **JWT Authentication**: Secure token-based auth
- **CORS Protection**: Configured allowed origins
- **Input Validation**: Pydantic schemas
- **File Type Validation**: PDF/DOCX only
- **SQL Injection Protection**: SQLAlchemy ORM

## Performance Optimizations

- **Async Processing**: FastAPI async endpoints
- **Database Connection Pooling**: SQLAlchemy pooling
- **File Caching**: Optimized file handling
- **Lazy Loading**: Database relationships
- **API Rate Limiting**: Built-in FastAPI features

## Deployment Architecture

### Docker Containers
- **db**: PostgreSQL database container
- **backend**: FastAPI application container
- **frontend**: React application with Nginx

### Networking
- **app_network**: Isolated Docker network
- **Port Mapping**: 80 (frontend), 8000 (backend), 5432 (database)

### Environment Variables
- DATABASE_URL
- SECRET_KEY
- DEBUG
- ALLOWED_ORIGINS

## Monitoring & Logging

- **Health Checks**: Built-in Docker health checks
- **API Logging**: Request/response logging
- **Error Handling**: Comprehensive error responses
- **Database Monitoring**: Connection health checks

## Future Enhancements

- **Microservices**: Individual services for ML processing
- **Message Queue**: Async job processing (Redis/Celery)
- **Load Balancing**: Multiple backend instances
- **CDN**: Static file serving optimization
- **Monitoring**: Prometheus/Grafana integration

### Backend Directory Structure

```
backend/app/
├── __init__.py
├── main.py                 # FastAPI application entry point
├── config.py               # Application configuration & settings
│
├── api/                    # API Routes & Dependencies
│   ├── __init__.py
│   ├── deps.py             # Dependency injection (auth, database)
│   └── v1/                 # API Version 1
│       ├── __init__.py
│       ├── router.py       # Main API router (aggregates all routes)
│       ├── auth.py         # Authentication endpoints
│       ├── users.py        # User management endpoints
│       ├── resume.py        # Resume upload & management
│       ├── job.py           # Job description endpoints
│       ├── analysis.py      # Analysis endpoints
│       └── dashboard.py    # Dashboard statistics
│
├── core/                   # Core functionality
│   ├── __init__.py
│   └── security.py         # JWT tokens, password hashing
│
├── db/                     # Database configuration
│   ├── __init__.py
│   ├── base.py             # SQLAlchemy Base & mixins
│   └── database.py         # Database session & engine
│
├── models/                 # SQLAlchemy ORM Models
│   ├── __init__.py
│   ├── user.py             # User model
│   ├── resume.py           # Resume model
│   ├── job.py              # JobDescription model
│   └── analysis.py         # Analysis model
│
├── schemas/                # Pydantic Schemas (Request/Response)
│   ├── __init__.py
│   ├── user.py             # User schemas
│   ├── token.py            # Token schemas
│   ├── resume.py           # Resume schemas
│   ├── job.py              # Job schemas
│   ├── analysis.py         # Analysis schemas
│   └── dashboard.py        # Dashboard schemas
│
├── ml/                     # Machine Learning / AI Components
│   ├── __init__.py
│   ├── resume_parser.py    # Extract text & parse resume
│   ├── jd_parser.py        # Parse job descriptions
│   ├── scorer.py           # Calculate ATS scores
│   └── recommender.py      # Generate recommendations
│
└── utils/                  # Utility functions
    ├── __init__.py
    └── file_handler.py     # File operations
```

### Backend Key Files

#### `backend/app/main.py`
- FastAPI application instance
- CORS middleware configuration
- API router inclusion
- Static file serving for uploads

#### `backend/app/config.py`
- Environment variable management
- Database URL construction
- Application settings (SECRET_KEY, CORS, file upload limits)
- Uses `pydantic-settings` for configuration

#### `backend/app/core/security.py`
- `get_password_hash()` - Bcrypt password hashing
- `verify_password()` - Password verification
- `create_access_token()` - JWT token creation
- `decode_access_token()` - JWT token decoding

#### `backend/app/api/deps.py`
- `get_current_user()` - Authentication dependency
- `get_db()` - Database session dependency
- OAuth2 token extraction

#### `backend/app/db/database.py`
- SQLAlchemy engine creation
- Database session management
- Connection pooling

---

## 🎨 Frontend Architecture

### Frontend Directory Structure

```
frontend/src/
├── index.jsx               # React application entry point
├── index.css               # Global styles & Tailwind imports
├── App.jsx                 # Main app component with routing
│
├── pages/                  # Page Components
│   ├── HomePage.jsx        # Landing page
│   ├── LoginPage.jsx       # User login
│   ├── SignupPage.jsx      # User registration
│   ├── UploadPage.jsx      # Resume upload & job input
│   ├── ResultsPage.jsx     # Analysis results display
│   └── DashboardPage.jsx    # User dashboard with history
│
├── components/             # Reusable Components
│   ├── common/             # Common UI components
│   │   ├── Button.jsx      # Button component
│   │   ├── Card.jsx        # Card container
│   │   ├── Input.jsx       # Input field
│   │   ├── Navbar.jsx      # Navigation bar
│   │   └── ProgressBar.jsx # Progress indicator
│   │
│   ├── upload/             # Upload-related components
│   │   ├── FileUpload.jsx  # Drag & drop file upload
│   │   └── JobInput.jsx    # Job description input form
│   │
│   └── results/            # Results display components
│       ├── ScoreCard.jsx   # ATS score circular display
│       ├── SkillsList.jsx  # Skills comparison list
│       └── Recommendations.jsx # Recommendations display
│
├── context/                # React Context
│   └── AuthContext.jsx     # Authentication state management
│
└── services/               # API Services
    └── api.jsx             # Axios instance & API methods
```

### Frontend Key Files

#### `frontend/src/App.jsx`
- React Router configuration
- Route definitions
- Protected route wrapper
- Navigation logic

#### `frontend/src/services/api.jsx`
- Axios instance with base URL: `http://localhost:8000/api/v1`
- Request interceptor (adds JWT token)
- Response interceptor (handles 401 errors)
- API method exports:
  - `authAPI` - Authentication
  - `userAPI` - User management
  - `resumeAPI` - Resume operations
  - `jobAPI` - Job description operations
  - `analysisAPI` - Analysis operations
  - `dashboardAPI` - Dashboard statistics

#### `frontend/src/context/AuthContext.jsx`
- Global authentication state
- `user` - Current user object
- `loading` - Loading state
- `login()` - Login function
- `register()` - Registration function
- `logout()` - Logout function
- `checkAuth()` - Verify token on mount

#### `frontend/src/pages/UploadPage.jsx`
- Resume file upload handling
- Job description input
- Automatic upload/save on analyze
- Step-by-step workflow
- Error handling

#### `frontend/src/pages/ResultsPage.jsx`
- Displays analysis results
- ATS score visualization
- Score breakdown
- Skills comparison
- Recommendations list

---

## 🗄️ Database Schema

### Database: `resume_optimizer`

### Table: `users`

**Purpose:** Store user accounts and authentication data

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEXED | User email address |
| `hashed_password` | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| `full_name` | VARCHAR(100) | NOT NULL | User's full name |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Account active status |
| `is_verified` | BOOLEAN | NOT NULL, DEFAULT FALSE | Email verification status |
| `last_login` | TIMESTAMP | NULLABLE | Last login timestamp |
| `created_at` | TIMESTAMP | NOT NULL | Account creation time |
| `updated_at` | TIMESTAMP | NOT NULL | Last update time |

**Relationships:**
- One-to-Many with `resumes` (cascade delete)
- One-to-Many with `analyses` (cascade delete)

---

### Table: `resumes`

**Purpose:** Store uploaded resume files and parsed data

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique resume identifier |
| `user_id` | INTEGER | FOREIGN KEY → users.id, NOT NULL, INDEXED | Owner user |
| `filename` | VARCHAR(255) | NOT NULL | Original filename |
| `file_path` | VARCHAR(500) | NOT NULL | Server file path |
| `file_type` | VARCHAR(10) | NOT NULL | File type (pdf/docx) |
| `file_size` | INTEGER | NOT NULL | File size in bytes |
| `raw_text` | TEXT | NULLABLE | Extracted text content |
| `parsed_data` | JSON | NULLABLE | Structured parsed data |
| `skills` | JSON | NULLABLE | Array of extracted skills |
| `created_at` | TIMESTAMP | NOT NULL | Upload timestamp |
| `updated_at` | TIMESTAMP | NOT NULL | Last update time |

**Relationships:**
- Many-to-One with `users` (on delete CASCADE)
- One-to-Many with `analyses` (cascade delete)

**JSON Fields:**
- `parsed_data`: `{summary, experience, education, contact_info, ...}`
- `skills`: `["Python", "React", "PostgreSQL", ...]`

---

### Table: `job_descriptions`

**Purpose:** Store job description data

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique job identifier |
| `user_id` | INTEGER | FOREIGN KEY → users.id, NOT NULL, INDEXED | Owner user |
| `title` | VARCHAR(255) | NULLABLE | Job title |
| `company` | VARCHAR(255) | NULLABLE | Company name |
| `location` | VARCHAR(255) | NULLABLE | Job location |
| `raw_text` | TEXT | NOT NULL | Full job description text |
| `parsed_data` | JSON | NULLABLE | Structured parsed data |
| `required_skills` | JSON | NULLABLE | Array of required skills |
| `keywords` | JSON | NULLABLE | Array of keywords |
| `created_at` | TIMESTAMP | NOT NULL | Creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL | Last update time |

**Relationships:**
- Many-to-One with `users` (on delete CASCADE)
- One-to-Many with `analyses` (cascade delete)

**JSON Fields:**
- `parsed_data`: `{requirements, responsibilities, qualifications, ...}`
- `required_skills`: `["Python", "Docker", "AWS", ...]`
- `keywords`: `["agile", "scrum", "CI/CD", ...]`

---

### Table: `analyses`

**Purpose:** Store analysis results comparing resumes to job descriptions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique analysis identifier |
| `user_id` | INTEGER | FOREIGN KEY → users.id, NOT NULL, INDEXED | Owner user |
| `resume_id` | INTEGER | FOREIGN KEY → resumes.id, NOT NULL, INDEXED | Analyzed resume |
| `job_id` | INTEGER | FOREIGN KEY → job_descriptions.id, NOT NULL, INDEXED | Target job |
| `ats_score` | FLOAT | NOT NULL | Overall ATS score (0-100) |
| `score_breakdown` | JSON | NULLABLE | Detailed category scores |
| `matched_skills` | JSON | NULLABLE | Skills found in both |
| `missing_skills` | JSON | NULLABLE | Skills in job but not resume |
| `extra_skills` | JSON | NULLABLE | Skills in resume but not job |
| `matched_keywords` | JSON | NULLABLE | Keywords found in resume |
| `missing_keywords` | JSON | NULLABLE | Keywords missing from resume |
| `recommendations` | JSON | NULLABLE | Array of recommendation objects |
| `original_summary` | TEXT | NULLABLE | Original resume summary |
| `improved_summary` | TEXT | NULLABLE | AI-improved summary |
| `created_at` | TIMESTAMP | NOT NULL | Analysis timestamp |
| `updated_at` | TIMESTAMP | NOT NULL | Last update time |

**Relationships:**
- Many-to-One with `users` (on delete CASCADE)
- Many-to-One with `resumes` (on delete CASCADE)
- Many-to-One with `job_descriptions` (on delete CASCADE)

**JSON Fields:**
- `score_breakdown`: `{skills_score: 90, experience_score: 80, keywords_score: 85, format_score: 90, achievements_score: 75}`
- `matched_skills`: `["Python", "React", "PostgreSQL"]`
- `missing_skills`: `["Docker", "AWS", "GraphQL"]`
- `extra_skills`: `["MongoDB", "Vue.js"]`
- `matched_keywords`: `["agile", "scrum", "CI/CD"]`
- `missing_keywords`: `["microservices", "kubernetes"]`
- `recommendations`: `[{priority: "high", category: "skills", message: "...", details: "..."}, ...]`

---

## 🔗 Database Relationships Diagram

```
users (1) ──< (many) resumes
users (1) ──< (many) job_descriptions
users (1) ──< (many) analyses

resumes (1) ──< (many) analyses
job_descriptions (1) ──< (many) analyses
```

**Cascade Rules:**
- Deleting a user deletes all their resumes, job descriptions, and analyses
- Deleting a resume deletes all analyses using that resume
- Deleting a job description deletes all analyses using that job

---

## 🌐 API Endpoints

### Base URL: `http://localhost:8000/api/v1`

### Authentication Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/auth/register` | No | Register new user |
| POST | `/auth/login` | No | Login (form data) |
| POST | `/auth/login/json` | No | Login (JSON) |

**Request/Response Examples:**

```json
// POST /auth/register
Request: {
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "SecurePass123"
}
Response: {
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-01T00:00:00"
}

// POST /auth/login/json
Request: {
  "email": "user@example.com",
  "password": "SecurePass123"
}
Response: {
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### User Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/users/me` | Yes | Get current user info |
| GET | `/users/me/stats` | Yes | Get user statistics |
| PUT | `/users/me` | Yes | Update user info |
| DELETE | `/users/me` | Yes | Delete account |

### Resume Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/resume/upload` | Yes | Upload resume file (multipart/form-data) |
| GET | `/resume/` | Yes | Get all user resumes |
| GET | `/resume/{id}` | Yes | Get resume by ID |
| DELETE | `/resume/{id}` | Yes | Delete resume |

**Upload Request:**
- Content-Type: `multipart/form-data`
- Field name: `file`
- Allowed types: PDF, DOCX
- Max size: 5MB

### Job Description Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/job/` | Yes | Create job description |
| GET | `/job/` | Yes | Get all user job descriptions |
| GET | `/job/{id}` | Yes | Get job by ID |
| DELETE | `/job/{id}` | Yes | Delete job description |

**Create Request:**
```json
{
  "title": "Senior React Developer",
  "company": "Tech Corp",
  "raw_text": "We are looking for..."
}
```

### Analysis Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/analysis/analyze` | Yes | Run analysis (resume_id, job_id) |
| GET | `/analysis/` | Yes | Get analysis history |
| GET | `/analysis/{id}` | Yes | Get analysis by ID |
| DELETE | `/analysis/{id}` | Yes | Delete analysis |

**Analyze Request:**
```json
{
  "resume_id": 1,
  "job_id": 1
}
```

**Analysis Response:**
```json
{
  "id": 1,
  "ats_score": 85.5,
  "score_breakdown": {
    "skills_score": 90,
    "experience_score": 80,
    "keywords_score": 85,
    "format_score": 90,
    "achievements_score": 75
  },
  "matched_skills": ["Python", "React"],
  "missing_skills": ["Docker"],
  "recommendations": [...]
}
```

### Dashboard Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/dashboard/stats` | Yes | Get dashboard statistics |

**Response:**
```json
{
  "total_analyses": 10,
  "average_score": 82.5,
  "best_score": 95.0,
  "improvement": 12.5,
  "recent_analyses": [...]
}
```

---

## 🔄 Data Flow

### User Registration Flow

```
Frontend (SignupPage) 
  → POST /auth/register 
  → Backend (auth.py) 
  → Hash password (security.py)
  → Create user (models/user.py)
  → Save to database
  → Return user data
  → Frontend redirects to login
```

### Login Flow

```
Frontend (LoginPage)
  → POST /auth/login/json
  → Backend (auth.py)
  → Verify credentials (security.py)
  → Generate JWT token
  → Return token
  → Frontend stores in localStorage
  → Redirect to /upload
```

### Resume Analysis Flow

```
1. User uploads resume (UploadPage)
   → POST /resume/upload
   → Backend saves file & parses (resume_parser.py)
   → Returns resume_id

2. User enters job description (UploadPage)
   → POST /job/
   → Backend parses JD (jd_parser.py)
   → Returns job_id

3. User clicks "Analyze" (UploadPage)
   → POST /analysis/analyze (resume_id, job_id)
   → Backend:
     a. Loads resume & job data
     b. Calculates ATS score (scorer.py)
     c. Generates recommendations (recommender.py)
     d. Saves analysis to database
   → Returns analysis_id
   → Frontend redirects to /results/{id}

4. Results displayed (ResultsPage)
   → GET /analysis/{id}
   → Display score, skills, recommendations
```

---

## 🔐 Authentication Flow

1. **Token Storage:** JWT stored in `localStorage` as `token`
2. **Token Format:** `Bearer {token}` in Authorization header
3. **Token Expiry:** 1440 minutes (24 hours)
4. **Token Validation:** On every protected route request
5. **Auto-logout:** On 401 response, token cleared, redirect to login

---

## 📦 Key Dependencies

### Backend (`requirements.txt`)

```python
# Core
fastapi==0.110.0
uvicorn[standard]==0.27.1
pydantic==2.6.1
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# File Processing
pymupdf==1.23.26
python-docx==1.1.0

# AI/NLP
spacy==3.7.4
scikit-learn==1.4.0
numpy==1.26.4
```

### Frontend (`package.json`)

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.20.0",
  "axios": "^1.6.2",
  "lucide-react": "^0.294.0",
  "recharts": "^2.10.3",
  "tailwindcss": "^3.3.6"
}
```

---

## 🎯 Environment Variables

### Backend (`.env` file)

```env
DATABASE_URL=postgresql://postgres:password123@localhost:5432/resume_optimizer
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=True
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
UPLOAD_DIR=uploads
MAX_FILE_SIZE=5242880
```

### Frontend Configuration

- API Base URL: `http://localhost:8000/api/v1` (hardcoded in `api.jsx`)
- For production, update in `frontend/src/services/api.jsx`

---

## 🚀 Deployment Architecture

### Development
- Backend: `uvicorn app.main:app --reload` (port 8000)
- Frontend: `npm run dev` (port 5173)
- Database: Local PostgreSQL

### Production (Docker)
- Backend container: FastAPI + Uvicorn
- Frontend container: Nginx serving built React app
- Database container: PostgreSQL
- All connected via Docker network

---

## 📝 Important Notes for AI Agents

1. **File Uploads:** Stored in `backend/uploads/` directory
2. **JWT Tokens:** Stored in browser `localStorage`, not cookies
3. **CORS:** Configured for `localhost:5173` and `localhost:3000`
4. **Database:** Uses SQLAlchemy ORM, not raw SQL
5. **Validation:** Pydantic schemas for request/response validation
6. **Error Handling:** FastAPI HTTPException for errors
7. **File Types:** Only PDF and DOCX accepted for resumes
8. **File Size Limit:** 5MB maximum
9. **Password Hashing:** Bcrypt with passlib
10. **Token Format:** JWT with HS256 algorithm

---

## 🔍 Code Patterns

### Backend Pattern
- **Dependency Injection:** FastAPI Depends() for database and auth
- **ORM Models:** SQLAlchemy models in `models/`
- **Schemas:** Pydantic models in `schemas/` for validation
- **Routes:** FastAPI routers in `api/v1/`
- **Services:** Business logic in route handlers

### Frontend Pattern
- **Component-Based:** React functional components with hooks
- **Context API:** AuthContext for global state
- **Custom Hooks:** useAuth() for authentication
- **API Service:** Centralized Axios instance
- **Protected Routes:** Wrapper component checks authentication

---

## 📚 Additional Resources

- **API Documentation:** http://localhost:8000/docs (Swagger UI)
- **Testing Guide:** See `TESTING_GUIDE.md`
- **Terminal Commands:** See `TERMINAL_GUIDE.md`
- **Quick Start:** See `QUICK_START.md`

---

**This document provides complete architecture understanding for AI agents and developers working on this project.**

