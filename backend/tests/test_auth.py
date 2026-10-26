
def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "TestPassword@123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "user registered successfully"
    assert data["user"]["name"] == "Test User"
    assert data["user"]["email"] == "testuser@example.com"
    assert "id" in data["user"]
    assert "password" not in data["user"]


def test_login_with_valid_credentials(client):
    # Register the user first
    client.post(
        "/auth/register",
        json={
            "name": "Login Test User",
            "email": "loginuser@example.com",
            "password": "TestPassword@123",
        },
    )

    # Log in with the same credentials
    response = client.post(
        "/auth/login",
        json={
            "email": "loginuser@example.com",
            "password": "TestPassword@123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Login Successful"
    assert data["user"]["email"] == "loginuser@example.com"
    assert "access_token" in data
    assert data["access_token"]


def test_login_with_wrong_password(client):
    # Register the user first
    client.post(
        "/auth/register",
        json={
            "name": "Wrong Password User",
            "email": "wrongpassword@example.com",
            "password": "CorrectPassword@123",
        },
    )

    # Attempt login with an incorrect password
    response = client.post(
        "/auth/login",
        json={
            "email": "wrongpassword@example.com",
            "password": "WrongPassword@123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_with_unknown_email(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "unknownuser@example.com",
            "password": "TestPassword@123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
