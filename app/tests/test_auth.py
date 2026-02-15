from app.core.security import verify_password


def test_signup_and_login(client):
    #signup
    response = client.post("/api/v1/auth/signup", json={
        "name": "Test User",
        "email": "test@example.com",
        "role": "student",
        "password": "password123"
    })
    assert response.status_code == 201
    signup_data = response.json()
    assert signup_data["name"] == "Test User"
    assert signup_data["email"] == "test@example.com"
    assert "id" in signup_data
    assert "hashed_password" not in signup_data

    #login
    response = client.post("/api/v1/auth/login", data={
        "username": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_signup_with_existing_email(client):
    # First signup
    response = client.post("/api/v1/auth/signup", json={
        "name": "Test User",
        "email": "test@example.com",
        "role": "student",
        "password": "password123"
    })
    assert response.status_code == 400

    # Second signup with same email
    response = client.post("/api/v1/auth/signup", json={
        "name": "Test User",
        "email": "test@example.com",
        "role": "student",
        "password": "password123"
    })

    assert response.status_code == 400

def test_login_with_invalid_credentials(client):
    # Attempt login with invalid credentials
    response = client.post("/api/v1/auth/login", data={
        "username": "text@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 400