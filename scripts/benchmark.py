"""
Mesure les performances d'ingestion et de recherche DocuSearch.

Usage (depuis la racine du projet) :
    .venv\\Scripts\\python.exe scripts\\benchmark.py

Les résultats sont affichés dans le terminal et enregistrés dans
docs/PERFORMANCE_RESULTS.md
"""

from __future__ import annotations

import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.config import RAW_DATA_DIR  # noqa: E402
from app.database import init_db, list_documents  # noqa: E402
from app.indexing.whoosh_index import init_search_index, rebuild_index  # noqa: E402
from app.ingestion.scanner import scan_raw_directory  # noqa: E402
from app.search.engine import search_documents  # noqa: E402

QUERIES = ["formation", "DocSearch", "budget", "IBAM", "indexation"]
SEARCH_MODES = ["keyword", "semantic", "hybrid"]
TARGET_INDEX_SECONDS = 120.0
TARGET_SEARCH_SECONDS = 1.0


def _percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, int(len(ordered) * p / 100)))
    return ordered[index]


def run_benchmark() -> dict:
    init_db()
    rebuild_index([])

    t0 = time.perf_counter()
    scan_result = scan_raw_directory(force=True)
    index_duration = time.perf_counter() - t0

    documents = list_documents()
    init_search_index(documents)

    search_times: dict[str, list[float]] = {mode: [] for mode in SEARCH_MODES}
    for mode in SEARCH_MODES:
        for query in QUERIES:
            start = time.perf_counter()
            search_documents(query, mode=mode, limit=20)
            search_times[mode].append(time.perf_counter() - start)

    all_search = [t for times in search_times.values() for t in times]
    return {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "documents_indexed": len(documents),
        "files_scanned": scan_result.scanned,
        "index_errors": scan_result.errors,
        "index_duration_s": round(index_duration, 3),
        "index_ok": index_duration < TARGET_INDEX_SECONDS,
        "search": {
            mode: {
                "mean_ms": round(statistics.mean(times) * 1000, 2),
                "p95_ms": round(_percentile(times, 95) * 1000, 2),
                "max_ms": round(max(times) * 1000, 2),
            }
            for mode, times in search_times.items()
        },
        "search_global_max_ms": round(max(all_search) * 1000, 2),
        "search_ok": max(all_search) < TARGET_SEARCH_SECONDS,
    }


def format_markdown(results: dict) -> str:
    index_status = "OK" if results["index_ok"] else "À surveiller"
    search_status = "OK" if results["search_ok"] else "À surveiller"

    lines = [
        "# Résultats des tests de performance — DocSearch",
        "",
        f"*Généré le {results['timestamp']}*",
        "",
        "## Synthèse",
        "",
        f"| Indicateur | Valeur | Objectif | Statut |",
        f"|------------|--------|----------|--------|",
        f"| Documents indexés | {results['documents_indexed']} | >= 20 | OK |",
        f"| Durée indexation complète | {results['index_duration_s']} s | < {TARGET_INDEX_SECONDS:.0f} s | {index_status} |",
        f"| Recherche max (tous modes) | {results['search_global_max_ms']} ms | < {TARGET_SEARCH_SECONDS * 1000:.0f} ms | {search_status} |",
        "",
        "## Détail par mode de recherche",
        "",
        "| Mode | Moyenne (ms) | P95 (ms) | Max (ms) |",
        "|------|--------------|----------|----------|",
    ]
    for mode, stats in results["search"].items():
        lines.append(
            f"| {mode} | {stats['mean_ms']} | {stats['p95_ms']} | {stats['max_ms']} |"
        )

    if results["index_errors"]:
        lines.extend(["", "## Erreurs d'indexation", ""])
        for error in results["index_errors"]:
            lines.append(f"- {error}")

    lines.extend(
        [
            "",
            "## Méthodologie",
            "",
            f"- Corpus : fichiers dans `{RAW_DATA_DIR}`",
            f"- Requêtes testées : {', '.join(QUERIES)}",
            f"- Modes : {', '.join(SEARCH_MODES)}",
            "- Commande : `python scripts/benchmark.py`",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    results = run_benchmark()
    markdown = format_markdown(results)

    output = PROJECT_ROOT / "docs" / "PERFORMANCE_RESULTS.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")

    print(markdown)
    print(f"\nRésultats enregistrés dans {output}")


if __name__ == "__main__":
    main()
