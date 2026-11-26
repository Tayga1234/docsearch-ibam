import logging
import time
from dataclasses import dataclass, field
from pathlib import Path

from app.config import RAW_DATA_DIR, SUPPORTED_EXTENSIONS
from app.ingestion.service import commit_deferred_index, ingest_file
from app.models.document import Document

logger = logging.getLogger(__name__)


@dataclass
class ScanResult:
    scanned: int = 0
    indexed: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)


def scan_raw_directory(*, force: bool = False) -> ScanResult:
    result = ScanResult()
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    pending: list[Document] = []
    started = time.perf_counter()

    for path in sorted(RAW_DATA_DIR.iterdir()):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        result.scanned += 1

        try:
            ingest_result = ingest_file(path, force=force, defer_index=True)
            if ingest_result.status == "skipped":
                result.skipped += 1
            else:
                result.indexed += 1
                if ingest_result.document is not None:
                    pending.append(ingest_result.document)
        except Exception as exc:
            result.errors.append(f"{path.name}: {exc}")

    if pending:
        commit_deferred_index(pending)

    logger.info(
        "scan_raw_directory scanned=%s indexed=%s skipped=%s errors=%s duration_ms=%.1f",
        result.scanned,
        result.indexed,
        result.skipped,
        len(result.errors),
        (time.perf_counter() - started) * 1000,
    )
    return result
