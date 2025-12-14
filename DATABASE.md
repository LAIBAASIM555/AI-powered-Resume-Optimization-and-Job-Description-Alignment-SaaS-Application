# 🗄️ Database Documentation

## Database Overview

Ye project PostgreSQL database use karta hai jo saari user data, resumes, job descriptions, aur analysis results store karta hai.

## Database Schema

### Tables Detail

#### 1. Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE NOT NULL,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

**Fields:**
- `id`: Primary key, auto-increment
- `email`: Unique email address
- `hashed_password`: Argon2 hashed password
- `full_name`: User's full name
- `is_active`: Account status
- `is_verified`: Email verification status
- `last_login`: Last login timestamp
- `created_at/updated_at`: Timestamps

#### 2. Resumes Table
```sql
CREATE TABLE resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_content BYTEA,
    parsed_text TEXT,
    skills_extracted JSON,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Fields:**
- `id`: Primary key, auto-increment
- `user_id`: Foreign key to users table
- `filename`: Original file name
- `file_content`: Binary file data
- `parsed_text`: Extracted text from PDF/DOCX
- `skills_extracted`: JSON array of extracted skills
- `upload_date`: Upload timestamp

#### 3. Job Descriptions Table
```sql
CREATE TABLE job_descriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255),
    company VARCHAR(255),
    description TEXT NOT NULL,
    requirements TEXT,
    skills_required JSON,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

**Fields:**
- `id`: Primary key, auto-increment
- `title`: Job title
- `company`: Company name
- `description`: Full job description
- `requirements`: Job requirements text
- `skills_required`: JSON array of required skills
- `created_date`: Creation timestamp

#### 4. Analyses Table
```sql
CREATE TABLE analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    resume_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    similarity_score FLOAT NOT NULL,
    matching_skills JSON,
    missing_skills JSON,
    recommendations JSON,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_descriptions(id) ON DELETE CASCADE
);
```

**Fields:**
- `id`: Primary key, auto-increment
- `user_id`: Foreign key to users table
- `resume_id`: Foreign key to resumes table
- `job_id`: Foreign key to job_descriptions table
- `similarity_score`: ML-calculated similarity score (0-100)
- `matching_skills`: JSON array of matching skills
- `missing_skills`: JSON array of missing skills
- `recommendations`: JSON array of AI recommendations
- `created_date`: Analysis timestamp

## Relationships

```
users (1) ──── (many) resumes
users (1) ──── (many) analyses
resumes (1) ──── (many) analyses
job_descriptions (1) ──── (many) analyses
```

## Database Configuration

### Connection Settings
```python
DATABASE_URL = "postgresql://postgres:password123@db:5432/resume_optimizer"
```

### SQLAlchemy Configuration
```python
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG
)
```

## Indexes

### Performance Indexes
```sql
-- Users table indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Resumes table indexes
CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_resumes_upload_date ON resumes(upload_date);

-- Job descriptions indexes
CREATE INDEX idx_job_descriptions_created_date ON job_descriptions(created_date);

-- Analyses table indexes
CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_resume_id ON analyses(resume_id);
CREATE INDEX idx_analyses_job_id ON analyses(job_id);
CREATE INDEX idx_analyses_created_date ON analyses(created_date);
CREATE INDEX idx_analyses_similarity_score ON analyses(similarity_score);
```

## Data Types

### JSON Fields Structure

#### skills_extracted (Resumes)
```json
[
    "Python",
    "JavaScript",
    "React",
    "FastAPI",
    "PostgreSQL"
]
```

#### skills_required (Job Descriptions)
```json
[
    "Python",
    "Django",
    "REST API",
    "PostgreSQL",
    "Docker"
]
```

#### matching_skills (Analyses)
```json
[
    {"skill": "Python", "match_score": 0.95},
    {"skill": "PostgreSQL", "match_score": 0.88}
]
```

#### missing_skills (Analyses)
```json
[
    {"skill": "Django", "importance": "high"},
    {"skill": "Docker", "importance": "medium"}
]
```

#### recommendations (Analyses)
```json
[
    {
        "type": "skill",
        "priority": "high",
        "title": "Learn Django",
        "description": "Add Django framework to your skill set"
    },
    {
        "type": "experience",
        "priority": "medium",
        "title": "Gain Docker experience",
        "description": "Get hands-on experience with containerization"
    }
]
```

## Database Operations

### Common Queries

#### Get User with Resumes
```sql
SELECT u.*, r.filename, r.upload_date
FROM users u
LEFT JOIN resumes r ON u.id = r.user_id
WHERE u.id = ?
```

#### Get Analysis Results
```sql
SELECT a.*, r.filename, jd.title, jd.company
FROM analyses a
JOIN resumes r ON a.resume_id = r.id
JOIN job_descriptions jd ON a.job_id = jd.id
WHERE a.user_id = ?
ORDER BY a.created_date DESC
```

#### Get Top Skills
```sql
SELECT skill, COUNT(*) as frequency
FROM (
    SELECT json_array_elements_text(skills_extracted) as skill
    FROM resumes
) skills
GROUP BY skill
ORDER BY frequency DESC
LIMIT 10
```

## Backup & Recovery

### Database Backup
```bash
# Docker container backup
docker exec resume_db pg_dump -U postgres resume_optimizer > backup.sql

# Direct PostgreSQL backup
pg_dump -U postgres -h localhost -d resume_optimizer > backup.sql
```

### Database Restore
```bash
# Docker container restore
docker exec -i resume_db psql -U postgres resume_optimizer < backup.sql

# Direct PostgreSQL restore
psql -U postgres -h localhost -d resume_optimizer < backup.sql
```

## Performance Monitoring

### Query Performance
```sql
-- Check slow queries
SELECT query, calls, total_time, mean_time, rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Check table sizes
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Connection Monitoring
```sql
-- Check active connections
SELECT count(*) as active_connections
FROM pg_stat_activity
WHERE state = 'active';

-- Check connection states
SELECT state, count(*)
FROM pg_stat_activity
GROUP BY state;
```

## Migration Strategy

### Using Alembic
```bash
# Create new migration
alembic revision -m "Add new table"

# Run migrations
alembic upgrade head

# Downgrade
alembic downgrade -1
```

## Security Considerations

- **Password Hashing**: Argon2 algorithm
- **SQL Injection Protection**: Parameterized queries
- **Connection Encryption**: SSL/TLS enabled
- **Access Control**: Row-level security
- **Audit Logging**: All changes logged

## Troubleshooting

### Common Issues

#### Connection Refused
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check logs
docker logs resume_db
```

#### Slow Queries
```bash
# Enable query logging
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_duration = on;

# Check running queries
SELECT * FROM pg_stat_activity WHERE state = 'active';
```

#### Disk Space Issues
```bash
# Check database size
SELECT pg_size_pretty(pg_database_size('resume_optimizer'));

# Vacuum database
VACUUM FULL;
```

## Development Setup

### Local Database
```bash
# Start PostgreSQL with Docker
docker run -d --name postgres \
  -e POSTGRES_DB=resume_optimizer \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password123 \
  -p 5432:5432 \
  postgres:15-alpine
```

### Database GUI Tools
- **pgAdmin**: Web-based PostgreSQL admin
- **DBeaver**: Universal database tool
- **TablePlus**: Modern database client
- **psql**: Command-line client