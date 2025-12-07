"""Test PostgreSQL database connection"""

def test_database_connection(db):
    """Test that database connection works"""
    from sqlalchemy import text
    
    result = db.execute(text("SELECT 1"))
    assert result.scalar() == 1


def test_database_version(db):
    """Test PostgreSQL version"""
    from sqlalchemy import text
    
    result = db.execute(text("SELECT version()"))
    version = result.scalar()
    assert "PostgreSQL" in version

