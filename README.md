# 🎯 AI Resume Optimizer

AI-powered Resume Optimization and Job Description Alignment SaaS Application.

## 📋 Features

- ✅ Upload Resume (PDF/DOCX)
- ✅ Parse Job Description
- ✅ Calculate ATS Score (0-100%)
- ✅ Identify Matched & Missing Skills
- ✅ AI-Powered Recommendations
- ✅ User Authentication (JWT)
- ✅ Analysis History Dashboard

## 🛠️ Tech Stack

### Backend

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- spaCy (NLP)
- scikit-learn

### Frontend

- React.js
- Tailwind CSS
- Axios
- React Router

## 🚀 How to Run

### Prerequisites

- Docker & Docker Compose (Recommended)
- OR Python 3.11+ & Node.js 18+
- PostgreSQL 15+

---

## Option 1: Docker (Recommended - Easiest)

### Step 1: Clone and Navigate

```bash
git clone <repository-url>
cd ai-resume-optimizer
```

### Step 2: Start with Docker Compose

```bash
# Start PostgreSQL and Backend
cd backend
docker-compose up --build

# Wait for "Application startup complete" message
```

### Step 3: Access the Application

- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Step 4: Start Frontend (in new terminal)

```bash
cd frontend
npm install
npm run dev
```

- Frontend: http://localhost:5173

---

## Option 2: Local Development (Without Docker)

### Backend Setup

#### Step 1: Install PostgreSQL

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database
sudo -u postgres psql
CREATE DATABASE resume_optimizer;
\q
```

#### Step 2: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Windows CMD)
venv\Scripts\activate.bat

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Create .env file (copy from .env.example and update)
cp .env.example .env
```

#### Step 3: Update .env file

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/resume_optimizer
SECRET_KEY=your-very-long-random-secret-key
```

#### Step 4: Run Backend

```bash
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 📁 Project Structure

```
ai-resume-optimizer/
├── backend/
│   ├── app/
│   │   ├── api/v1/        # API Routes
│   │   ├── core/          # Security
│   │   ├── db/            # Database
│   │   ├── models/        # SQLAlchemy Models
│   │   ├── schemas/       # Pydantic Schemas
│   │   ├── ml/            # AI/ML Components
│   │   └── main.py        # FastAPI App
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── context/
│   └── package.json
└── README.md
```

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/register | Register new user |
| POST | /api/v1/auth/login | Login (form data) |
| POST | /api/v1/auth/login/json | Login (JSON) |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/users/me | Get current user |
| GET | /api/v1/users/me/stats | Get user stats |
| PUT | /api/v1/users/me | Update user |
| DELETE | /api/v1/users/me | Delete account |

### Resume

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/resume/upload | Upload resume (PDF/DOCX) |
| GET | /api/v1/resume/ | Get all resumes |
| GET | /api/v1/resume/{id} | Get resume by ID |
| DELETE | /api/v1/resume/{id} | Delete resume |

### Job Description

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/job/ | Create job description |
| GET | /api/v1/job/ | Get all job descriptions |
| GET | /api/v1/job/{id} | Get job by ID |
| DELETE | /api/v1/job/{id} | Delete job |

### Analysis

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/analysis/analyze | Analyze resume vs job |
| GET | /api/v1/analysis/ | Get analysis history |
| GET | /api/v1/analysis/{id} | Get analysis by ID |
| DELETE | /api/v1/analysis/{id} | Delete analysis |

### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/dashboard/stats | Get dashboard stats |

---

## 🧪 Testing API

### Using Swagger UI

1. Go to http://localhost:8000/docs
2. Click "Authorize" and enter JWT token
3. Test any endpoint

### Using curl

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"password123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Use the returned access_token for authenticated requests
```

---

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection URL | - |
| SECRET_KEY | JWT secret key | - |
| DEBUG | Enable debug mode | True |
| ALLOWED_ORIGINS | CORS allowed origins | http://localhost:3000 |
| UPLOAD_DIR | Upload directory | uploads |
| MAX_FILE_SIZE | Max file size (bytes) | 5242880 |

---

## 📊 Database Schema

```
users
├── id (PK)
├── email (unique)
├── hashed_password
├── full_name
├── is_active
├── created_at
└── updated_at

resumes
├── id (PK)
├── user_id (FK → users)
├── filename
├── file_path
├── raw_text
├── parsed_data (JSON)
├── skills (JSON)
└── created_at

job_descriptions
├── id (PK)
├── user_id (FK → users)
├── title
├── company
├── raw_text
├── required_skills (JSON)
├── keywords (JSON)
└── created_at

analyses
├── id (PK)
├── user_id (FK → users)
├── resume_id (FK → resumes)
├── job_id (FK → job_descriptions)
├── ats_score
├── score_breakdown (JSON)
├── matched_skills (JSON)
├── missing_skills (JSON)
├── recommendations (JSON)
└── created_at
```

---

## 🐛 Troubleshooting

### PostgreSQL Connection Error

```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check if database exists
sudo -u postgres psql -c "\l"
```

### Port Already in Use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 5432
lsof -ti:5432 | xargs kill -9
```

### Docker Issues

```bash
# Remove all containers and volumes
docker-compose down -v

# Rebuild from scratch
docker-compose up --build
```

### Windows PowerShell Virtual Environment

```powershell
# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate:
.\venv\Scripts\Activate.ps1

# Or use activate.bat:
.\venv\Scripts\activate.bat
```

---

## 🧪 Running Tests

```bash
# Create test database first
docker exec -it resume_postgres_db psql -U postgres -c "CREATE DATABASE resume_optimizer_test;"

# Or if using local PostgreSQL
psql -U postgres -c "CREATE DATABASE resume_optimizer_test;"

# Run tests
cd backend
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html
```

---

## 👥 Team

- Member 1: Backend + AI/ML
- Member 2: Frontend + Testing

## 📄 License

This project is part of Final Year Project (FYP).
