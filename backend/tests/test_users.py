"""Test user endpoints with PostgreSQL"""

def test_get_current_user(client, auth_headers):
    """Test getting current user info"""
    response = client.get("/api/v1/users/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"


def test_get_current_user_unauthorized(client):
    """Test accessing protected route without token"""
    response = client.get("/api/v1/users/me")
    
    assert response.status_code == 401


def test_update_user(client, auth_headers):
    """Test updating user info"""
    response = client.put(
        "/api/v1/users/me",
        headers=auth_headers,
        json={"full_name": "Updated Name"}
    )
    
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"


def test_get_user_stats(client, auth_headers):
    """Test getting user statistics"""
    response = client.get("/api/v1/users/me/stats", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "total_analyses" in data
    assert data["total_analyses"] == 0  # No analyses yet

