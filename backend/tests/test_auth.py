def test_register_login_and_me(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "pytest@example.com", "password": "testpass123", "full_name": "Pytest User"},
    )
    assert resp.status_code == 201
    assert resp.json()["email"] == "pytest@example.com"

    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "pytest@example.com", "password": "testpass123"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]

    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "pytest@example.com"


def test_login_with_wrong_password_fails(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "wrongpass@example.com", "password": "correctpass", "full_name": "User"},
    )
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "wrongpass@example.com", "password": "incorrectpass"},
    )
    assert resp.status_code == 401


def test_duplicate_registration_fails(client):
    payload = {"email": "dup@example.com", "password": "testpass123", "full_name": "Dup User"}
    client.post("/api/v1/auth/register", json=payload)
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 400