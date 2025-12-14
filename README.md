# AI-Powered Resume Optimization and Job Description Alignment SaaS Application

A comprehensive SaaS platform that uses artificial intelligence to optimize resumes and align them with job descriptions. The application provides resume parsing, job description analysis, skill matching, and personalized recommendations to help job seekers improve their applications.

## 🏗️ Project Architecture

### Overview
This is a full-stack web application built with modern technologies:

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

### Components

#### Backend (FastAPI)
- **Framework**: FastAPI with async support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **File Processing**: PDF and DOCX parsing with PyMuPDF and python-docx
- **AI/ML**: spaCy for NLP, scikit-learn for similarity matching
- **API Documentation**: Automatic OpenAPI/Swagger docs

#### Frontend (React)
- **Framework**: React 18 with Vite build tool
- **Styling**: Tailwind CSS for responsive design
- **HTTP Client**: Axios for API communication
- **Charts**: Recharts for data visualization
- **Routing**: React Router for navigation

#### Database Schema
```
users
├── id (Primary Key)
├── email (Unique)
├── hashed_password
├── full_name
├── is_active
├── is_verified
└── last_login

resumes
├── id (Primary Key)
├── user_id (Foreign Key)
├── filename
├── file_content
├── parsed_text
├── skills_extracted
└── upload_date

job_descriptions
├── id (Primary Key)
├── title
├── company
├── description
├── requirements
├── skills_required
└── created_date

analyses
├── id (Primary Key)
├── user_id (Foreign Key)
├── resume_id (Foreign Key)
├── job_id (Foreign Key)
├── similarity_score
├── matching_skills
├── missing_skills
├── recommendations
└── created_date
```

## 🚀 Quick Start

### Prerequisites

#### For All Platforms
- **Docker & Docker Compose**: Latest versions
- **Git**: For cloning the repository

#### For Local Development (Windows/Linux)
- **Python**: 3.11 or higher
- **Node.js**: 18.x or higher
- **PostgreSQL**: 15.x or higher (if not using Docker)

### Option 1: Docker Deployment (Recommended)

#### Windows Setup
1. **Install Docker Desktop**:
   - Download from https://www.docker.com/products/docker-desktop
   - Run the installer and follow the setup wizard
   - Enable WSL 2 if prompted
   - Start Docker Desktop

2. **Verify Installation**:
   ```powershell
   docker --version
   docker-compose --version
   ```

#### Linux Setup
1. **Install Docker**:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install docker.io docker-compose
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker $USER

   # Logout and login again for group changes to take effect
   ```

2. **Verify Installation**:
   ```bash
   docker --version
   docker-compose --version
   ```

#### Running with Docker
1. **Clone the repository**:
   ```bash
   git clone https://github.com/LAIBAASIM555/AI-powered-Resume-Optimization-and-Job-Description-Alignment-SaaS-Application.git
   cd AI-powered-Resume-Optimization-and-Job-Description-Alignment-SaaS-Application
   ```

2. **Start the application**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - **Frontend**: http://localhost:80
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

4. **Stop the application**:
   ```bash
   docker-compose down
   ```

### Option 2: Local Development Setup

#### Windows Setup
1. **Install Python 3.11+**:
   - Download from https://python.org
   - Add to PATH during installation

2. **Install Node.js 18+**:
   - Download from https://nodejs.org
   - Use LTS version

3. **Install PostgreSQL**:
   - Download from https://postgresql.org
   - Or use Docker: `docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=password123 postgres:15-alpine`

#### Linux Setup
1. **Install Python 3.11+**:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3.11 python3.11-venv python3-pip

   # CentOS/RHEL
   sudo yum install python311 python311-pip
   ```

2. **Install Node.js 18+**:
   ```bash
   # Ubuntu/Debian
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs

   # CentOS/RHEL
   curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
   sudo yum install -y nodejs
   ```

3. **Install PostgreSQL**:
   ```bash
   # Ubuntu/Debian
   sudo apt install postgresql postgresql-contrib

   # Or use Docker
   sudo docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=password123 postgres:15-alpine
   ```

#### Local Development Steps
1. **Clone and setup**:
   ```bash
   git clone https://github.com/LAIBAASIM555/AI-powered-Resume-Optimization-and-Job-Description-Alignment-SaaS-Application.git
   cd AI-powered-Resume-Optimization-and-Job-Description-Alignment-SaaS-Application
   ```

2. **Backend setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Database setup**:
   ```bash
   # Create database
   createdb resume_optimizer

   # Or with Docker
   docker run -d --name postgres -p 5432:5432 -e POSTGRES_DB=resume_optimizer -e POSTGRES_PASSWORD=password123 postgres:15-alpine
   ```

4. **Frontend setup**:
   ```bash
   cd ../frontend
   npm install
   npm run build
   ```

5. **Run the application**:
   ```bash
   # Terminal 1: Backend
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

6. **Access the application**:
   - **Frontend**: http://localhost:5173 (dev) or serve dist/ folder
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

## 📊 Database Architecture

### Tables Overview

#### Users Table
Manages user accounts and authentication.

#### Resumes Table
Stores uploaded resume files and parsed content.

#### Job Descriptions Table
Contains job posting information and requirements.

#### Analyses Table
Stores analysis results and recommendations.

### Relationships
- Users → Resumes (One-to-Many)
- Users → Analyses (One-to-Many)
- Resumes → Analyses (One-to-Many)
- Job Descriptions → Analyses (One-to-Many)

## 📦 Dependencies

### Backend Dependencies
```
fastapi==0.110.0
uvicorn[standard]==0.27.1
python-multipart==0.0.9
python-dotenv==1.0.1
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pydantic==2.6.1
pydantic-settings==2.1.0
email-validator==2.1.0
pymupdf==1.23.26
python-docx==1.1.0
spacy==3.7.4
scikit-learn==1.4.0
numpy==1.26.4
pytest>=7.0.0,<8.0.0
pytest-asyncio==0.23.4
httpx==0.26.0
aiofiles==23.2.1
```

### Frontend Dependencies
```json
{
  "dependencies": {
    "axios": "^1.6.2",
    "lucide-react": "^0.294.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "recharts": "^2.10.3"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.6",
    "vite": "^5.0.8"
  }
}
```

## 🐳 Docker Configuration

### Services
- **db**: PostgreSQL 15 Alpine
- **backend**: Python FastAPI application
- **frontend**: Node.js React application served by Nginx

### Volumes
- `postgres_data`: Persistent database storage
- `backend_uploads`: File upload storage

### Networks
- `app_network`: Isolated network for inter-service communication

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing key
- `DEBUG`: Debug mode flag
- `ALLOWED_ORIGINS`: CORS allowed origins

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```bash
DATABASE_URL=postgresql://postgres:password123@db:5432/resume_optimizer
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:80
```

### Database Configuration
The application uses SQLAlchemy with connection pooling and automatic table creation.

## 🧪 Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints
- `POST /api/v1/auth/login`: User authentication
- `POST /api/v1/resume/upload`: Upload resume
- `POST /api/v1/job/`: Create job description
- `POST /api/v1/analysis/`: Perform analysis
- `GET /api/v1/dashboard/`: Get user dashboard

## 🚀 Deployment

### Production Considerations
1. **Environment Variables**: Use strong secrets
2. **Database**: Use managed PostgreSQL service
3. **File Storage**: Use cloud storage (AWS S3, etc.)
4. **SSL/TLS**: Enable HTTPS
5. **Monitoring**: Add logging and monitoring
6. **Scaling**: Use container orchestration (Kubernetes)

### Docker Production
```bash
# Build for production
docker-compose -f docker-compose.yml up --build -d

# View logs
docker-compose logs -f

# Scale services
docker-compose up -d --scale backend=3
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

#### Docker Issues
- **Permission denied**: Run `sudo usermod -aG docker $USER` and logout/login
- **Port already in use**: Change ports in docker-compose.yml
- **Build fails**: Clear Docker cache with `docker system prune`

#### Backend Issues
- **Database connection fails**: Check DATABASE_URL and database availability
- **spaCy model not found**: Run `python -m spacy download en_core_web_sm`
- **Import errors**: Ensure all dependencies are installed

#### Frontend Issues
- **Build fails**: Clear node_modules and reinstall
- **API calls fail**: Check backend URL and CORS settings

### Getting Help
- Check the issues page on GitHub
- Review the API documentation
- Check Docker and application logs

---

**Note**: For the URL issue you mentioned, use `http://localhost:8000` instead of `http://0.0.0.0:8000`. The `0.0.0.0` address binds to all interfaces inside the container but is not accessible from outside.
