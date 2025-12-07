import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

from app.main import app
from app.db.database import get_db
from app.db.base import Base
from app.config import settings

# Test Database URL - Use separate test database
# Option 1: PostgreSQL Test Database (Recommended for CI/CD)
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:password123@localhost:5432/resume_optimizer_test"
)

# Create test database engine
engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

# Test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create all tables before tests, drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    """Get database session for each test"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    """Get test client with database override"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    del app.dependency_overrides[get_db]


@pytest.fixture
def test_user(client):
    """Create a test user"""
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    })
    return response.json()


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for test user"""
    response = client.post("/api/v1/auth/login/json", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_resume_file():
    """Create a sample PDF file for testing"""
    import io
    # Simple PDF-like content for testing
    content = b"%PDF-1.4 test resume content"
    return io.BytesIO(content)

