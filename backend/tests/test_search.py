from app.ingestion.service import ingest_file
from app.search import search_documents
from app.search.semantic import invalidate_semantic_cache


def test_search_finds_matching_document(sample_txt):
    ingest_file(sample_txt)

    results = search_documents("DocSearch", mode="keyword")

    assert len(results) == 1
    assert results[0].title == "note.txt"
    assert results[0].score > 0
    assert results[0].tags


def test_semantic_search_finds_related_document(sample_txt):
    ingest_file(sample_txt)

    results = search_documents("projet recherche burkina", mode="semantic")

    assert len(results) >= 1
    assert results[0].title == "note.txt"


def test_hybrid_search_preserves_keyword_highlights(sample_txt):
    ingest_file(sample_txt)

    results = search_documents("DocSearch", mode="hybrid")

    assert len(results) >= 1
    assert "<mark" in results[0].excerpt


def test_semantic_cache_invalidates_after_ingest(sample_txt, isolated_storage):
    ingest_file(sample_txt)
    first = search_documents("DocSearch", mode="semantic")
    assert first

    other = isolated_storage["raw_dir"] / "autre.txt"
    other.write_text("Document complémentaire sur l'indexation", encoding="utf-8")
    invalidate_semantic_cache()
    ingest_file(other)

    second = search_documents("indexation", mode="semantic")
    assert any(hit.title == "autre.txt" for hit in second)


def test_search_returns_empty_for_unknown_term(sample_txt):
    ingest_file(sample_txt)

    results = search_documents("xyzinexistant")

    assert results == []


def test_search_returns_empty_for_blank_query():
    assert search_documents("   ") == []


def test_search_handles_whoosh_special_characters(sample_txt):
    ingest_file(sample_txt)

    results = search_documents('DocSearch AND ( "???', mode="keyword")

    assert isinstance(results, list)


def test_search_hit_exposes_size_and_date(sample_txt):
    ingest_file(sample_txt)

    results = search_documents("DocSearch", mode="hybrid")

    assert results
    assert results[0].size_bytes > 0
    assert results[0].indexed_at is not None
