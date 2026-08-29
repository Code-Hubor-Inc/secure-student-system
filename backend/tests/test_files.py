import io


def _get_token(client, email):
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "testpass123", "full_name": "Files User"},
    )
    resp = client.post("/api/v1/auth/login", json={"email": email, "password": "testpass123"})
    return resp.json()["access_token"]


def test_upload_list_download_delete_roundtrip(client):
    token = _get_token(client, "filesuser@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    content = b"secret transcript contents"
    resp = client.post(
        "/api/v1/files/",
        headers=headers,
        files={"upload": ("transcript.txt", io.BytesIO(content), "text/plain")},
    )
    assert resp.status_code == 201
    file_id = resp.json()["id"]

    resp = client.get("/api/v1/files/", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp = client.get(f"/api/v1/files/{file_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.content == content

    resp = client.delete(f"/api/v1/files/{file_id}", headers=headers)
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/files/{file_id}", headers=headers)
    assert resp.status_code == 404


def test_cannot_access_other_users_file(client):
    token_a = _get_token(client, "usera@example.com")
    token_b = _get_token(client, "userb@example.com")

    resp = client.post(
        "/api/v1/files/",
        headers={"Authorization": f"Bearer {token_a}"},
        files={"upload": ("a.txt", io.BytesIO(b"user a data"), "text/plain")},
    )
    file_id = resp.json()["id"]

    resp = client.get(f"/api/v1/files/{file_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert resp.status_code == 404