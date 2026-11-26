import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import app


@pytest.fixture
def isolated_storage(tmp_path, monkeypatch):
    db_dir = tmp_path / "db"
    raw_dir = tmp_path / "raw"
    whoosh_dir = tmp_path / "whoosh"
    db_dir.mkdir()
    raw_dir.mkdir()

    monkeypatch.setattr(database, "DB_DIR", db_dir)
    monkeypatch.setattr(database, "DB_PATH", db_dir / "documents.db")
    monkeypatch.setattr("app.config.RAW_DATA_DIR", raw_dir)
    monkeypatch.setattr("app.config.WHOOSH_INDEX_DIR", whoosh_dir)
    monkeypatch.setattr("app.ingestion.scanner.RAW_DATA_DIR", raw_dir)
    monkeypatch.setattr("app.ingestion.service.RAW_DATA_DIR", raw_dir)
    monkeypatch.setattr("app.api.routes.RAW_DATA_DIR", raw_dir)
    monkeypatch.setattr("app.indexing.whoosh_index.WHOOSH_INDEX_DIR", whoosh_dir)

    database.init_db()
    return {"db_dir": db_dir, "raw_dir": raw_dir, "whoosh_dir": whoosh_dir}


def _login(client: TestClient, username: str, password: str) -> TestClient:
    response = client.post("/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200, response.text
    token = response.json()["token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def admin_api(isolated_storage):
    return _login(TestClient(app), "admin", "archives")


@pytest.fixture
def user_api(isolated_storage):
    return _login(TestClient(app), "fatou", "isgo")


@pytest.fixture
def sample_txt(isolated_storage):
    path = isolated_storage["raw_dir"] / "note.txt"
    path.write_text("Projet tutoré DocSearch\nBurkina Faso", encoding="utf-8")
    return path


@pytest.fixture
def sample_csv(isolated_storage):
    path = isolated_storage["raw_dir"] / "data.csv"
    path.write_text("nom,ville\nAlice,Ouaga\nBob,Bobo", encoding="utf-8")
    return path


@pytest.fixture
def sample_docx(isolated_storage):
    from docx import Document as DocxDocument

    path = isolated_storage["raw_dir"] / "rapport.docx"
    doc = DocxDocument()
    doc.add_paragraph("Rapport annuel")
    doc.add_paragraph("Indexation intelligente")
    doc.save(path)
    return path


@pytest.fixture
def sample_pdf(isolated_storage, monkeypatch):
    path = isolated_storage["raw_dir"] / "document.pdf"

    class FakePage:
        def extract_text(self):
            return "Contenu extrait du PDF de test"

    class FakePdf:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        @property
        def pages(self):
            # Deux pages : une avec texte, une vide → page_count total = 2
            return [FakePage(), FakePageEmpty()]

    class FakePageEmpty:
        def extract_text(self):
            return None

    def fake_open(file_path):
        return FakePdf()

    monkeypatch.setattr("app.extraction.pdf_extractor.pdfplumber.open", fake_open)
    path.write_bytes(b"%PDF-1.4 fake content")
    return path
