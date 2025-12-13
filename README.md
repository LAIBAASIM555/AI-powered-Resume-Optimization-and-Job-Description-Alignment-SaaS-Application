# 🎯 AI Resume Optimizer

AI-powered Resume Optimization and Job Description Alignment SaaS Application.

## 📋 Features

- ✅ **Resume Upload** - Upload PDF/DOCX files with drag & drop support
- ✅ **Job Description Parsing** - Intelligent extraction of skills and requirements
- ✅ **ATS Score Calculation** - Comprehensive scoring (0-100%) with breakdown
- ✅ **Skills Analysis** - Matched and missing skills identification
- ✅ **AI-Powered Recommendations** - Prioritized, actionable improvement suggestions
- ✅ **User Authentication** - Secure JWT-based authentication system
- ✅ **Analysis History Dashboard** - Track all analyses with trends and statistics
- ✅ **Modern UI** - Professional glass-morphism design with Tailwind CSS
- ✅ **Responsive Design** - Works seamlessly on mobile, tablet, and desktop
- ✅ **Real-time Feedback** - Loading states, error handling, and success messages

## 🛠️ Tech Stack

### Backend

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- spaCy (NLP)
- scikit-learn

### Frontend

- **React.js 18+** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **Tailwind CSS 3+** - Utility-first CSS framework
- **Axios** - HTTP client with interceptors
- **React Router v6** - Client-side routing
- **Lucide React** - Modern icon library
- **Recharts** - Chart library for data visualization

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

## 🧪 Testing

### Comprehensive Testing Guide

For detailed testing procedures, see **[TESTING_GUIDE.md](./TESTING_GUIDE.md)**

### Quick Test Flow

1. **Register a new user:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","full_name":"Test User","password":"Test123456"}'
   ```

2. **Login and get token:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/login/json \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"Test123456"}'
   ```

3. **Upload resume (replace YOUR_TOKEN):**
   ```bash
   curl -X POST http://localhost:8000/api/v1/resume/upload \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -F "file=@resume.pdf"
   ```

4. **Create job description:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/job/ \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title":"Senior Developer","company":"Tech Corp","raw_text":"Job description text..."}'
   ```

5. **Run analysis:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/analysis/analyze \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"resume_id":1,"job_id":1}'
   ```

### Using Swagger UI

1. Start the backend server
2. Navigate to http://localhost:8000/docs
3. Click "Authorize" button
4. Enter JWT token: `Bearer YOUR_TOKEN`
5. Test any endpoint interactively

### Frontend Testing

1. Start both backend and frontend servers
2. Open http://localhost:5173 in browser
3. Open Developer Tools (F12) → Network tab
4. Follow the complete user flow:
   - Register → Login → Upload → Analyze → View Results → Dashboard
5. Monitor API calls and responses
6. Check console for errors

---

## 🎨 UI Features

### Design System

- **Color Palette:**
  - Primary: Blue (#0284c7 - primary-600)
  - Secondary: Purple (#d946ef - secondary-500)
  - Accent: Yellow (#eab308 - accent-500)
  - Success: Green (#10b981)
  - Error: Red (#ef4444)

- **Components:**
  - Glass-morphism cards with backdrop blur
  - Gradient backgrounds
  - Smooth transitions and animations
  - Responsive grid layouts
  - Modern icon system (Lucide React)

### User Interface Pages

1. **Home Page** (`/`)
   - Hero section with call-to-action
   - Features showcase
   - How it works section
   - Statistics display

2. **Login Page** (`/login`)
   - Glass-morphism card design
   - Icon-based form inputs
   - Error handling
   - Link to signup

3. **Signup Page** (`/signup`)
   - Multi-field registration form
   - Real-time validation
   - Terms acceptance
   - Success animation

4. **Upload Page** (`/upload`)
   - Drag & drop file upload
   - Job description textarea
   - Real-time validation
   - Progress indicators

5. **Results Page** (`/results/:id`)
   - Circular ATS score display
   - Score breakdown with progress bars
   - Skills comparison (matched/missing)
   - Prioritized recommendations
   - Action buttons

6. **Dashboard Page** (`/dashboard`)
   - Statistics cards
   - Score trend chart (Recharts)
   - Analysis history table
   - Empty state handling

---

## 🔧 Environment Variables

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | `postgresql://postgres:password123@localhost:5432/resume_optimizer` |
| `SECRET_KEY` | JWT secret key (generate strong key) | Required |
| `DEBUG` | Enable debug mode | `True` |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | `http://localhost:5173,http://localhost:3000` |
| `UPLOAD_DIR` | Upload directory | `uploads` |
| `MAX_FILE_SIZE` | Max file size in bytes | `5242880` (5MB) |

### Frontend Configuration

The frontend API base URL is configured in `src/services/api.jsx`:
```javascript
const API_BASE_URL = 'http://localhost:8000/api/v1';
```

For production, update this to your production API URL.

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

### Common Issues

#### 1. Network Error / Connection Refused

**Symptoms:** Frontend shows "Network Error" when calling API

**Solutions:**
- ✅ Verify backend is running on `http://localhost:8000`
- ✅ Check backend logs for errors
- ✅ Verify CORS settings in backend allow `http://localhost:5173`
- ✅ Check firewall isn't blocking port 8000
- ✅ Test API directly: `curl http://localhost:8000/health`

#### 2. Authentication Issues

**Symptoms:** "Invalid credentials" or token errors

**Solutions:**
- ✅ Check password meets requirements (min 8 characters)
- ✅ Verify email format is correct
- ✅ Check token is stored: `localStorage.getItem('token')`
- ✅ Clear localStorage and try again
- ✅ Check backend SECRET_KEY is set correctly

#### 3. File Upload Fails

**Symptoms:** Resume upload shows error

**Solutions:**
- ✅ Verify file is PDF or DOCX format
- ✅ Check file size < 5MB
- ✅ Ensure user is authenticated (has valid token)
- ✅ Check backend `uploads/` directory exists and is writable
- ✅ Verify backend has required dependencies (PyMuPDF, python-docx)

#### 4. Buttons Not Visible

**Symptoms:** Buttons appear white on white

**Solutions:**
- ✅ Clear browser cache (Ctrl+Shift+Delete)
- ✅ Restart dev server: `npm run dev`
- ✅ Verify Tailwind CSS is compiled: Check `index.css` imports
- ✅ Check browser console for CSS errors

#### 5. PostgreSQL Connection Error

**Solutions:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql  # Linux
# OR check Services on Windows

# Check if database exists
sudo -u postgres psql -c "\l"

# Verify connection string in .env
DATABASE_URL=postgresql://postgres:password123@localhost:5432/resume_optimizer
```

#### 6. Port Already in Use

**Solutions:**
```bash
# Windows PowerShell
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

#### 7. Docker Issues

**Solutions:**
```bash
# Remove all containers and volumes
docker-compose down -v

# Rebuild from scratch
docker-compose up --build --force-recreate

# Check logs
docker-compose logs -f
```

#### 8. Windows PowerShell Virtual Environment

**Solutions:**
```powershell
# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate:
.\venv\Scripts\Activate.ps1

# Or use activate.bat:
.\venv\Scripts\activate.bat
```

#### 9. Frontend Build Errors

**Symptoms:** npm install fails or build errors

**Solutions:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear npm cache
npm cache clean --force

# Update dependencies
npm update
```

#### 10. API Timeout Errors

**Symptoms:** Requests timeout after 10 seconds

**Solutions:**
- ✅ Check backend is processing requests (check logs)
- ✅ For large file uploads, increase timeout in `api.jsx`
- ✅ Check network connection
- ✅ Verify backend isn't stuck processing

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

## 📱 Application Flow

### Complete User Journey

1. **Landing** → User visits homepage
2. **Registration** → User creates account
3. **Login** → User authenticates
4. **Upload** → User uploads resume and adds job description
5. **Analysis** → System analyzes and generates report
6. **Results** → User views ATS score and recommendations
7. **Dashboard** → User tracks analysis history

### Navigation Map

```
Home (/)
  ├── Signup (/signup)
  │   └── Login (/login)
  │       └── Upload (/upload)
  │           └── Results (/results/:id)
  │               └── Dashboard (/dashboard)
  └── Login (/login)
      └── Upload (/upload)
          └── Results (/results/:id)
              └── Dashboard (/dashboard)
```

---

## 🔐 Security Features

- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - Bcrypt password hashing
- **CORS Protection** - Configured allowed origins
- **Input Validation** - Server-side validation with Pydantic
- **File Type Validation** - Only PDF/DOCX allowed
- **File Size Limits** - Maximum 5MB file size
- **SQL Injection Protection** - SQLAlchemy ORM prevents SQL injection
- **XSS Protection** - React automatically escapes content

---

## 📈 Performance Optimizations

- **API Timeout** - 10-second timeout prevents hanging requests
- **Lazy Loading** - Components load on demand
- **Optimized Queries** - Database queries optimized with indexes
- **Caching** - Token stored in localStorage
- **Code Splitting** - React Router code splitting
- **Image Optimization** - Optimized assets

---

## 🚀 Deployment

### Backend Deployment

1. Set environment variables
2. Build Docker image: `docker build -t resume-optimizer-backend .`
3. Run container with PostgreSQL
4. Update CORS settings for production domain

### Frontend Deployment

1. Build production bundle: `npm run build`
2. Serve `dist/` folder with nginx or similar
3. Update API base URL in `api.jsx`
4. Configure environment variables

---

## 📚 Additional Resources

- **Testing Guide:** See [TESTING_GUIDE.md](./TESTING_GUIDE.md) for comprehensive testing procedures
- **API Documentation:** Available at http://localhost:8000/docs when backend is running
- **Backend Code:** Located in `backend/app/`
- **Frontend Code:** Located in `frontend/src/`

---

## 🎯 Quick Start Checklist

- [ ] Install PostgreSQL and create database
- [ ] Set up backend virtual environment
- [ ] Install backend dependencies (`pip install -r requirements.txt`)
- [ ] Configure `.env` file with database URL and SECRET_KEY
- [ ] Start backend server (`uvicorn app.main:app --reload`)
- [ ] Install frontend dependencies (`npm install`)
- [ ] Start frontend dev server (`npm run dev`)
- [ ] Open http://localhost:5173 in browser
- [ ] Register a new account
- [ ] Upload a resume and test the flow

---

## 👥 Team

- **Backend & AI/ML:** FastAPI, PostgreSQL, spaCy, scikit-learn
- **Frontend & UI:** React, Tailwind CSS, Lucide Icons, Recharts

## 📄 License

This project is part of Final Year Project (FYP).

---

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React team for the amazing frontend library
- Tailwind CSS for the utility-first CSS framework
- Lucide for the beautiful icon set
- All open-source contributors

---

## 📞 Support

For issues or questions:
1. Check [TESTING_GUIDE.md](./TESTING_GUIDE.md) for common issues
2. Review troubleshooting section above
3. Check backend logs for errors
4. Check browser console for frontend errors
5. Verify all services are running correctly
