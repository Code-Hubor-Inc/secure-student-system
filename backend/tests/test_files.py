def _register_and_login(client, email="filer@example.com"):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "supersecret",
            "full_name": "File Owner",
        },
    )
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "supersecret"},
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_upload_list_download_delete_flow(client):
    headers = _register_and_login(client)

    upload_response = client.post(
        "/api/v1/files/upload",
        headers=headers,
        files={"file": ("hello.txt", b"hello world", "text/plain")},
    )
    assert upload_response.status_code == 200
    file_body = upload_response.json()
    assert file_body["original_filename"] == "hello.txt"
    assert file_body["file_size"] == len(b"hello world")
    file_id = file_body["id"]

    list_response = client.get("/api/v1/files/", headers=headers)
    assert list_response.status_code == 200
    files = list_response.json()
    assert len(files) == 1
    assert files[0]["id"] == file_id

    download_response = client.get(f"/api/v1/files/{file_id}/download", headers=headers)
    assert download_response.status_code == 200
    assert download_response.content == b"hello world"

    delete_response = client.delete(f"/api/v1/files/{file_id}", headers=headers)
    assert delete_response.status_code == 200

    list_after_delete = client.get("/api/v1/files/", headers=headers)
    assert list_after_delete.json() == []


def test_download_requires_ownership(client):
    owner_headers = _register_and_login(client, email="owner@example.com")
    other_headers = _register_and_login(client, email="other@example.com")

    upload_response = client.post(
        "/api/v1/files/upload",
        headers=owner_headers,
        files={"file": ("secret.txt", b"top secret", "text/plain")},
    )
    file_id = upload_response.json()["id"]

    response = client.get(f"/api/v1/files/{file_id}/download", headers=other_headers)
    assert response.status_code == 404


def test_files_require_authentication(client):
    response = client.get("/api/v1/files/")
    assert response.status_code == 401
