from app.database import get_document, list_documents
from app.ingestion.scanner import scan_raw_directory
from app.ingestion.service import ingest_file, save_uploaded_file


def test_ingest_file_indexes_txt(sample_txt):
    result = ingest_file(sample_txt)

    assert result.status == "indexed"
    document = get_document(result.document_id)
    assert document is not None
    assert document.title == "note.txt"
    assert "DocSearch" in document.content
    assert document.metadata.get("content_hash")


def test_ingest_file_skips_unchanged_file(sample_txt):
    first = ingest_file(sample_txt)
    second = ingest_file(sample_txt)

    assert first.status == "indexed"
    assert second.status == "skipped"


def test_ingest_file_reindexes_when_content_changes_same_size(sample_txt):
    ingest_file(sample_txt)
    # Même taille approximative possible ; on change clairement le contenu
    sample_txt.write_text("AAAA\nContenu différent DocSearch", encoding="utf-8")

    result = ingest_file(sample_txt)
    document = get_document(result.document_id)

    assert result.status == "indexed"
    assert "différent" in document.content


def test_ingest_file_force_reindexes(sample_txt):
    ingest_file(sample_txt)
    sample_txt.write_text("Contenu modifié pour forcer la réindexation", encoding="utf-8")

    result = ingest_file(sample_txt, force=True)
    document = get_document(result.document_id)

    assert result.status == "indexed"
    assert "Contenu modifié" in document.content


def test_scan_raw_directory_indexes_all_supported_files(sample_txt, sample_csv, sample_docx):
    result = scan_raw_directory()

    assert result.scanned == 3
    assert result.indexed == 3
    assert result.errors == []
    assert len(list_documents()) == 3


def test_save_uploaded_file_writes_to_raw_dir(isolated_storage):
    path = save_uploaded_file("upload.txt", "Fichier uploade".encode("utf-8"))

    assert path.exists()
    assert path.read_bytes() == "Fichier uploade".encode("utf-8")
    assert path.parent == isolated_storage["raw_dir"]


def test_save_uploaded_file_avoids_overwrite(isolated_storage):
    first = save_uploaded_file("same.txt", b"one")
    second = save_uploaded_file("same.txt", b"two")

    assert first.name == "same.txt"
    assert second.name == "same_1.txt"
    assert first.read_bytes() == b"one"
    assert second.read_bytes() == b"two"
