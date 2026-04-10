# 🤖 AI-Powered Resume Optimization and Job Description Alignment — SaaS Application

> A full-stack SaaS platform that uses Machine Learning and optional AI APIs to optimize resumes, calculate ATS scores, analyze career paths, and provide personalized improvement recommendations for job seekers.

---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 📄 Resume Upload & Parsing | Upload PDF/DOCX — auto-extracts text, skills, and structured data |
| ✅ Strict Resume Validation | Rejects non-resume documents (invoices, images, random text) |
| 💼 Job Description Analysis | Parses job postings and extracts required skills & keywords |
| 📊 ATS Scoring Engine | TF-IDF + cosine similarity scoring (0–100) against job descriptions |
| 🎯 Career Path Analysis | Matches resume against 100+ careers across multiple fields |
| 💡 Personalized Recommendations | Prioritized, actionable tips to improve resume for each role |
| 🤖 Optional AI Enhancement | Plug in Google Gemini or OpenAI API for smarter ATS analysis |
| 🌗 Dark/Light Mode | Full theme toggle across the entire UI |
| 📈 Dashboard | Track all past analyses and score history |

---

## 🏗️ System Architecture

```
┌─────────────────────┐     HTTP/REST      ┌──────────────────────┐     SQLAlchemy    ┌───────────────────┐
│   Frontend (React)  │ ◄─────────────── ► │  Backend  (FastAPI)  │ ◄──────────────► │ Database (Postgres)│
│                     │                    │                      │                   │                   │
│  • Vite + Tailwind  │                    │  • JWT Auth          │                   │  • users          │
│  • React Router v6  │                    │  • ML Engine         │                   │  • resumes        │
│  • Axios API Client │                    │  • Career Analyzer   │                   │  • job_descriptions│
│  • Recharts Charts  │                    │  • AI Generator      │                   │  • analyses       │
│  • Dark/Light Theme │                    │  • File Processing   │                   │                   │
└─────────────────────┘                    └──────────────────────┘                   └───────────────────┘
```

---

## 🧠 ML/AI Components

```
backend/app/ml/
├── resume_parser.py      # Extracts text from PDF/DOCX using PyMuPDF & python-docx
├── resume_validator.py   # STRICT validation — rejects non-resume documents
├── jd_parser.py          # Parses job descriptions, extracts required skills & keywords
├── jd_validator.py       # Validates that submitted text is a real job description
├── scorer.py             # ATS scoring: TF-IDF + cosine similarity (5-component score)
├── recommender.py        # Generates prioritized, actionable recommendations
├── skills_database.py    # 500+ skills database + find_skills_in_text()
├── career_analyzer.py    # Matches resume to 100+ career paths across multiple fields
├── career_database.py    # CAREER_DATABASE & CAREER_FIELDS — career data store
└── ai_generator.py       # Optional: Gemini/OpenAI API for AI-enhanced ATS analysis
```

### ATS Score Breakdown

| Component | Weight | What It Measures |
|-----------|--------|-----------------|
| Skills Match | **40%** | Resume skills vs. required job skills |
| Keywords Match | **25%** | Industry keywords in resume vs. job description |
| Experience Match | **20%** | Experience level and duration alignment |
| Format & Structure | **10%** | Resume formatting quality and completeness |
| Achievements | **5%** | Quantified results and impact statements |

---

## 🗄️ Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PK | Auto-increment ID |
| email | VARCHAR(255) UNIQUE | Login email |
| hashed_password | VARCHAR(255) | Argon2 hash |
| full_name | VARCHAR(100) | Display name |
| is_active | BOOLEAN | Account status |
| is_verified | BOOLEAN | Email verified |
| last_login | TIMESTAMP | Last login time |
| created_at | TIMESTAMP | Account created |
| updated_at | TIMESTAMP | Last updated |

### Resumes Table
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PK | Auto-increment ID |
| user_id | INTEGER FK | → users.id (CASCADE) |
| filename | VARCHAR(255) | Original filename |
| file_path | VARCHAR(500) | Server storage path |
| file_type | VARCHAR(10) | `pdf` or `docx` |
| file_size | INTEGER | Size in bytes |
| raw_text | TEXT | Extracted plain text |
| parsed_data | JSONB | Structured sections (name, contact, experience, education) |
| skills | JSONB | Extracted skills array |
| created_at | TIMESTAMP | Upload time |

### Job Descriptions Table
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PK | Auto-increment ID |
| user_id | INTEGER FK | → users.id (CASCADE) |
| title | VARCHAR(255) | Job title |
| company | VARCHAR(255) | Company name |
| location | VARCHAR(255) | Job location |
| raw_text | TEXT | Full description text |
| parsed_data | JSONB | Structured (required_skills, preferred_skills, keywords) |
| required_skills | JSONB | Skills array from JD |
| keywords | JSONB | Keywords array from JD |
| created_at | TIMESTAMP | Created time |

### Analyses Table
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PK | Auto-increment ID |
| user_id | INTEGER FK | → users.id |
| resume_id | INTEGER FK | → resumes.id |
| job_id | INTEGER FK | → job_descriptions.id |
| ats_score | FLOAT | Overall score 0–100 |
| score_breakdown | JSONB | Per-component scores |
| matched_skills | JSONB | Skills in both resume & job |
| missing_skills | JSONB | Skills required but missing |
| extra_skills | JSONB | Resume skills not in JD |
| matched_keywords | JSONB | Keywords matched |
| missing_keywords | JSONB | Keywords missing |
| recommendations | JSONB | Prioritized recommendations |
| original_summary | TEXT | Resume summary as parsed |
| improved_summary | TEXT | AI-improved summary (optional) |
| created_at | TIMESTAMP | Analysis timestamp |

---

## 📁 Full Project Structure

```
Resume-Optimization/
├── README.md
├── docker-compose.yml           # Orchestrates db + backend + frontend containers
├── test_ml_system.py            # Standalone ML system test script
├── .gitignore
│
├── Docs/                        # Project documentation
│   ├── API.md                   # Full API reference with request/response examples
│   ├── ARCHITECTURE.md          # System architecture & component details
│   ├── DATABASE.md              # Database schema & SQL definitions
│   ├── SETUP.md                 # Setup guide (Docker & local)
│   ├── TERMINAL.md              # Quick terminal commands reference
│   └── TESTING.md               # Testing guide & manual test scenarios
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env                     # Environment variables (not committed)
│   ├── .env.example             # Template for .env
│   ├── init.sql                 # Database initialization SQL
│   │
│   └── app/
│       ├── main.py              # FastAPI app entry point
│       ├── config.py            # Settings via pydantic-settings
│       │
│       ├── api/
│       │   ├── deps.py          # Auth + DB dependency injection
│       │   └── v1/
│       │       ├── router.py    # Aggregates all API routes
│       │       ├── auth.py      # /auth/register, /auth/login, /auth/login/json
│       │       ├── users.py     # /users/me, /users/me/stats
│       │       ├── resume.py    # /resume/upload, /resume/{id}
│       │       ├── job.py       # /job/ (CRUD)
│       │       ├── analysis.py  # /analysis/analyze, /analysis/{id}
│       │       ├── dashboard.py # /dashboard/stats
│       │       └── career.py    # /career/analyze, /career/fields, /career/careers
│       │
│       ├── core/
│       │   └── security.py      # JWT creation/validation, Argon2 hashing
│       │
│       ├── db/
│       │   ├── base.py          # SQLAlchemy Base + TimestampMixin
│       │   └── database.py      # Engine + get_db() session factory
│       │
│       ├── models/              # SQLAlchemy ORM models
│       │   ├── user.py
│       │   ├── resume.py
│       │   ├── job.py
│       │   └── analysis.py
│       │
│       ├── schemas/             # Pydantic request/response schemas
│       │   ├── user.py
│       │   ├── token.py
│       │   ├── resume.py
│       │   ├── job.py
│       │   ├── analysis.py
│       │   ├── dashboard.py
│       │   └── career.py
│       │
│       ├── ml/                  # Machine Learning & AI components
│       │   ├── resume_parser.py
│       │   ├── resume_validator.py
│       │   ├── jd_parser.py
│       │   ├── jd_validator.py
│       │   ├── scorer.py
│       │   ├── recommender.py
│       │   ├── skills_database.py
│       │   ├── career_analyzer.py
│       │   ├── career_database.py
│       │   └── ai_generator.py
│       │
│       └── utils/
│           └── file_handler.py
│
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── index.html
    │
    └── src/
        ├── App.jsx              # Root component + routing
        ├── index.jsx            # React entry point
        ├── index.css            # Global styles + Tailwind
        │
        ├── pages/
        │   ├── HomePage.jsx
        │   ├── LoginPage.jsx
        │   ├── SignupPage.jsx
        │   ├── UploadPage.jsx
        │   ├── ResultsPage.jsx
        │   ├── DashboardPage.jsx
        │   └── CareerAnalysisPage.jsx
        │
        ├── components/
        │   ├── common/          # Navbar, Footer, Button, Card, Input, etc.
        │   ├── upload/          # Upload-specific sub-components
        │   └── results/         # Results display sub-components
        │
        ├── context/
        │   ├── AuthContext.jsx  # Authentication state (login/logout)
        │   └── ThemeContext.jsx # Dark/Light mode
        │
        └── services/
            └── api.jsx          # Axios instance + all API method calls
```

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)
```bash
git clone https://github.com/LAIBAASIM555/AI-powered-Resume-Optimization-and-Job-Description-Alignment-SaaS-Application.git
cd AI-powered-Resume-Optimization-and-Job-Description-Alignment-SaaS-Application
docker-compose up -d --build
```
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs

### Option 2: Local Development (Windows)
```powershell
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000

---

## 🤖 AI API Key Support (Optional)

The system works **fully out-of-the-box** using local ML (spaCy + scikit-learn). However, for **AI-enhanced, smarter ATS scoring**, you can add an API key from either:

### Option A: Google Gemini (Recommended)
1. Get a free key at: https://aistudio.google.com/
2. Add to `backend/.env`:
```env
GOOGLE_API_KEY=your-google-api-key-here
AI_SERVICE_PREFERRED=gemini
USE_AI_PARSING=True
```

### Option B: OpenAI (ChatGPT/GPT-4)
1. Get a key at: https://platform.openai.com/
2. Add to `backend/.env`:
```env
OPENAI_API_KEY=your-openai-api-key-here
AI_SERVICE_PREFERRED=openai
USE_AI_PARSING=True
```

### What AI Enhancement Does
| Without AI | With AI |
|-----------|---------|
| TF-IDF + cosine similarity scoring | Gemini/GPT-4 understands context and nuance |
| Keyword-based skill matching | Recognizes skill synonyms and related experience |
| Rule-based recommendations | AI-generated, personalized improvement advice |
| Local, fast, always works | Better accuracy, requires internet + API key |

> **Note**: If the API key is missing or the API call fails, the system **automatically falls back** to the local ML engine — no errors, no downtime.

---

## 🔐 Security Features

- **Password Hashing**: Argon2 algorithm (industry standard)
- **JWT Authentication**: HS256 tokens, 24-hour expiry
- **CORS Protection**: Configurable allowed origins
- **Input Validation**: Pydantic schemas on all endpoints
- **File Validation**: Only PDF/DOCX, max 5MB enforced
- **Resume Validation**: Strict content validation — rejects non-resume documents
- **SQL Injection Protection**: SQLAlchemy ORM (no raw SQL)

---

## 📡 API Endpoints Overview

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/auth/register` | No | Register new user |
| POST | `/api/v1/auth/login/json` | No | Login (JSON body) |
| GET | `/api/v1/users/me` | Yes | Get current user profile |
| POST | `/api/v1/resume/upload` | Yes | Upload PDF/DOCX resume |
| GET | `/api/v1/resume/` | Yes | Get all user resumes |
| POST | `/api/v1/job/` | Yes | Create job description |
| POST | `/api/v1/analysis/analyze` | Yes | Run ATS analysis |
| GET | `/api/v1/analysis/` | Yes | Get analysis history |
| GET | `/api/v1/dashboard/stats` | Yes | Dashboard statistics |
| POST | `/api/v1/career/analyze` | Yes | Career path analysis |
| GET | `/api/v1/career/fields` | No | List career fields |
| GET | `/health` | No | Health check |

> Full API documentation: [Docs/API.md](Docs/API.md)

---

## 🛠️ Tech Stack Summary

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite 5, Tailwind CSS 3, React Router v6 |
| Backend | Python 3.11+, FastAPI 0.110, Uvicorn |
| Database | PostgreSQL 15, SQLAlchemy 2.0, Alembic |
| Auth | JWT (python-jose), Argon2 (passlib) |
| ML/NLP | spaCy 3.7, scikit-learn 1.4, NumPy |
| File Processing | PyMuPDF, python-docx |
| Optional AI | Google Gemini API, OpenAI API |
| DevOps | Docker, Docker Compose, Nginx |

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|---------| 
| Docker not starting | `docker system prune -a` then `docker-compose up --build` |
| Port 8000/5432 in use | Change ports in `docker-compose.yml` |
| Database connection fails | Check `DATABASE_URL` in `.env` |
| spaCy model missing | `python -m spacy download en_core_web_sm` |
| Resume rejected | Must be a real resume with contact info + work experience |
| API key not working | Check `.env` — set `AI_SERVICE_PREFERRED` to `gemini` or `openai` |

---

## 📖 Documentation

| File | Description |
|------|-------------|
| [Docs/API.md](Docs/API.md) | Complete API reference |
| [Docs/ARCHITECTURE.md](Docs/ARCHITECTURE.md) | System architecture details |
| [Docs/DATABASE.md](Docs/DATABASE.md) | Database schema & SQL |
| [Docs/SETUP.md](Docs/SETUP.md) | Step-by-step setup guide |
| [Docs/TERMINAL.md](Docs/TERMINAL.md) | Terminal commands cheat sheet |
| [Docs/TESTING.md](Docs/TESTING.md) | Testing guide |

---

## 📄 License

This project is licensed under the **MIT License**.

---

*Built with ❤️ using FastAPI, React, PostgreSQL, and Machine Learning*
