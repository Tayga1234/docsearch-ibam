from fastapi.testclient import TestClient

from app.main import app


def test_login_user_and_admin(isolated_storage):
    client = TestClient(app)

    user = client.post("/auth/login", json={"username": "fatou", "password": "isgo"})
    admin = client.post("/auth/login", json={"username": "admin", "password": "archives"})

    assert user.status_code == 200
    assert user.json()["user"]["role"] == "user"
    assert user.json()["user"]["is_admin"] is False
    assert admin.status_code == 200
    assert admin.json()["user"]["role"] == "admin"
    assert admin.json()["user"]["is_admin"] is True


def test_login_rejects_bad_password(isolated_storage):
    client = TestClient(app)
    response = client.post("/auth/login", json={"username": "fatou", "password": "wrong"})
    assert response.status_code == 401


def test_user_cannot_scan_or_delete(user_api, sample_txt):
    scan = user_api.post("/ingest/scan")
    assert scan.status_code == 403

    user_api.post("/ingest/scan")  # still forbidden
    listed = user_api.get("/documents")
    assert listed.status_code == 200

    delete = user_api.delete("/documents/whatever")
    assert delete.status_code == 403


def test_public_space_allows_search_and_list(isolated_storage, sample_txt):
    client = TestClient(app)
    assert client.get("/search", params={"q": "DocSearch"}).status_code == 200
    assert client.get("/documents").status_code == 200
    assert client.get("/search/compare", params={"q": "DocSearch"}).status_code == 200


def test_admin_actions_require_login(isolated_storage):
    client = TestClient(app)
    assert client.post("/ingest/scan").status_code == 401
    assert client.post("/index/rebuild", params={"confirm": True}).status_code == 401


def test_admin_can_scan(admin_api, sample_txt):
    response = admin_api.post("/ingest/scan")
    assert response.status_code == 200
    assert response.json()["indexed"] == 1
