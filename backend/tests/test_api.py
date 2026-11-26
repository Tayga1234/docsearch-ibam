from fastapi.testclient import TestClient

from app.config import API_VERSION
from app.main import app


def test_health(isolated_storage):
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == API_VERSION
    assert "documents" in data
    assert "index_ready" in data
    assert "formats" in data
    assert "modes" in data


def test_ingest_scan_indexes_files(admin_api, sample_txt, sample_csv):
    client = admin_api
    response = client.post("/ingest/scan")

    assert response.status_code == 200
    data = response.json()
    assert data["indexed"] == 2

    documents = client.get("/documents").json()
    assert documents["total"] == 2
    assert len(documents["items"]) == 2


def test_ingest_upload_txt(admin_api):
    client = admin_api
    response = client.post(
        "/ingest/upload",
        files={"file": ("demo.txt", b"Upload via API", "text/plain")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "indexed"
    assert data["document"]["title"] == "demo.txt"


def test_ingest_upload_rejects_unsupported_format(admin_api):
    client = admin_api
    response = client.post(
        "/ingest/upload",
        files={"file": ("image.png", b"fake", "image/png")},
    )

    assert response.status_code == 400


def test_ingest_upload_unique_name_on_collision(admin_api):
    client = admin_api
    first = client.post(
        "/ingest/upload",
        files={"file": ("collision.txt", b"Premier", "text/plain")},
    )
    second = client.post(
        "/ingest/upload",
        files={"file": ("collision.txt", b"Second", "text/plain")},
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["document"]["title"] == "collision.txt"
    assert second.json()["document"]["title"] == "collision_1.txt"


def test_get_document_detail(admin_api, sample_txt):
    client = admin_api
    client.post("/ingest/scan")
    document_id = client.get("/documents").json()["items"][0]["id"]

    response = client.get(f"/documents/{document_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "note.txt"
    assert "DocSearch" in response.json()["content"]


def test_get_document_not_found(admin_api):
    client = admin_api
    response = client.get("/documents/inexistant")

    assert response.status_code == 404


def test_documents_pagination_and_filters(admin_api, sample_txt, sample_csv, isolated_storage):
    client = admin_api
    sci = isolated_storage["raw_dir"] / "sci_2024_ri_0001_bm25.txt"
    sci.write_text("BM25 ranking scientifique\nindex inversé", encoding="utf-8")
    client.post("/ingest/scan")

    page = client.get("/documents", params={"limit": 1, "offset": 0}).json()
    assert page["total"] == 3
    assert len(page["items"]) == 1
    assert "category" in page["items"][0]

    filtered = client.get("/documents", params={"file_type": "csv"}).json()
    assert filtered["total"] == 1
    assert filtered["items"][0]["file_type"] == "csv"

    queried = client.get("/documents", params={"q": "Alice"}).json()
    assert queried["total"] == 1

    scientific = client.get("/documents", params={"category": "scientific"}).json()
    assert scientific["total"] == 1
    assert scientific["items"][0]["category"] == "scientific"

    archives = client.get("/documents", params={"category": "archives"}).json()
    assert archives["total"] == 2

    by_class = client.get("/documents", params={"sort": "category", "limit": 10}).json()
    assert by_class["items"][0]["category"] == "scientific"

    health = client.get("/health").json()
    assert health["categories"]["scientific"] == 1
    assert health["categories"]["archives"] == 2


def test_delete_document(admin_api, sample_txt):
    client = admin_api
    client.post("/ingest/scan")
    document_id = client.get("/documents").json()["items"][0]["id"]

    blocked = client.delete(f"/documents/{document_id}")
    assert blocked.status_code == 400

    response = client.delete(f"/documents/{document_id}?confirm=true")
    assert response.status_code == 200
    assert response.json()["deleted"] is True

    assert client.get(f"/documents/{document_id}").status_code == 404
    assert client.get("/documents").json()["total"] == 0


def test_search_endpoint(admin_api, sample_txt):
    client = admin_api
    client.post("/ingest/scan")

    response = client.get("/search", params={"q": "DocSearch", "mode": "keyword"})

    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert data["results"][0]["title"] == "note.txt"


def test_search_requires_query(admin_api):
    client = admin_api
    response = client.get("/search", params={"q": "  "})

    assert response.status_code == 400


def test_search_compare_modes(admin_api, sample_txt):
    client = admin_api
    client.post("/ingest/scan")

    response = client.get("/search/compare", params={"q": "DocSearch"})

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "DocSearch"
    assert set(data["modes"]) == {"keyword", "semantic", "hybrid"}
    for hits in data["modes"].values():
        assert len(hits) <= 3
        assert any(hit["title"] == "note.txt" for hit in hits)


def test_search_compare_requires_query(admin_api):
    client = admin_api
    response = client.get("/search/compare", params={"q": "  "})

    assert response.status_code == 400


def test_documents_sort(admin_api, sample_txt, sample_csv):
    client = admin_api
    client.post("/ingest/scan")

    by_title = client.get("/documents", params={"sort": "title"}).json()["items"]
    titles = [item["title"] for item in by_title]
    assert titles == sorted(titles, key=str.lower)

    by_type = client.get("/documents", params={"sort": "type"}).json()["items"]
    types = [item["file_type"] for item in by_type]
    assert types == sorted(types)

    invalid = client.get("/documents", params={"sort": "score"})
    assert invalid.status_code == 400


def test_search_special_characters_does_not_crash(admin_api, sample_txt):
    client = admin_api
    client.post("/ingest/scan")

    response = client.get("/search", params={"q": 'AND OR " (', "mode": "keyword"})

    assert response.status_code == 200
    assert "results" in response.json()


def test_openapi_and_swagger_docs(isolated_storage):
    client = TestClient(app)
    docs = client.get("/docs")
    schema = client.get("/openapi.json").json()

    assert docs.status_code == 200
    assert schema["info"]["title"] == "DocSearch API"
    assert {tag["name"] for tag in schema["tags"]} >= {
        "Santé",
        "Ingestion",
        "Recherche",
        "Documents",
        "Index",
    }
    for path in (
        "/health",
        "/ingest/scan",
        "/ingest/upload",
        "/search",
        "/documents",
        "/documents/{document_id}",
        "/index/rebuild",
    ):
        assert path in schema["paths"]
    assert schema["paths"]["/search"]["get"]["summary"] == "Recherche selon le mode choisi"


def test_search_rejects_unknown_mode_and_limit(admin_api):
    client = admin_api
    unknown_mode = client.get("/search", params={"q": "DocSearch", "mode": "inconnu"})
    too_low = client.get("/search", params={"q": "DocSearch", "limit": 0})
    too_high = client.get("/search", params={"q": "DocSearch", "limit": 101})

    assert unknown_mode.status_code == 400
    assert too_low.status_code == 400
    assert too_high.status_code == 400


def test_rebuild_index_endpoint(admin_api, sample_txt, sample_csv):
    client = admin_api
    client.post("/ingest/scan")

    blocked = client.post("/index/rebuild")
    assert blocked.status_code == 400

    response = client.post("/index/rebuild?confirm=true")

    assert response.status_code == 200
    assert response.json()["indexed"] == 2

    search_response = client.get("/search", params={"q": "Alice"})
    assert search_response.json()["total"] == 1
