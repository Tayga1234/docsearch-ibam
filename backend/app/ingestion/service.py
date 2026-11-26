import hashlib
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from app.config import MAX_UPLOAD_BYTES, RAW_DATA_DIR
from app.database import create_document_from_file, get_document_by_path, upsert_document
from app.extraction import extract_text
from app.indexing.whoosh_index import index_document, index_documents
from app.intelligence import enrich_document
from app.models.document import Document

logger = logging.getLogger(__name__)


@dataclass
class IngestFileResult:
    status: Literal["indexed", "skipped"]
    document_id: str | None = None
    document: Document | None = None


def file_fingerprint(path: Path) -> dict[str, str | float | int]:
    data = path.read_bytes()
    stat = path.stat()
    return {
        "content_hash": hashlib.sha256(data).hexdigest(),
        "mtime": stat.st_mtime,
        "size_bytes": stat.st_size,
    }


def should_skip_file(path: Path) -> bool:
    existing = get_document_by_path(str(path.resolve()))
    if existing is None:
        return False

    fingerprint = file_fingerprint(path)
    meta = existing.metadata or {}
    if meta.get("content_hash") == fingerprint["content_hash"]:
        return True

    # Compatibilité avec anciennes entrées : taille + mtime
    if (
        existing.size_bytes == fingerprint["size_bytes"]
        and meta.get("mtime") == fingerprint["mtime"]
    ):
        return True

    return False


def ingest_file(
    path: Path,
    *,
    force: bool = False,
    defer_index: bool = False,
) -> IngestFileResult:
    if not path.is_file():
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    if not force and should_skip_file(path):
        existing = get_document_by_path(str(path.resolve()))
        return IngestFileResult(
            status="skipped",
            document_id=existing.id if existing else None,
            document=existing,
        )

    started = time.perf_counter()
    fingerprint = file_fingerprint(path)
    extraction = extract_text(path)
    metadata = {
        **extraction.metadata,
        "content_hash": fingerprint["content_hash"],
        "mtime": fingerprint["mtime"],
    }
    document = create_document_from_file(
        source_path=path,
        title=path.name,
        content=extraction.content,
        file_type=path.suffix.lower().lstrip("."),
        mime_type=extraction.metadata.get("mime_type"),
        metadata=metadata,
    )
    document = enrich_document(document)
    saved = upsert_document(document)

    if not defer_index:
        index_document(saved)

    logger.info(
        "ingest_file path=%s status=indexed defer_index=%s duration_ms=%.1f",
        path.name,
        defer_index,
        (time.perf_counter() - started) * 1000,
    )
    return IngestFileResult(status="indexed", document_id=saved.id, document=saved)


def save_uploaded_file(filename: str, content: bytes) -> Path:
    if len(content) > MAX_UPLOAD_BYTES:
        raise ValueError(
            f"Fichier trop volumineux (max {MAX_UPLOAD_BYTES // (1024 * 1024)} Mo)"
        )

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = Path(filename).name
    destination = RAW_DATA_DIR / safe_name

    if destination.exists():
        stem = destination.stem
        suffix = destination.suffix
        counter = 1
        while True:
            candidate = RAW_DATA_DIR / f"{stem}_{counter}{suffix}"
            if not candidate.exists():
                destination = candidate
                break
            counter += 1

    destination.write_bytes(content)
    return destination


def commit_deferred_index(documents: list[Document]) -> int:
    return index_documents(documents)
