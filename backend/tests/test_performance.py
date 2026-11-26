"""Tests de performance (seuils du cahier des charges)."""

import time

import pytest

from app.extraction import extract_text
from app.indexing.whoosh_index import init_search_index, rebuild_index
from app.ingestion.service import ingest_file
from app.search.engine import search_documents


def _seed_corpus(raw_dir, count: int = 25) -> None:
    for index in range(count):
        path = raw_dir / f"perf_doc_{index:03d}.txt"
        path.write_text(
            f"Document performance {index}. DocSearch ISGO formation indexation Burkina.\n",
            encoding="utf-8",
        )


@pytest.mark.performance
def test_indexing_under_two_minutes(isolated_storage):
    raw_dir = isolated_storage["raw_dir"]
    _seed_corpus(raw_dir, count=30)

    start = time.perf_counter()
    indexed = 0
    for path in sorted(raw_dir.glob("perf_doc_*.txt")):
        ingest_file(path, force=True)
        indexed += 1
    duration = time.perf_counter() - start

    assert indexed == 30
    assert duration < 120, f"Indexation trop lente : {duration:.1f}s"


@pytest.mark.performance
def test_search_under_one_second(isolated_storage):
    raw_dir = isolated_storage["raw_dir"]
    _seed_corpus(raw_dir, count=20)

    for path in sorted(raw_dir.glob("perf_doc_*.txt")):
        ingest_file(path, force=True)

    from app.database import list_documents

    documents = list_documents()
    rebuild_index(documents)
    init_search_index(documents)

    durations = []
    for mode in ("keyword", "semantic", "hybrid"):
        start = time.perf_counter()
        hits = search_documents("formation DocSearch", mode=mode, limit=20)
        durations.append(time.perf_counter() - start)
        assert isinstance(hits, list)

    assert max(durations) < 1.0, f"Recherche trop lente : {max(durations):.3f}s"


def test_extractor_throughput(sample_txt):
    start = time.perf_counter()
    for _ in range(50):
        result = extract_text(sample_txt)
        assert result.content
    duration = time.perf_counter() - start
    assert duration < 5.0
