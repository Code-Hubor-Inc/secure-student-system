def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "alice@example.com",
            "password": "supersecret",
            "full_name": "Alice Example",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "alice@example.com"
    assert "hashed_password" not in body


def test_register_duplicate_email_rejected(client):
    payload = {
        "email": "bob@example.com",
        "password": "supersecret",
        "full_name": "Bob Example",
    }
    first = client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 200

    second = client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 400


def test_login_and_me(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "carol@example.com",
            "password": "supersecret",
            "full_name": "Carol Example",
        },
    )

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "carol@example.com", "password": "supersecret"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    assert login_response.json()["token_type"] == "bearer"

    me_response = client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "carol@example.com"


def test_login_with_wrong_password_fails(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "dave@example.com",
            "password": "supersecret",
            "full_name": "Dave Example",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        data={"username": "dave@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
