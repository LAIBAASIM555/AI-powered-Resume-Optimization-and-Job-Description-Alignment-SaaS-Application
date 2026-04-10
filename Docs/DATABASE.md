# 🗄️ Database Documentation

Complete database documentation for the AI Resume Optimizer project.

## Database Overview

This project uses **PostgreSQL 15** as its primary database. SQLAlchemy 2.0 is used as the ORM. All tables include `created_at` and `updated_at` timestamps via the `TimestampMixin` base class.

---

## ER Diagram (Entity-Relationship)

```mermaid
erDiagram
    USERS ||--o{ RESUMES : "uploads"
    USERS ||--o{ JOB_DESCRIPTIONS : "creates"
    USERS ||--o{ ANALYSES : "performs"
    RESUMES ||--o{ ANALYSES : "analyzed_in"
    JOB_DESCRIPTIONS ||--o{ ANALYSES : "compared_with"

    USERS {
        int id PK
        varchar email UK
        varchar hashed_password
        varchar full_name
        boolean is_active
        boolean is_verified
        timestamp last_login
        timestamp created_at
        timestamp updated_at
    }

    RESUMES {
        int id PK
        int user_id FK
        varchar filename
        varchar file_path
        varchar file_type
        int file_size
        text raw_text
        json parsed_data
        json skills
        timestamp created_at
        timestamp updated_at
    }

    JOB_DESCRIPTIONS {
        int id PK
        int user_id FK
        varchar title
        varchar company
        varchar location
        text raw_text
        json parsed_data
        json required_skills
        json keywords
        timestamp created_at
        timestamp updated_at
    }

    ANALYSES {
        int id PK
        int user_id FK
        int resume_id FK
        int job_id FK
        float ats_score
        json score_breakdown
        json matched_skills
        json missing_skills
        json extra_skills
        json matched_keywords
        json missing_keywords
        json recommendations
        text original_summary
        text improved_summary
        timestamp created_at
        timestamp updated_at
    }
```

---

## Relationships Diagram

```mermaid
flowchart TD
    subgraph Users
        U[Users Table]
    end

    subgraph Content
        R[Resumes Table]
        J[Job Descriptions Table]
    end

    subgraph Results
        A[Analyses Table]
    end

    U -->|1:N| R
    U -->|1:N| J
    U -->|1:N| A
    R -->|1:N| A
    J -->|1:N| A
```

---

## Data Flow Diagram

```mermaid
flowchart LR
    A[User Registration] --> B[(Users Table)]
    C[Resume Upload] --> D[(Resumes Table)]
    E[Job Description] --> F[(Job Descriptions Table)]

    D --> G[Analysis + Career Analysis]
    F --> G
    G --> H[(Analyses Table)]

    B --> I[Authentication]
    I --> J[JWT Token]
```

---

## Tables Detail

### 1. Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE NOT NULL,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_id ON users(id);
```

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Unique auto-incremented identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email (used for login) |
| hashed_password | VARCHAR(255) | NOT NULL | Argon2 password hash |
| full_name | VARCHAR(100) | NOT NULL | Display name |
| is_active | BOOLEAN | DEFAULT TRUE | Account enabled/disabled flag |
| is_verified | BOOLEAN | DEFAULT FALSE | Email verification flag |
| last_login | TIMESTAMP | NULLABLE | Last successful login timestamp |
| created_at | TIMESTAMP | NOT NULL | Account creation time |
| updated_at | TIMESTAMP | NOT NULL | Last update time |

---

### 2. Resumes Table

```sql
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    file_size INTEGER NOT NULL,
    raw_text TEXT,
    parsed_data JSONB,
    skills JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_resumes_user_id ON resumes(user_id);
```

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| user_id | INTEGER | Foreign key → users (CASCADE delete) |
| filename | VARCHAR(255) | Original uploaded filename |
| file_path | VARCHAR(500) | Server file system path |
| file_type | VARCHAR(10) | `pdf` or `docx` |
| file_size | INTEGER | File size in bytes |
| raw_text | TEXT | Extracted plain text (by resume_parser.py) |
| parsed_data | JSONB | Structured parsed data (name, contact, sections) |
| skills | JSONB | JSON array of extracted skill strings |
| created_at | TIMESTAMP | Upload timestamp |
| updated_at | TIMESTAMP | Last update time |

---

### 3. Job Descriptions Table

```sql
CREATE TABLE job_descriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    company VARCHAR(255),
    location VARCHAR(255),
    raw_text TEXT NOT NULL,
    parsed_data JSONB,
    required_skills JSONB,
    keywords JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_job_descriptions_user_id ON job_descriptions(user_id);
```

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| user_id | INTEGER | Foreign key → users (CASCADE delete) |
| title | VARCHAR(255) | Job title (nullable) |
| company | VARCHAR(255) | Company name (nullable) |
| location | VARCHAR(255) | Job location (nullable) |
| raw_text | TEXT | Full job description text (required) |
| parsed_data | JSONB | Full parsed data including preferred_skills |
| required_skills | JSONB | Extracted required skills array |
| keywords | JSONB | Extracted keywords array |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update time |

---

### 4. Analyses Table

```sql
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    resume_id INTEGER NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES job_descriptions(id) ON DELETE CASCADE,
    ats_score FLOAT NOT NULL,
    score_breakdown JSONB,
    matched_skills JSONB,
    missing_skills JSONB,
    extra_skills JSONB,
    matched_keywords JSONB,
    missing_keywords JSONB,
    recommendations JSONB,
    original_summary TEXT,
    improved_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_resume_id ON analyses(resume_id);
CREATE INDEX idx_analyses_job_id ON analyses(job_id);
```

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| user_id | INTEGER | Foreign key → users (CASCADE delete) |
| resume_id | INTEGER | Foreign key → resumes (CASCADE delete) |
| job_id | INTEGER | Foreign key → job_descriptions (CASCADE delete) |
| ats_score | FLOAT | Overall ATS compatibility score (0–100) |
| score_breakdown | JSONB | Breakdown by component (skills, keywords, etc.) |
| matched_skills | JSONB | Skills found in both resume and job |
| missing_skills | JSONB | Skills required by job but missing from resume |
| extra_skills | JSONB | Skills in resume but not in job description |
| matched_keywords | JSONB | Keywords found in both documents |
| missing_keywords | JSONB | Keywords in job but missing from resume |
| recommendations | JSONB | Prioritized improvement recommendations |
| original_summary | TEXT | Resume's professional summary (as parsed) |
| improved_summary | TEXT | AI-improved summary (nullable, future feature) |
| created_at | TIMESTAMP | Analysis run timestamp |
| updated_at | TIMESTAMP | Last update time |

---

## JSON Field Structures

### `score_breakdown` (Analyses)
```json
{
    "skills_score": 85,
    "keywords_score": 78,
    "experience_score": 82,
    "format_score": 90,
    "achievements_score": 75
}
```

### `skills` (Resumes)
```json
["Python", "JavaScript", "React", "PostgreSQL", "Docker"]
```

### `parsed_data` (Job Descriptions)
```json
{
    "required_skills": ["Python", "FastAPI"],
    "preferred_skills": ["Docker", "Kubernetes"],
    "keywords": ["agile", "CI/CD"],
    "experience_required": "3-5 years"
}
```

### `recommendations` (Analyses)
```json
[
    {
        "priority": "high",
        "category": "skills",
        "message": "Add Docker experience",
        "details": "Docker is listed as a required skill in the job description"
    },
    {
        "priority": "medium",
        "category": "keywords",
        "message": "Include 'microservices' keyword",
        "details": "The job description mentions microservices multiple times"
    }
]
```

---

## Cascade Delete Rules

```mermaid
flowchart TD
    A[Delete User] --> B[All User's Resumes deleted]
    A --> C[All User's Job Descriptions deleted]
    A --> D[All User's Analyses deleted]

    E[Delete Resume] --> F[All Analyses referencing this Resume deleted]
    G[Delete Job Description] --> H[All Analyses referencing this Job deleted]
```

---

## Database Operations

### Backup
```bash
docker exec resume_db pg_dump -U postgres resume_optimizer > backup.sql
```

### Restore
```bash
docker exec -i resume_db psql -U postgres resume_optimizer < backup.sql
```

### Connect
```bash
docker exec -it resume_db psql -U postgres -d resume_optimizer
```

### Common Queries
```sql
-- Get user's analysis history with resume and job info
SELECT a.id, a.ats_score, r.filename, j.title, a.created_at
FROM analyses a
JOIN resumes r ON a.resume_id = r.id
JOIN job_descriptions j ON a.job_id = j.id
WHERE a.user_id = 1
ORDER BY a.created_at DESC;

-- Average score per user
SELECT user_id, AVG(ats_score) AS avg_score, COUNT(*) AS total_analyses
FROM analyses
GROUP BY user_id
ORDER BY avg_score DESC;

-- Most recent analysis per user
SELECT DISTINCT ON (user_id) user_id, ats_score, created_at
FROM analyses
ORDER BY user_id, created_at DESC;
```

---

## Connection Configuration

The database connection is managed via `app/db/database.py`:

```python
# From app/config.py
DATABASE_URL = "postgresql://postgres:password123@localhost:5432/resume_optimizer"

# Engine created in database.py
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)
```

For Docker, the host is `db` (service name):
```env
DATABASE_URL=postgresql://postgres:password123@db:5432/resume_optimizer
```

---

## Security

- **Password Hashing**: Argon2 algorithm via `passlib[argon2]`
- **SQL Injection Protection**: All queries use SQLAlchemy ORM — no raw SQL in application code
- **Cascade Deletes**: Foreign key constraints ensure no orphaned records
- **Indexes**: Indexed on all foreign keys and the `email` field for fast queries